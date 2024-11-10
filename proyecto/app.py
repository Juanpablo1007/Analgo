import os
from flask import Flask, jsonify, request
from flask_cors import CORS  # Permitir solicitudes desde un dominio diferente

app = Flask(__name__)
CORS(app)  # Habilita CORS para aceptar solicitudes desde el frontend

@app.route('/api/ejecutar_funcion', methods=['POST'])
def ejecutar_funcion():
    # Lógica de negocio que deseas ejecutar
    resultado = {"mensaje": "Función ejecutada exitosamente"}
    return jsonify(resultado)

@app.route('/api/chart-2', methods=['POST'])
def ejecutar_chart():
    # Lógica de negocio para la segunda ruta
    resultado = {"mensaje": "Función chart"}
    return jsonify(resultado)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Usa el puerto asignado por Render o el puerto 5000 por defecto
    app.run(debug=True, host="0.0.0.0", port=port)
