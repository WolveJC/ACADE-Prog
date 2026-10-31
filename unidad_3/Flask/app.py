"""
Aplicación Flask de Gestión de Inventario para Touken Café.

Punto de entrada: crea la app, registra los blueprints y arranca el servidor.
  - config.py     → configuración
  - services/     → lógica de negocio (inventario, almacenamiento, PDF)
  - routes/       → controladores (blueprints)
"""

import os

from flask import Flask, session, url_for

from config import Config
from routes import exportar, inventario, mermas, movimientos, pedidos, productos, recepcion
from routes.comun import CLAVE_SESION, responder
from services.almacenamiento import AlmacenInventario


def create_app(config=None) -> Flask:
    """Fábrica de la aplicación. `config` permite sobrescribir valores (p. ej. en tests)."""
    app = Flask(__name__)
    app.config.from_object(Config)
    if config:
        app.config.update(config)

    # JSON legible: conserva tildes y el orden de las columnas.
    app.json.ensure_ascii = False
    app.json.sort_keys = False

    almacen = AlmacenInventario(app.config["DATA_DIR"])
    app.extensions["almacen"] = almacen
    eliminados = almacen.limpiar_antiguos(app.config["DIAS_RETENCION"])
    app.logger.info("Limpieza de archivos antiguos: %d eliminados.", eliminados)

    app.register_blueprint(inventario.bp)
    app.register_blueprint(pedidos.bp)
    app.register_blueprint(movimientos.bp)
    app.register_blueprint(recepcion.bp)
    app.register_blueprint(mermas.bp)
    app.register_blueprint(productos.bp)
    app.register_blueprint(exportar.bp)

    @app.context_processor
    def _contexto_plantillas():
        inv_id = session.get(CLAVE_SESION)
        return {"hay_inventario": bool(inv_id) and almacen.existe(inv_id)}

    @app.errorhandler(413)
    def _archivo_demasiado_grande(_error):
        limite = app.config["MAX_CONTENT_LENGTH"] // (1024 * 1024)
        return responder(
            f"El archivo supera el tamaño máximo permitido ({limite} MB).",
            413,
            destino=url_for("inventario.upload_csv"),
        )

    return app


app = create_app()

if __name__ == "__main__":
    # Seguro por defecto: sin modo debug y solo accesible desde esta máquina.
    # Para desarrollo:  FLASK_DEBUG=1 python app.py   (host: FLASK_HOST=0.0.0.0)
    app.run(
        debug=os.environ.get("FLASK_DEBUG") == "1",
        host=os.environ.get("FLASK_HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5000")),
    )
