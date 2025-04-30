from lxml import etree
import xmltodict
import json

class HC2ResponseParser:
    @staticmethod
    def limpiar_xml(xml_str):
        return xml_str.lstrip()

    @staticmethod
    def extract_inner_xml_from_cdata(xml_string: str) -> str:
        xml_string = HC2ResponseParser.limpiar_xml(xml_string)
        try:
            root = etree.fromstring(xml_string.encode('utf-8'))
        except etree.XMLSyntaxError as e:
            raise ValueError(f"1.Error al parsear XML externo: {e}")

        namespaces = {
            'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
            'ws': 'http://ws.hc2.dc.com/v1'
        }

        cdata_node = root.find('.//ws:consultarHC2Return', namespaces)
        if cdata_node is None or cdata_node.text is None:
            raise ValueError("2.No se encontró el nodo consultarHC2Return con CDATA.")

        inner_xml = cdata_node.text.strip()
        inner_xml = inner_xml.lstrip()

        try:
            parsed_dict = xmltodict.parse(inner_xml)
            json_str = json.dumps(parsed_dict, indent=2, ensure_ascii=False)
            return json_str
        except Exception as e:
            raise ValueError(f"3.Error al convertir XML a JSON: {e}")
