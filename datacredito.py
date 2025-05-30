from utils.signer import sign_soap
from lxml import etree
from hc2_parser  import HC2ResponseParser
from utils.caracteresespecialesreemplazador  import CaracteresEspecialesReemplazador
from utils.tildesreemplazador  import TildesReemplazador
import requests

WSDL_URL = "https://demo-servicesesb.datacredito.com.co:443/wss/dhws3/services/DHServicePlus"

def consultar_persona(data):
    # 1. Cargar plantilla
    with open("templates/request.xml", "r") as f:
        soap_xml = f.read()

    # 2. Reemplazar tildes
    data["primerApellido"] = TildesReemplazador().reemplazar(data["primerApellido"])

    # 3. Reemplazar datos
    for key, value in data.items():
        soap_xml = soap_xml.replace(f"${{{key}}}", str(value))

    # 4. Firmar SOAP
    signed_xml = sign_soap(soap_xml)

    # 5. Hacer el request
    headers = {"Content-Type": "text/xml; charset=utf-8"}
    # response = requests.post(WSDL_URL, data=signed_xml, headers=headers)
    response = requests.post(
        WSDL_URL,
        data=signed_xml,
        headers=headers,
        cert=("cert.pem", "key.pem")  # Certificados SSL para handshake HTTPS
    )
    #print("==== RESPUESTA ====")
    #print(response.text)
    reemplazador = CaracteresEspecialesReemplazador()
    texto_limpio = reemplazador.reemplazar(response.text)
    #print("\n==== TEXTO LIMPIO ====")
    #print(texto_limpio)
    #print("==== FIN ====")
    json_result = HC2ResponseParser.extract_inner_xml_from_cdata(texto_limpio)
    return json_result
    #return response.text
