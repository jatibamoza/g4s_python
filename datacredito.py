from utils.signer import sign_soap
from lxml import etree
from hc2_parser  import HC2ResponseParser
import requests

WSDL_URL = "https://demo-servicesesb.datacredito.com.co:443/wss/dhws3/services/DHServicePlus"

def consultar_persona(data):
    # 1. Cargar plantilla
    with open("templates/request.xml", "r") as f:
        soap_xml = f.read()

    # 2. Reemplazar datos
    for key, value in data.items():
        soap_xml = soap_xml.replace(f"${{{key}}}", str(value))

    # 3. Firmar SOAP
    signed_xml = sign_soap(soap_xml)

    # 4. Hacer el request
    headers = {"Content-Type": "text/xml; charset=utf-8"}
    # response = requests.post(WSDL_URL, data=signed_xml, headers=headers)
    response = requests.post(
        WSDL_URL,
        data=signed_xml,
        headers=headers,
        cert=("cert.pem", "key.pem")  # Certificados SSL para handshake HTTPS
    )
    json_result = HC2ResponseParser.extract_json_from_cdata(response.text)
    return json_result
