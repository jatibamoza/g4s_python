import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.tildesreemplazador import TildesReemplazador

texto_original = "José Pérez Álvarez está aquí con Íñigo y Úrsula."
reemplazador = TildesReemplazador()
texto_sin_tildes = reemplazador.reemplazar(texto_original)

print("Texto original:")
print(texto_original)
print("\nTexto sin tildes:")
print(texto_sin_tildes)