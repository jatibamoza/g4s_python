from hc2_parser import HC2ResponseParser  
from lxml import etree

with open("respuesta.txt", "r", encoding="utf-8") as f:
    contenido = f.read()

if __name__ == "__main__":
    try:
        resultado_json = HC2ResponseParser.extract_inner_xml_from_cdata(contenido)
        print("✅ JSON extraído correctamente:")
        print(resultado_json)
    except Exception as e:
        print("❌ Error:", str(e))
