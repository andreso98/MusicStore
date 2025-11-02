from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)

# Conexión base datos local
def get_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};SERVER=ANDRESO;DATABASE=MusicStoreDB;Trusted_Connection=yes;'
    )

# Ruta principal (solo para prueba)
@app.route('/')
def home():
    return "Servidor Flask activo - MusicStore"

# Ruta para guardar la cotización
@app.route('/guardarCotizacion', methods=['POST'])
def guardar_cotizacion():
    data = request.get_json()

    nombre = data['nombre']
    ciudad = data['ciudad']
    direccion = data['direccion']
    celular = data['celular']
    productos = data['productos']

    conn = get_connection()
    cursor = conn.cursor()

    for p in productos:
        cursor.execute("""
            INSERT INTO Cotizaciones (Nombre, Ciudad, Direccion, Celular, Producto, Cantidad, PrecioUnitario, Total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nombre, ciudad, direccion, celular, p['nombre'], p['cantidad'], p['precio'], p['total']))
    
    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Cotización guardada correctamente"}), 200

if __name__ == '__main__':
    app.run(debug=True)