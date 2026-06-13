from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)


def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "carrito"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "secret123"),
    )


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            cantidad INTEGER NOT NULL,
            precio NUMERIC(12,2) NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def index():
    return jsonify({"mensaje": "API Carrito de Compras", "version": "1.0"})


# Endpoint 1: Agregar producto
@app.route("/productos", methods=["POST"])
def agregar_producto():
    data = request.get_json()
    nombre = data.get("nombre")
    cantidad = data.get("cantidad")
    precio = data.get("precio")

    if not nombre or cantidad is None or precio is None:
        return jsonify({"error": "Faltan campos: nombre, cantidad, precio"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO productos (nombre, cantidad, precio) VALUES (%s, %s, %s) RETURNING id",
        (nombre, cantidad, precio),
    )
    nuevo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensaje": "Producto agregado", "id": nuevo_id}), 201


# Endpoint 2: Listar productos
@app.route("/productos", methods=["GET"])
def listar_productos():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, cantidad, precio FROM productos ORDER BY id")
    filas = cur.fetchall()
    cur.close()
    conn.close()

    productos = [
        {"id": f[0], "nombre": f[1], "cantidad": f[2], "precio": float(f[3])}
        for f in filas
    ]
    return jsonify(productos)


# Endpoint 3: Eliminar producto
@app.route("/productos/<int:producto_id>", methods=["DELETE"])
def eliminar_producto(producto_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM productos WHERE id = %s RETURNING id", (producto_id,))
    eliminado = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if eliminado:
        return jsonify({"mensaje": "Producto eliminado correctamente"})
    return jsonify({"error": "Producto no encontrado"}), 404


# Endpoint 4 (Parte 5): Calcular total del carrito
@app.route("/carrito/total", methods=["GET"])
def calcular_total():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COALESCE(SUM(cantidad * precio), 0) FROM productos")
    total = float(cur.fetchone()[0])
    cur.close()
    conn.close()

    return jsonify({"total": total})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)