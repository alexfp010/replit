from flask import Flask, jsonify, request
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)  # Conecta con ngrok

# Simulación de base de datos
productos = [
    {"id": 1, "nombre": "Cloro", "marca": "Cloralex", "categoria": "Limpieza", "precio": 25.5, "unidades": 100, "presentacion": "botella"},
    {"id": 2, "nombre": "Leche", "marca": "Lala", "categoria": "Lácteos", "precio": 18.0, "unidades": 200, "presentacion": "litro"},
    {"id": 3, "nombre": "Refresco", "marca": "Coca-Cola", "categoria": "Refrescos", "precio": 15.0, "unidades": 150, "presentacion": "lata"}
]

carrito = []

@app.route('/productos', methods=['GET'])
def obtener_productos():
    return jsonify(productos), 200

@app.route('/productos/<int:producto_id>', methods=['GET'])
def obtener_producto(producto_id):
    producto = next((p for p in productos if p['id'] == producto_id), None)
    if producto:
        return jsonify(producto), 200
    return jsonify({'mensaje': 'Producto no encontrado'}), 404

@app.route('/carrito', methods=['POST'])
def agregar_carrito():
    data = request.get_json()
    item = {
        "id": len(carrito) + 1,
        "producto_id": data['producto_id'],
        "cantidad": data['cantidad']
    }
    carrito.append(item)
    return jsonify(item), 201

@app.route('/carrito/<int:item_id>', methods=['PUT'])
def modificar_carrito(item_id):
    data = request.get_json()
    item = next((c for c in carrito if c['id'] == item_id), None)
    if item:
        item['cantidad'] = data['cantidad']
        return jsonify(item), 200
    return jsonify({'mensaje': 'Producto en carrito no encontrado'}), 404

@app.route('/carrito/<int:item_id>', methods=['DELETE'])
def eliminar_carrito(item_id):
    global carrito
    carrito = [c for c in carrito if c['id'] != item_id]
    return jsonify({'mensaje': 'Producto eliminado del carrito'}), 200

@app.route('/pedido/confirmar', methods=['POST'])
def confirmar_pedido():
    total = 0
    detalle = []
    for item in carrito:
        producto = next((p for p in productos if p['id'] == item['producto_id']), None)
        if producto:
            subtotal = producto['precio'] * item['cantidad']
            total += subtotal
            detalle.append({
                "producto": producto['nombre'],
                "cantidad": item['cantidad'],
                "subtotal": subtotal
            })
    pedido = {
        "pedido_id": 1,
        "total": total,
        "detalle": detalle
    }
    carrito.clear()
    return jsonify(pedido), 200

app.run(host='0.0.0.0', port=3000)
