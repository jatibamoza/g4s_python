from lxml import etree
import json
import re

class HC2ResponseParser:
    @staticmethod
    def limpiar_xml(xml_str):
        """
        Elimina espacios en blanco antes del encabezado XML
        para evitar errores de parseo.
        """
        return xml_str.lstrip()
    
    @staticmethod
    def extract_json_from_cdata(xml_string: str) -> str:
        xml_string = HC2ResponseParser.limpiar_xml(xml_string)  # Aplicamos limpieza
        try:
            root = etree.fromstring(xml_string.encode('utf-8'))
        except etree.XMLSyntaxError as e:
            raise ValueError(f"Error al parsear XML: {e}")

        namespaces = {
            'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
            'ws': 'http://servicios.datos.com'
        }

        cdata_node = root.find('.//ws:consultarHC2Return', namespaces)
        if cdata_node is None or cdata_node.text is None:
            raise ValueError("No se encontro el nodo consultarHC2Return con CDATA. xml_string: " + xml_string)

        cdata_text = cdata_node.text.strip()

        json_match = re.search(r'{.*}', cdata_text, re.DOTALL)
        if not json_match:
            raise ValueError("No se encontro un contenido JSON valido dentro del CDATA.")

        try:
            json_object = json.loads(json_match.group())
        except json.JSONDecodeError as e:
            raise ValueError(f"Error al parsear JSON del CDATA: {e}")

        return json.dumps(json_object, indent=2, ensure_ascii=False)