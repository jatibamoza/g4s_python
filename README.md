
# BridgeSalesforceDatacredito

Este proyecto expone un servicio REST en Python que actúa como puente entre Salesforce y el servicio SOAP de DataCrédito. Realiza lo siguiente:

- Recibe peticiones desde Salesforce con datos personales.
- Genera un XML SOAP firmado digitalmente (WS-Security).
- Envía la solicitud al endpoint SOAP de DataCrédito.
- Procesa la respuesta (incluyendo datos XML dentro de CDATA).
- Devuelve una respuesta XML o JSON estructurada para ser deserializada en Salesforce.

## 🧱 Estructura del proyecto

```
/templates               # Contiene la plantilla SOAP
/utils                  # Utilidades para limpiar caracteres y firmar XML
/test                   # Pruebas unitarias
/cert.pem, /key.pem     # Certificados SSL
datacredito.py          # Lógica principal del request SOAP
signer.py               # Firma WS-Security
hc2_parser.py           # Procesamiento XML del CDATA
app.py                  # Servicio Flask
requirements.txt
render.yaml             # Configuración de despliegue en Render
```

---

## 🚀 Despliegue en Render.com

1. **Crear el repositorio en GitHub** y subir el proyecto.
2. **Ir a [https://render.com](https://render.com)** y registrarse.
3. Crear un nuevo servicio → "Web Service".
4. Conectar tu cuenta de GitHub y seleccionar el repositorio.
5. Configurar:

   - **Environment**: `Python`
   - **Build Command**:  
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**:  
     ```bash
     python app.py
     ```
   - **Root Directory**: raíz del repositorio (vacío si está en la raíz)
   - **Region**: Oregon o la más cercana
   - **Free Plan**: puede usarse para pruebas

6. ***ESTO SE DEBE HACER EN PROD*** **Agregar variables de entorno (Environment Variables):**

   - `DATACREDITO_USERNAME`: usuario SOAP
   - `DATACREDITO_PASSWORD`: contraseña SOAP
   - `FLASK_ENV`: `production`

7. Render detectará el `render.yaml` automáticamente y aplicará la configuración.

---

## 🔐 Seguridad

- Las credenciales de DataCrédito se manejan mediante variables de entorno OJO EN PROD.
- El certificado `cert.pem` y la clave `key.pem` se utilizan para establecer HTTPS bidireccional.
- `signer.py` usa `lxml` y `cryptography` para firmar digitalmente el cuerpo del mensaje SOAP (WS-Security).

---

## 🧪 Test local

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate   # o venv\Scripts\activate en Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor local
python app.py

# Probar desde Postman o curl
curl -X POST http://localhost:5000/consultar -H "Content-Type: application/json" -d '{"primerApellido": "Pérez", ...}'
```

---

## ✅ Dependencias principales

- Flask
- lxml
- requests
- cryptography
- pyopenssl
- xmltodict

---

## 📬 Contacto

Proyecto para integración técnica entre Salesforce y DataCrédito Colombia.
Desarrollado por Javier Tibamoza.
