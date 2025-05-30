import json
import os

class TildesReemplazador:
    def __init__(self, archivo_parametrico="utils/vocales_tildes.json"):
        if not os.path.exists(archivo_parametrico):
            raise FileNotFoundError(f"No se encontró el archivo de configuración: {archivo_parametrico}")
        with open(archivo_parametrico, "r", encoding="utf-8") as f:
            self.reemplazos = json.load(f)

    def reemplazar(self, texto):
        for caracter_con_tilde, caracter_normal in self.reemplazos.items():
            texto = texto.replace(caracter_con_tilde, caracter_normal)
        return texto