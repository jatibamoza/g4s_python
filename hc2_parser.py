from lxml import etree
import re

class HC2ResponseParser:
    @staticmethod
    def limpiar_xml(xml_str):
        return xml_str.lstrip()

    @staticmethod
    def extract_inner_xml_from_cdata(xml_string: str) -> etree._Element:
        xml_string = HC2ResponseParser.limpiar_xml(xml_string)
        try:
            root = etree.fromstring(xml_string.encode('utf-8'))
        except etree.XMLSyntaxError as e:
            raise ValueError(f"Error al parsear XML externo: {e}")

        namespaces = {
            'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
            'ws': 'http://ws.hc2.dc.com/v1'
        }

        cdata_node = root.find('.//ws:consultarHC2Return', namespaces)
        if cdata_node is None or cdata_node.text is None:
            raise ValueError("No se encontró el nodo consultarHC2Return con CDATA.")

        inner_xml = cdata_node.text.strip()

        # Limpia espacios y posibles saltos de línea antes del <?xml
        inner_xml = inner_xml.lstrip()

        try:
            inner_root = etree.fromstring(inner_xml.encode('utf-8'))
        except etree.XMLSyntaxError as e:
            raise ValueError(f"Error al parsear XML interno dentro del CDATA: {e}")

        return inner_root
