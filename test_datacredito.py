from datacredito import consultar_persona

# Datos de prueba simulados (estos deben ser válidos según el servicio real)
datos = {
    "clave": "60AWA",
    "identificacion": "123573",
    "primerApellido": "REYES",
    "producto": "64",
    "tipoIdentificacion": "1",
    "usuario": "800215227"
}

resultado = consultar_persona(datos)
print("\n=== Resultado final ===")
print(resultado)
