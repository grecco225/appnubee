from flask import Flask, jsonify, request, send_file
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Carga el archivo .env automáticamente (solo en local; en PythonAnywhere usarás variables de entorno del dashboard)
load_dotenv()


# ─────────────────────────────────────────
# Configuración de la App
# ─────────────────────────────────────────
app = Flask(__name__)

# Lee las credenciales desde variables de entorno (forma segura)
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://ugwnnkzycpwurufcfxcx.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_m2i9T_MYya5EOESW22YvKg_o6Pd1QaW")

# Inicializa el cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ─────────────────────────────────────────
# Rutas de ejemplo — ¡Cámbialas por tu lógica!
# ─────────────────────────────────────────

@app.route("/")
def index():
    return """
    <html>
    <head>
        <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
        <meta charset="utf-8">
    </head>
    <body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
        <h2>¡Flask + Supabase funcionando!</h2>
        <p>Rutas disponibles:</p>
        <ul style="list-style:none; padding:0;">
            <li><a href="/estudiantes">GET /estudiantes</a> — Leer todos los estudiantes</li>
        </ul>
    </body>
    </html>
    """

@app.route("/favicon.ico")
def favicon():
    return send_file("favicon.ico", mimetype="image/x-icon")


# ─── Leer todos los estudiantes ─────────────
@app.route("/estudiantes", methods=["GET"])
def get_estudiantes():
    """Lee todos los registros de la tabla 'Estudiantes'."""
    try:
        response = supabase.table("Estudiantes").select("*").execute()
        return jsonify({"ok": True, "data": response.data})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# ─── Insertar un nuevo estudiante ───────────
@app.route("/estudiantes", methods=["POST"])
def crear_estudiante():
    """Inserta un nuevo registro en la tabla 'Estudiantes'."""
    body = request.get_json()
    if not body:
        return jsonify({"ok": False, "error": "Se requiere un cuerpo JSON"}), 400
    try:
        response = supabase.table("Estudiantes").insert(body).execute()
        return jsonify({"ok": True, "data": response.data}), 201
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# ─────────────────────────────────────────
# Arrancar el servidor
# ─────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5002)
