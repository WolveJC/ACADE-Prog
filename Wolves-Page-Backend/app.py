"""
Wolves-Page-Backend
-------------------
Backend minimo para el Cafe de Wolves-Page. Su unico trabajo es ser el
intermediario entre el navegador del usuario y las 3 APIs externas
(TheMealDB, RapidAPI/Edamam, Spoonacular), para:

1. Esconder las API keys (antes vivian hardcodeadas en el codigo del
   cliente -- CafePage.jsx y TriviaWidget.jsx -- visibles para cualquiera).
2. Evitar el CORS que bloqueaba las llamadas directas desde el navegador
   (servidor-a-servidor no tiene esa restriccion).
3. Limitar cuantas veces un mismo visitante puede disparar estas
   llamadas, para proteger la cuota gratuita de las 3 APIs.
"""

import os
import re

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests

load_dotenv()  # Lee el archivo .env en desarrollo local

app = Flask(__name__)

# -----------------------------------------------------------------
# CORS: solo el dominio real del frontend puede llamar a esta API.
# En local, FRONTEND_ORIGIN apunta a localhost:3000 (tu npm start).
# -----------------------------------------------------------------
FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "http://localhost:3000,https://dev-wolvespage.vercel.app")
ALLOWED_ORIGINS = [
   origin.strip().rstrip("/")
   for origin in FRONTEND_ORIGIN.split(",") 
   if origin.strip()
]
CORS(app, resources={r"/api/*": {"origins": ALLOWED_ORIGINS}})

# -----------------------------------------------------------------
# Limite de cuota. Por defecto usa memoria (storage_uri="memory://"),
# lo que significa: el contador vive mientras el proceso del servidor
# este corriendo. Si tu host gratuito "duerme" el servicio por
# inactividad y lo reinicia, el contador se reinicia con el -- esto
# es una limitacion conocida, no un error de este codigo. Cuando
# quieras que la cuota sobreviva reinicios, cambia storage_uri a un
# Redis externo (ej. Upstash, con capa gratuita) y listo.
# -----------------------------------------------------------------
limiter = Limiter(
    key_func=get_remote_address,  # identifica "dispositivo" por IP (ver nota abajo)
    app=app,
    storage_uri="memory://",
    default_limits=[],  # sin limite global; cada ruta define el suyo
)

SPOONACULAR_API_KEY = os.environ.get("SPOONACULAR_API_KEY")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
RAPIDAPI_HOST = "edamam-edamam-nutrition-analysis.p.rapidapi.com"

# Cuantas veces puede llamar la MISMA IP a cada endpoint, y en que
# ventana de tiempo. Ajusta esto a lo que realmente necesites.
QUOTA_LIMIT = "1 per day"


# ===================================================================
# Endpoint 1: Receta del dia (reemplaza el fetch directo a TheMealDB
# que vivia en RecipeCard.jsx)
# ===================================================================
@app.route("/api/receta", methods=["GET"])
@limiter.limit(QUOTA_LIMIT)
def get_receta():
    try:
        resp = requests.get(
            "https://www.themealdb.com/api/json/v1/1/random.php", timeout=10
        )
        resp.raise_for_status()
        return jsonify(resp.json())
    except requests.RequestException:
        return jsonify({"error": "No se pudo cargar la receta del día."}), 502


# ===================================================================
# Endpoint 2: Trivia de comida (reemplaza el fetch a Spoonacular que
# vivia en TriviaWidget.jsx, con la key hardcodeada)
# ===================================================================
@app.route("/api/trivia", methods=["GET"])
@limiter.limit(QUOTA_LIMIT)
def get_trivia():
    if not SPOONACULAR_API_KEY:
        return jsonify({"error": "API key no configurada en el servidor."}), 500

    try:
        resp = requests.get(
            "https://api.spoonacular.com/food/trivia/random",
            params={"apiKey": SPOONACULAR_API_KEY},
            timeout=10,
        )
        resp.raise_for_status()
        return jsonify(resp.json())
    except requests.RequestException:
        return jsonify({"error": "No se pudo cargar la trivia."}), 502


# ===================================================================
# normalize_ingredient: traduccion directa (misma logica, linea por
# linea) de la funcion del mismo nombre que vivia en CafePage.jsx.
# Se mueve aqui porque la normalizacion de ingredientes es parte de
# "preparar la consulta a Edamam", y eso ahora pasa en el servidor.
# ===================================================================
def normalize_ingredient(measure, ingredient):
    m = (measure or "").strip().lower()
    ing = (ingredient or "").strip().lower()

    m = re.sub(r"\btbs\b", "tbsp", m)
    m = re.sub(r"\btbls\b", "tbsp", m)
    m = re.sub(r"\btsp\b", "tsp", m)
    m = re.sub(r"\bml\b", " ml", m)
    m = re.sub(r"\bg\b", " g", m)
    m = re.sub(r"\bkg\b", " kg", m)
    m = re.sub(r"\bl\b", " l", m)
    m = re.sub(r"\bpinch\b", "1 pinch", m)
    m = re.sub(r"\bdash\b", "1 dash", m)
    m = re.sub(r"\bto taste\b", "", m)
    m = re.sub(r"\bas needed\b", "", m)

    ing = re.sub(r"free[- ]?range", "", ing, flags=re.IGNORECASE)
    ing = re.sub(r"beaten", "", ing, flags=re.IGNORECASE)
    ing = re.sub(r"pinkling", "pickling", ing, flags=re.IGNORECASE)
    ing = re.sub(r"sea salt", "salt", ing, flags=re.IGNORECASE)
    ing = re.sub(r"black pepper", "pepper", ing, flags=re.IGNORECASE)
    ing = re.sub(r"clove[s]? garlic", "garlic", ing, flags=re.IGNORECASE)
    ing = re.sub(r"egg[s]?", "egg", ing, flags=re.IGNORECASE)

    formatted = f"{m} {ing}".strip()
    if not m:
        formatted = ing
    return formatted


# ===================================================================
# Endpoint 3: Analisis nutricional (reemplaza el fetch a RapidAPI que
# vivia en CafePage.jsx, con la key hardcodeada). El cliente manda la
# receta completa (tal cual la devuelve TheMealDB) y este endpoint
# hace la normalizacion + la llamada a RapidAPI.
# ===================================================================
@app.route("/api/nutricion", methods=["POST"])
@limiter.limit(QUOTA_LIMIT)
def post_nutricion():
    if not RAPIDAPI_KEY:
        return jsonify({"error": "API key no configurada en el servidor."}), 500

    data = request.get_json(silent=True) or {}
    recipe = data.get("recipe")
    if not recipe:
        return jsonify({"error": "Falta la receta en el cuerpo de la petición."}), 400

    query_parts = []
    for i in range(1, 21):
        ingredient = recipe.get(f"strIngredient{i}")
        measure = recipe.get(f"strMeasure{i}")
        if ingredient and ingredient.strip():
            normalized = normalize_ingredient(measure, ingredient)
            query_parts.append(f"ingr={requests.utils.quote(normalized)}")

    if not query_parts:
        return jsonify({"error": "No se encontraron ingredientes para analizar."}), 400

    query_string = "&".join(query_parts)
    url = f"https://{RAPIDAPI_HOST}/api/nutrition-data?nutrition-type=cooking&{query_string}"

    try:
        resp = requests.get(
            url,
            headers={
                "x-rapidapi-key": RAPIDAPI_KEY,
                "x-rapidapi-host": RAPIDAPI_HOST,
            },
            timeout=15,
        )
        resp.raise_for_status()
        return jsonify(resp.json())
    except requests.RequestException:
        return jsonify(
            {"error": "El servicio de nutrición falló. Intenta más tarde."}
        ), 502

# ===================================================================
# Endpoint 4: Proxy de imagenes (evita bloqueos CORP / CORS)
# ===================================================================
@app.route("/api/proxy-imagen", methods=["GET"])
@limiter.limit("30 per minute")  # Limite adecuado para carga de imagenes
def proxy_imagen():
    image_url = request.args.get("url")
    
    # Validar que la URL venga de un origen permitido para evitar Server-Side Request Forgery (SSRF)
    if not image_url or not image_url.startswith("https://www.themealdb.com/"):
        return jsonify({"error": "Origen de imagen no permitido."}), 400

    try:
        resp = requests.get(image_url, timeout=10)
        resp.raise_for_status()
        
        # Devolver la imagen retransmitiendo su tipo de contenido (image/jpeg, etc.)
        content_type = resp.headers.get("Content-Type", "image/jpeg")
        return resp.content, 200, {"Content-Type": content_type}
        
    except requests.RequestException:
        return jsonify({"error": "No se pudo obtener la imagen."}), 502

# ===================================================================
# Ruta de salud, util para que Render/Railway confirmen que el
# servicio esta vivo, y para que tu mismo lo pruebes rapido.
# ===================================================================
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    # Solo para desarrollo local. En produccion, Render/Railway
    # arrancan el servidor con gunicorn (ver README.md).
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
