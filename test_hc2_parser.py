from hc2_parser import HC2ResponseParser  

sample_xml = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://servicios.datos.com">
  <soapenv:Header/>
  <soapenv:Body>
    <ws:consultarHC2Response>
      <ws:consultarHC2Return><![CDATA[
        {
          "Informes": {
            "Informe": [{
              "fechaConsulta": "2024-01-01",
              "respuesta": "OK",
              "codSeguridad": "ABC123",
              "NaturalNacional": {
                "nombres": "Juan",
                "primerApellido": "Pérez",
                "segundoApellido": "Gómez"
              }
            }]
          }
        }
      ]]></ws:consultarHC2Return>
    </ws:consultarHC2Response>
  </soapenv:Body>
</soapenv:Envelope>
"""

if __name__ == "__main__":
    try:
        result_json = HC2ResponseParser.extract_json_from_cdata(sample_xml)
        print("✅ JSON extraído correctamente:")
        print(result_json)
    except Exception as e:
        print("❌ Error:", str(e))
