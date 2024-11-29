from flask import Flask, jsonify
import pymysql

app = Flask(__name__)

# Configuración de la conexión a la base de datos
def obtener_conexion():
    return pymysql.connect(
        host='apimercadoagricola.cp0m2uu08onk.us-east-2.rds.amazonaws.com',
        user='admin',
        password='Efdade1146',
        database='api_mercado_agricola',
        cursorclass=pymysql.cursors.DictCursor
    )

# Función para obtener proveedores desde la base de datos
def obtener_proveedores():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT Nombre, Telefono, Correo, Direccion FROM Proveedores")
            return cursor.fetchall()  # Devuelve una lista de diccionarios
    finally:
        conexion.close()

# Función para obtener productos desde la base de datos
def obtener_productos():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT p.Nombre, p.Categoria, p.Precio, p.UnidadMedida, p.Cantidad, 
                       p.Disponible, pr.Nombre AS Proveedor
                FROM Productos p
                JOIN Proveedores pr ON p.ProveedorID = pr.ProveedorID
            """)
            return cursor.fetchall()  # Devuelve una lista de diccionarios
    finally:
        conexion.close()

# Ruta para buscar productos por categoría
@app.route('/Productos/Buscar/<categoria>', methods=['GET'])
def buscar_producto_por_categoria(categoria):
    productos = obtener_productos()
    productos_filtrados = [producto for producto in productos if producto['Categoria'].lower() == categoria.lower()]

    if productos_filtrados:
        return jsonify({
            "categoria": categoria,
            "productos": productos_filtrados
        })
    else:
        return jsonify({
            "error": "No se encontraron productos para esta categoría"
        }), 404

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
