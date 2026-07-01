import os
from flask import Flask, jsonify, request, send_file
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

# ─── Página principal ─────────────────────────────────────────
@app.route('/')
def index():
    return """
    <html>
    <head>
        <meta charset="utf-8">
        <title>Mi App</title>
    </head>
    <body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
        <h1>Flask + Supabase</h1>
        <a href="/estudiantes">Ver Estudiantes (JSON)</a>
    </body>
    </html>
    """

# ─── Leer todos los estudiantes ──────────────────────────────
@app.route('/estudiantes')
def get_estudiantes():
    response = supabase.table('Estudiantes').select("*").execute()
    estudiantes = response.data
    return jsonify({"ok": True, "data": estudiantes})

# ─── Insertar un estudiante ───────────────────────────────────
@app.route('/estudiantes', methods=['POST'])
def crear_estudiante():
    body = request.get_json()
    response = supabase.table('Estudiantes').insert(body).execute()
    return jsonify({"ok": True, "data": response.data}), 201

# ─── Favicon ──────────────────────────────────────────────────
@app.route('/favicon.ico')
def favicon():
    return send_file('favicon.ico', mimetype='image/x-icon')

if __name__ == '__main__':
    app.run(debug=True, port=5002)
