from flask import Flask, request, jsonify
import os

try:
    from datacredito import consultar_persona
except Exception as e:
    print("🚨 Error al importar datacredito.py:")
    import traceback
    traceback.print_exc()

app = Flask(__name__)

@app.route('/consultar', methods=['POST'])
def consultar():
    data = request.get_json()
    
    try:
        resultado = consultar_persona(data)
        return resultado, 200, {'Content-Type': 'text/xml'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

##if __name__ == "__main__":
##    app.run(debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
