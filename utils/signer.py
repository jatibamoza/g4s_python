import uuid
import base64
import os
from base64 import b64encode
from datetime import datetime, timezone
from cryptography.hazmat.primitives.serialization import pkcs12, Encoding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from lxml import etree

# Cargar certificado y clave privada desde el archivo .pfx
def load_keys(pfx_path, password):
    with open(pfx_path, 'rb') as f:
        pfx_data = f.read()
    private_key, certificate, _ = pkcs12.load_key_and_certificates(
        pfx_data, password.encode(), default_backend()
    )
    return private_key, certificate

# Canonicalizar nodo XML usando Exclusive Canonicalization (C14N)
def canonicalize(elem):
    return etree.tostring(elem, method="c14n", exclusive=True, with_comments=False)

# Calcular hash SHA1 y codificar en Base64
def sha1_base64(data: bytes) -> str:
    digest = hashes.Hash(hashes.SHA1(), backend=default_backend())
    digest.update(data)
    return b64encode(digest.finalize()).decode()

# Firmar el XML SOAP

def sign_soap(xml_string):
    private_key, cert = load_keys("genesys.pfx", "IxJR4e/Ua8/OfBw2")
    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.fromstring(xml_string.encode(), parser)

    # Asignar UUIDs dinámicos
    body_id = "Body-" + str(uuid.uuid4())

    # Buscar Body y Header
    body = root.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Body")
    header = root.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Header")

    # Limpiar Header antes de firmar
    header.clear()

    # Setear el wsu:Id dinámico en Body
    body.set("{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd}Id", body_id)

    # Canonicalizar Body limpio
    canonical_body = canonicalize(body)
    digest_value = sha1_base64(canonical_body)

    # Construir SignedInfo
    signed_info = etree.fromstring(f"""
    <ds:SignedInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
        <ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
        <ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
        <ds:Reference URI="#{body_id}">
            <ds:Transforms>
                <ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
            </ds:Transforms>
            <ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
            <ds:DigestValue>{digest_value}</ds:DigestValue>
        </ds:Reference>
    </ds:SignedInfo>
    """)

    # Canonicalizar SignedInfo
    canonical_signed_info = canonicalize(signed_info)

    # Firmar SignedInfo
    signature = private_key.sign(
        canonical_signed_info,
        padding.PKCS1v15(),
        hashes.SHA1()
    )
    signature_value = b64encode(signature).decode()

    # Certificado en Base64
    cert_der = cert.public_bytes(encoding=Encoding.DER)
    cert_b64 = b64encode(cert_der).decode()

    # Generar Nonce y Created
    nonce = base64.b64encode(os.urandom(16)).decode()
    created = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    # Construir UsernameToken
    username_token = f"""
    <wsse:UsernameToken>
        <wsse:Username>2-800215227</wsse:Username>
        <wsse:Password>ProduccionG4S2025*</wsse:Password>
        <wsse:Nonce>{nonce}</wsse:Nonce>
        <wsu:Created>{created}</wsu:Created>
    </wsse:UsernameToken>
    """

    # Construir WSSE Header completo
    wsse_header = f"""
    <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"
                   xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
        {username_token}
        <wsse:BinarySecurityToken EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary"
                                  ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3"
                                  wsu:Id="SecurityToken-1">{cert_b64}</wsse:BinarySecurityToken>
        <ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
            {etree.tostring(signed_info, encoding='unicode')}
            <ds:SignatureValue>{signature_value}</ds:SignatureValue>
            <ds:KeyInfo>
                <wsse:SecurityTokenReference>
                    <wsse:Reference URI="#SecurityToken-1"
                        ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3"/>
                </wsse:SecurityTokenReference>
            </ds:KeyInfo>
        </ds:Signature>
    </wsse:Security>
    """

    # Insertar nuevo Header firmado
    header.append(etree.fromstring(wsse_header))

    # Serializar XML final
    return etree.tostring(root, pretty_print=False, encoding="utf-8").decode()