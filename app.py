from flask import Flask, jsonify
from dbservice import obtener_proveedores, obtener_productos  # Importa funciones de la capa de servicio

app = Flask(__name__)

@app.route('/', methods=['GET'])
def mensaje_bienvenida():
    """
    Ruta de bienvenida que se muestra al iniciar la aplicación.
    """
    return jsonify({
        'mensaje': 'Bienvenido a la API de Mercado Agrícola'
    })

@app.route('/proveedores', methods=['GET'])
def lista_proveedores():
    try:
        proveedores = obtener_proveedores()  # Llama a la función del módulo
        return jsonify({
            'Proveedores': proveedores,
            'mensaje': f'Numero_de_proveedores_existentes: {len(proveedores)}'
        })
    except Exception as ex:
        return jsonify({'mensaje': 'ERROR'}), 500

@app.route('/productos', methods=['GET'])
def lista_productos():
    try:
        productos = obtener_productos()  # Llama a la función del módulo
        return jsonify({
            'Productos': productos,
            'mensaje': f'Numero_de_productos_existentes: {len(productos)}'
        })
    except Exception as ex:
        return jsonify({'mensaje': 'ERROR'}), 500

@app.route('/productos/buscar/<categoria>', methods=['GET'])
def buscar_producto_por_categoria(categoria):
    """
    Ruta para buscar productos por categoría.
    """
    try:
        productos = obtener_productos()  # Llama a la función para obtener productos
        productos_filtrados = [producto for producto in productos if producto['Categoria'].lower() == categoria.lower()]

        if productos_filtrados:
            return jsonify({
                'categoria': categoria,
                'productos': productos_filtrados,
                'mensaje': f'Numero_de_productos_encontrados: {len(productos_filtrados)}'
            })
        else:
            return jsonify({
                'mensaje': f'No se encontraron productos en la categoría: {categoria}'
            }), 404
    except Exception as ex:
        return jsonify({'mensaje': 'ERROR'}), 500

# ------------------- EJECUCIÓN DE LA APP -------------------
if __name__ == '__main__':
    app.run(debug=True)
