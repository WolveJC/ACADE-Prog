# Wolves-Page-Backend

Backend mínimo para el Café de [Wolves-Page](../Wolves-Page). Esconde las
API keys de TheMealDB/RapidAPI/Spoonacular, evita el CORS que bloqueaba
las llamadas directas desde el navegador, y limita cuántas veces un
mismo visitante puede llamar a cada API.

## Correrlo en local

```bash
cd Wolves-Page-Backend
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Abre .env y pon tus API keys reales de Spoonacular y RapidAPI
# (regenera ambas en sus paneles si no lo has hecho ya -- las
# anteriores quedaron expuestas en el código del cliente).

python app.py
```

Debería quedar corriendo en `http://localhost:5000`. Pruébalo con:

```bash
curl http://localhost:5000/api/health
curl http://localhost:5000/api/trivia
curl http://localhost:5000/api/receta
```

## Pendiente (no incluido en este primer esqueleto)

- **Despliegue real** (Render/Railway/etc.): falta decidir el host y
  configurar las variables de entorno ahí (nunca subas tu `.env` real).
- **Cambios en el frontend**: `RecipeCard.jsx`, `TriviaWidget.jsx` y
  `CafePage.jsx` todavía llaman directo a las APIs externas -- hay que
  apuntarlos a este backend (`/api/receta`, `/api/trivia`,
  `/api/nutricion`) una vez esté desplegado, y borrar las 2 keys que
  siguen hardcodeadas ahí.
- **CSP del frontend** (`vercel.json`): el `connect-src` que ajustamos
  recientemente para permitir TheMealDB/RapidAPI directo desde el
  navegador deja de ser necesario -- una vez el frontend hable solo con
  este backend, `connect-src` puede volver a ser simplemente la URL de
  este servicio.
- **Persistencia real de la cuota**: hoy el límite vive en memoria
  (`storage_uri="memory://"` en `app.py`). Si tu host gratuito duerme el
  servicio por inactividad, el contador se reinicia con cada despertar.
  Para que sea a prueba de reinicios, cambia `storage_uri` a un Redis
  externo (ej. la capa gratuita de Upstash).
