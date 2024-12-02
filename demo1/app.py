from firebase_admin import db
import firebase_admin
from flask import Flask, request, jsonify
from datetime import datetime
from firebase_admin.exceptions import FirebaseError
from flask_cors import CORS
from firebase_database import FirebaseDB

# IPara nicializar a Firebase
path = "credentials_key.json"
url = 'https://sensorapi-5552a-default-rtdb.firebaseio.com/'
fb_db=FirebaseDB(path, url)

# Para Inicializar Flask
app = Flask(__name__)
CORS(app) 

# Definir la referencia a la base de datos
fb_db_ref = db.reference('/sensor_data')

# Ruta para guardar datos de sensores (POST)
@app.route('/api/sensor_data', methods=['POST'])
def save_sensor_data():
    """
    Maneja las solicitudes POST para guardar datos de sensores.
    Valida el cuerpo de la solicitud, genera un timestamp y guarda los datos en Firebase.
    """
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.get_json()
        if not data:
            return jsonify({"error": "El cuerpo de la solicitud está vacío"}), 400

        # Extraer los valores necesarios
        idsensor = data.get('idsensor')
        valor = data.get('valor')

        # Validar campos obligatorios
        if not idsensor or valor is None:
            return jsonify({"error": "Los campos 'idsensor' y 'valor' son obligatorios"}), 400

        # Generar un timestamp para el registro
        timestamp = datetime.now()
        record = {
            "fecha": timestamp.strftime("%Y-%m-%d"),
            "hora": timestamp.strftime("%H:%M:%S"),
            "idsensor": idsensor,
            "valor": valor
        }

        # Guardar los datos en Firebase (auto-generando una ID)
        fb_db_ref.push(record)

        return jsonify({"message": "Datos del sensor guardados con éxito", "data": record}), 201

    except FirebaseError as e:
        return jsonify({"error": f"Error de Firebase: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500

# Ruta para obtener todos los datos de los sensores (GET)
@app.route('/api/sensor_data', methods=['GET'])
def get_sensor_data():
    """
    Maneja las solicitudes GET para recuperar todos los datos de sensores desde Firebase.
    """
    try:
        # Leer todos los datos desde Firebase
        data = fb_db_ref.get()

        # Si no hay datos, devolver una respuesta vacía
        if not data:
            return jsonify({"message": "No se encontraron datos de sensores", "data": []}), 200

        # Convertir los datos en una lista para facilitar su manejo
        sensor_data_list = [{"id": key, **value} for key, value in data.items()]
        return jsonify({"data": sensor_data_list}), 200

    except FirebaseError as e:
        return jsonify({"error": f"Error de Firebase: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500

# Ejecutar la aplicación Flask
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)