from caracteresespecialesreemplazador import CaracteresEspecialesReemplazador

texto_original = "Hola &lt;nombre&gt;, tu correo es test&#64;correo.com &amp; tu estado es &quot;activo&quot;."

reemplazador = CaracteresEspecialesReemplazador()
texto_limpio = reemplazador.reemplazar(texto_original)

print("Texto original:")
print(texto_original)
print("\nTexto limpio:")
print(texto_limpio)
