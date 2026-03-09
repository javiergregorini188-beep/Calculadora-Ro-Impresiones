import socket
import os
import sys

try:
    from flask import Flask, render_template, request, jsonify
except ImportError:
    print("\n❌ ERROR: La librería 'Flask' no está instalada. Ejecuta: pip install -r requirements.txt\n")
    sys.exit(1)

from models.calculadora import calcular_trabajo, calcular_anillado_dividido

# Crear la aplicación Flask
app = Flask(__name__)


@app.route("/")
def index():
    """Muestra la página principal de la calculadora."""
    return render_template("index.html")


@app.route("/calcular", methods=["POST"])
def handle_calculo():
    """
    Maneja la solicitud de cálculo inicial del formulario.
    Devuelve un JSON con los detalles del cálculo.
    """
    try:
        paginas = int(request.form.get("paginas", 0))
        tipo_color = request.form.get("tipo_color")
        tipo_faz = request.form.get("tipo_faz")
        lleva_anillado = request.form.get("anillado") == "on"

        resultado = calcular_trabajo(
            paginas, tipo_color, tipo_faz, lleva_anillado
        )
        return jsonify(resultado)

    except (ValueError, TypeError):
        return jsonify({"error": "Datos de entrada inválidos."}), 400


@app.route("/calcular-dividido", methods=["POST"])
def handle_calculo_dividido():
    """
    Maneja el cálculo para trabajos divididos en múltiples tomos.
    """
    try:
        hojas = int(request.form.get("hojas", 0))
        tomos = int(request.form.get("tomos", 0))

        division = calcular_anillado_dividido(hojas, tomos)

        if division:
            return jsonify(division)
        return jsonify({"error": "No se pudo calcular la división."}), 400

    except (ValueError, TypeError):
        return jsonify({"error": "Datos de entrada inválidos para la división."}), 400


def obtener_ip_local():
    """Intenta obtener la IP local de la máquina para mostrarla."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No necesita ser alcanzable, solo para detectar la interfaz correcta
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == "__main__":
    # Configuración para Render: obtener el puerto de las variables de entorno
    port = int(os.environ.get("PORT", 5000))

    if port == 5000:
        host_ip = obtener_ip_local()
        print(f"\n--- APLICACIÓN LISTA ---")
        print(f"Abre esta dirección en el navegador de tu celular:")
        print(f"➡️   http://{host_ip}:{port}")
        print(f"------------------------\n")

    # Se usa host='0.0.0.0' para aceptar conexiones desde la red (ej: el celular)
    app.run(debug=True, host='0.0.0.0', port=port)