import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datacredito import consultar_persona

# Datos de prueba simulados (estos deben ser válidos según el servicio real)
datos = {
    "clave": "60AWA",
    "identificacion": "29115313",
    "primerApellido": "EL HAGE",
    "producto": "64",
    "tipoIdentificacion": "1",
    "usuario": "800215227"
}

resultado = consultar_persona(datos)
print("\n=== Resultado final ===")
print(resultado)
