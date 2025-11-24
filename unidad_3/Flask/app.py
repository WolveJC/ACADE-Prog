"""
Aplicación Flask de Gestión de Inventario para Touken Café.

Permite subir inventario CSV, crear inventario manualmente, realizar pedidos
internos (stock) y generar pedidos a proveedor en formato PDF, con funciones
de limpieza y exportación.
"""

# Standard library
import csv
import datetime
import io
import os
import random
import string
import time
from typing import List, Tuple, Dict, Union, Any

# Third-party libraries
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
    send_file,
)
from fpdf import FPDF
import pandas as pd
from pandas.errors import EmptyDataError, ParserError


# Configuración básica de Flask
app = Flask(__name__)
# ¡Cambia esto por una clave secreta segura en producción!
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "secret-key-default-insecure")
UPLOAD_FOLDER = "uploads"

# Crear carpeta uploads si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def generar_codigo_aleatorio(longitud: int = 6) -> str:
    """
    Genera un código alfanumérico aleatorio de la longitud especificada.

    Args:
        longitud: La longitud deseada para el código (por defecto es 6).

    Returns:
        Una cadena alfanumérica aleatoria.
    """
    caracteres = string.ascii_uppercase + string.digits
    return "".join(random.choices(caracteres, k=longitud))


def limpiar_archivos_antiguos(dias: int = 1):
    """
    Elimina archivos de la carpeta 'uploads' que sean más antiguos
    que el número de días especificado.

    Args:
        dias: Número de días de antigüedad para considerar un archivo como 'antiguo'.
    """
    ahora = time.time()
    segundos_limite = dias * 24 * 3600
    archivos_eliminados = 0
    print("Ejecutando limpieza de archivos antiguos...")

    folder_path = app.config["UPLOAD_FOLDER"]
    if os.path.exists(folder_path):
        for nombre_archivo in os.listdir(folder_path):
            ruta_archivo = os.path.join(folder_path, nombre_archivo)
            try:
                if os.path.isfile(ruta_archivo):
                    # Usar getmtime (tiempo de última modificación)
                    timestamp_modificacion = os.path.getmtime(ruta_archivo)
                    if (ahora - timestamp_modificacion) > segundos_limite:
                        os.remove(ruta_archivo)
                        print(f"Archivo antiguo eliminado: {ruta_archivo}")
                        archivos_eliminados += 1
            except (OSError, PermissionError) as e:
                # Capturar errores del sistema operativo o permisos
                print(f"Error al procesar o eliminar {ruta_archivo}: {e}")

    if archivos_eliminados > 0:
        print(f"Se eliminaron {archivos_eliminados} archivos antiguos de {folder_path}.")
    else:
        print(f"No se encontraron archivos antiguos para eliminar en {folder_path}.")


# Ejecutar la limpieza al inicio de la aplicación (en contexto)
with app.app_context():
    limpiar_archivos_antiguos(dias=1)

# ==========================================================================
#                       RUTAS DE LA APLICACIÓN
# ==========================================================================


def _guardar_inventario_csv(inventario_data: list, filename: str) -> str:
    """Función auxiliar para guardar la lista de inventario en un archivo CSV."""
    ruta_archivo_creado = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if (
        not inventario_data
        or not isinstance(inventario_data, list)
        or not all(isinstance(item, dict) for item in inventario_data)
    ):
        raise ValueError("Formato de inventario inválido o vacío.")

    fieldnames = inventario_data[0].keys()

    try:
        with open(ruta_archivo_creado, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(inventario_data)
        return ruta_archivo_creado
    except KeyError as e:
        # W0707: Usar 'from e' para encadenar la excepción original
        raise KeyError(f"Error de clave al procesar inventario: falta la clave {e}") from e
    except (IOError, OSError) as e:
        # W0707: Usar 'from e' para encadenar la excepción original
        raise OSError(f"Error del sistema al guardar el archivo CSV: {e}") from e


@app.route("/crear_inventario", methods=["GET", "POST"])
def crear_inventario():
    """Ruta para mostrar la interfaz o procesar la creación manual del inventario."""
    if request.method == "POST":
        if not request.is_json:
            flash("Método no soportado. Use la interfaz interactiva.", "error")
            return redirect(url_for("crear_inventario"))

        data = request.get_json()
        inventario_para_guardar = data.get("inventario")

        if not data.get("guardar_csv") or not inventario_para_guardar:
            return jsonify({"message": "Datos inválidos o acción no reconocida."}), 400

        nombre_archivo_creado = (
            f"inventario_creado_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        try:
            ruta_archivo_creado = _guardar_inventario_csv(
                inventario_para_guardar, nombre_archivo_creado
            )

            # Cargar datos en la sesión
            session["csv_filepath"] = ruta_archivo_creado
            df = pd.read_csv(ruta_archivo_creado)
            df.fillna("", inplace=True)
            session["productos"] = df.to_dict(orient="records")

            session.pop("inventario_creado", None)

            return (
                jsonify(
                    {"message": (f"Inventario creado y guardado como {nombre_archivo_creado}.")}
                ),
                200,
            )
        except (KeyError, ValueError, OSError) as e:
            # Captura errores internos de la función auxiliar
            return (
                jsonify({"message": f"Error en los datos del inventario: {e}"}),
                400,
            )

    # Método GET: Mostrar la página
    inventario_temporal = session.get("inventario_creado", [])
    return render_template("crear_inventario.html", inventario_creado=inventario_temporal)


# --------------------------------------------------------------------------
def _manejar_subida_csv(file):
    """Función auxiliar para validar y procesar el archivo CSV subido."""
    if not file.filename.lower().endswith(".csv") or file.content_type != "text/csv":
        return "Por favor, sube un archivo CSV válido (.csv)."

    filename = file.filename
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    try:
        file.save(filepath)

        data = pd.read_csv(filepath)

        columnas_esperadas = [
            "Código",
            "Nombre",
            "Cantidad",
            "Demanda",
            "Tiempo entrega(Días)",
            "Fecha límite",
        ]
        if not all(col in data.columns for col in columnas_esperadas):
            raise ValueError(f"El CSV debe contener las columnas: {', '.join(columnas_esperadas)}")

        data.fillna("", inplace=True)
        json_data = data.to_dict(orient="records")

        # Guardar en sesión
        session["productos"] = json_data
        session["csv_filepath"] = filepath
        print(f"Archivo CSV cargado: {filepath}")
        return None  # Indica éxito

    except EmptyDataError:
        return "El archivo CSV está vacío."
    except ParserError:
        return "Error al procesar el archivo CSV. Verifique el formato."
    except ValueError as e:
        return str(e)
    # W0718: Capturamos errores generales de I/O o Pandas que no sean los anteriores.
    except (OSError, RuntimeError) as e:
        return f"Ocurrió un error inesperado al procesar el archivo: {e}"
    finally:
        # Asegurarse de limpiar archivos inválidos o fallidos
        if os.path.exists(filepath) and "productos" not in session:
            try:
                os.remove(filepath)
                print(f"Archivo fallido eliminado: {filepath}")
            except OSError:
                pass


def _responder_upload(mensaje: str, status_code: int, es_error: bool = False):
    """
    Auxiliar para R0911: Centraliza la respuesta de upload_csv.
    """
    if request.is_json:
        return jsonify({"message": mensaje}), status_code

    if es_error:
        flash(mensaje, "error")  # Asumiendo que la plantilla soporta categorías
    else:
        flash(mensaje)

    return redirect(request.url if es_error else url_for("upload_csv"))


@app.route("/", methods=["POST", "GET"])
def upload_csv():
    """Ruta de inicio para subir CSV de inventario."""
    # R0911 Corregido: Lógica simplificada delegando respuestas
    if request.method == "POST":
        if "file" not in request.files or request.files["file"].filename == "":
            return _responder_upload("No se seleccionó ningún archivo.", 400, es_error=True)

        error_message = _manejar_subida_csv(request.files["file"])

        if error_message:
            return _responder_upload(error_message, 400, es_error=True)

        # Éxito
        return _responder_upload("Archivo CSV cargado con éxito.", 200, es_error=False)

    # Método GET
    return render_template("subir_csv.html")


# --------------------------------------------------------------------------


def _procesar_formulario_stock(form_data: dict) -> Dict[str, int]:
    """
    Auxiliar para R0914: Extrae y valida el pedido del formulario.
    Returns: Diccionario con {codigo: cantidad}.
    """
    pedido_stock = {}
    for key, value in form_data.items():
        if key.startswith("pedido_stock[") and key.endswith("]"):
            codigo_limpio = key[len("pedido_stock[") : -1]
            try:
                cantidad_pedida = int(value)
                if cantidad_pedida > 0:
                    pedido_stock[codigo_limpio] = cantidad_pedida
            except ValueError:
                # Ignoramos valores no numéricos silenciosamente o logueamos
                pass
    return pedido_stock


def _actualizar_stock_inventario(
    productos: List[Dict], pedido_stock: Dict[str, int]
) -> Tuple[List[Dict], List[str], bool]:
    """
    Auxiliar para R0914/R0912: Aplica la lógica de negocio para actualizar el stock.
    """
    resultados_msg = []
    hubo_cambios = False
    factor_aprendizaje = 0.3
    # Copiamos la lista para no mutar la original directamente si falla algo
    productos_actualizados = [p.copy() for p in productos]

    for producto in productos_actualizados:
        codigo_str = str(producto["Código"])
        if codigo_str in pedido_stock:
            cantidad_pedida = pedido_stock[codigo_str]
            stock_actual = int(producto.get("Cantidad") or 0)
            demanda_actual = int(producto.get("Demanda") or 0)

            if cantidad_pedida <= stock_actual:
                producto["Cantidad"] = stock_actual - cantidad_pedida

                # Ajuste de demanda
                nueva_demanda = (
                    demanda_actual + (cantidad_pedida - demanda_actual) * factor_aprendizaje
                )
                producto["Demanda"] = min(round(nueva_demanda), 10)

                resultados_msg.append(
                    f"Pedido de {cantidad_pedida} {producto['Nombre']} OK. "
                    f"Nuevo stock: {producto['Cantidad']}"
                )
                hubo_cambios = True
            else:
                resultados_msg.append(
                    f"Stock insuficiente de {producto['Nombre']} "
                    f"(disp: {stock_actual}) para pedir {cantidad_pedida}."
                )

    return productos_actualizados, resultados_msg, hubo_cambios


@app.route("/pedir_stock", methods=["GET", "POST"])
def pedir_stock():
    """
    Ruta para procesar el pedido de stock interno y actualizar el inventario.
    Refactorizada para reducir complejidad (R0914, R0912).
    """
    productos = session.get("productos")
    if not productos:
        flash("No hay inventario cargado. Sube o crea un archivo CSV.", "warning")
        return redirect(url_for("upload_csv"))

    if request.method == "POST":
        # 1. Procesar Formulario
        pedido_stock = _procesar_formulario_stock(request.form)

        if not pedido_stock:
            return jsonify({"message": "No se especificó ninguna cantidad válida."}), 400

        # 2. Actualizar Lógica de Negocio
        # W0612 Corregido: 'productos_dict' eliminado pues no se usaba
        productos_nuevos, mensajes, cambios = _actualizar_stock_inventario(productos, pedido_stock)

        # 3. Persistencia
        if cambios:
            session["productos"] = productos_nuevos
            csv_path = session.get("csv_filepath")
            if csv_path and os.path.exists(csv_path):
                try:
                    df = pd.DataFrame(productos_nuevos)
                    df.to_csv(csv_path, index=False, encoding="utf-8")
                except (IOError, OSError) as e:
                    print(f"Error al actualizar CSV de inventario: {e}")

        return (
            jsonify(
                {
                    "message": "Proceso de pedido de stock completado.",
                    "detalles": mensajes,
                    "hubo_cambios": cambios,
                }
            ),
            200,
        )

    return render_template("pedir_stock.html", productos_stock=productos)


# --------------------------------------------------------------------------


# E1136 Corregido: Usar Tuple[list, list] en lugar de tuple[list, list]
def _obtener_y_validar_pedido(productos: list, form_data: dict) -> Tuple[List, List]:
    """
    Función auxiliar para extraer y validar los datos del pedido del proveedor.
    """
    pedido_proveedor = []
    errores_validacion = []
    productos_dict = {str(p["Código"]): p for p in productos}

    codigos_pedidos = set()
    for key in form_data.keys():
        if key.startswith("pedido_proveedor[") and key.endswith("]"):
            codigos_pedidos.add(key[len("pedido_proveedor[") : -1])

    for codigo in codigos_pedidos:
        cantidad_str = form_data.get(f"pedido_proveedor[{codigo}]")
        precio_str = form_data.get(f"precio_proveedor[{codigo}]")
        producto_info = productos_dict.get(codigo)

        if not producto_info:
            errores_validacion.append(f"Producto {codigo} no encontrado.")
            continue

        try:
            cantidad = int(cantidad_str) if cantidad_str else 0
            if cantidad < 0:
                errores_validacion.append(f"Producto {codigo}: Cantidad negativa.")
                continue
        except ValueError:
            errores_validacion.append(f"Producto {codigo}: Cantidad inválida.")
            continue

        if cantidad > 0:
            try:
                precio = float(precio_str) if precio_str else 0.0
                if precio <= 0:
                    errores_validacion.append(f"Producto {codigo}: Precio debe ser > 0.")
                    continue
            except ValueError:
                errores_validacion.append(f"Producto {codigo}: Precio inválido.")
                continue

            pedido_proveedor.append(
                {
                    "codigo": producto_info["Código"],
                    "nombre": producto_info["Nombre"],
                    "cantidad": cantidad,
                    "precio_unitario": precio,
                    "tiempo_entrega": producto_info.get("Tiempo entrega(Días)", "N/A"),
                    "stock_actual": producto_info.get("Cantidad", "N/A"),
                }
            )

    return pedido_proveedor, errores_validacion


@app.route("/pedir_proveedor", methods=["GET", "POST"])
def pedir_proveedor():
    """Ruta para recopilar y procesar los datos del pedido al proveedor."""
    productos = session.get("productos")
    if not productos:
        flash("No hay inventario cargado.", "warning")
        return redirect(url_for("upload_csv"))

    if request.method == "POST":
        # W0718 Corregido: Se captura KeyError/ValueError explícitamente si ocurren
        try:
            pedido_prov, errores = _obtener_y_validar_pedido(productos, request.form)

            if errores:
                return jsonify({"message": "Errores en el formulario.", "errors": errores}), 400

            if not pedido_prov:
                return jsonify({"message": "No se seleccionaron productos válidos."}), 400

            session["pedido_proveedor"] = pedido_prov

            return (
                jsonify(
                    {
                        "message": "Pedido listo para generar PDF.",
                        "redirect_url": url_for("generar_pdf_proveedor"),
                    }
                ),
                200,
            )

        except (KeyError, ValueError) as e:
            print(f"Error de datos en /pedir_proveedor: {e}")
            return jsonify({"message": f"Error al procesar datos: {e}"}), 400
        except Exception as e:
            print(f"Error inesperado en /pedir_proveedor: {e}")
            return jsonify({"message": "Error interno del servidor."}), 500

    return render_template("pedir_proveedor.html", productos_proveedor=productos)


# --------------------------------------------------------------------------


# E1136 Corregido: Usar Tuple[bytes, str]
def _crear_pdf_pedido(pedido_proveedor: list) -> Tuple[bytes, str]:
    """Función auxiliar para generar el contenido binario del PDF."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(0, 10, "Pedido al Proveedor - Touken Café", ln=True, align="C")
    pdf.set_font("Arial", size=9)
    pdf.cell(0, 5, f"Fecha de Generación: {fecha_hora}", ln=True, align="C")
    pdf.ln(8)

    # Encabezados
    pdf.set_font("Arial", "B", size=10)
    col_widths = [25, 75, 25, 30, 35]
    headers = ["Código", "Producto", "Cantidad", "Precio Unit.", "Precio Total"]
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, border=1, align="C")
    pdf.ln()

    # Contenido
    pdf.set_font("Arial", size=9)
    total_pedido = 0.0
    for item in pedido_proveedor:
        precio_total_item = item["cantidad"] * item["precio_unitario"]
        total_pedido += precio_total_item

        pdf.cell(col_widths[0], 8, str(item["codigo"]), border=1)

        x_before = pdf.get_x()
        y_before = pdf.get_y()
        pdf.multi_cell(col_widths[1], 8, item["nombre"], border=1, align="L")

        # W0612 Corregido: Se eliminó 'line_height' que no se usaba
        pdf.set_xy(x_before + col_widths[1], y_before)

        pdf.cell(col_widths[2], 8, str(item["cantidad"]), border=1, align="C")
        pdf.cell(col_widths[3], 8, f"${item['precio_unitario']:.2f}", border=1, align="R")
        pdf.cell(col_widths[4], 8, f"${precio_total_item:.2f}", border=1, align="R")
        pdf.ln()

    pdf.ln(5)
    pdf.set_font("Arial", "B", size=10)
    pdf.cell(sum(col_widths) - col_widths[-1], 10, "Total del Pedido:", border=0, align="R")
    pdf.cell(col_widths[-1], 10, f"${total_pedido:.2f}", border=1, align="R")
    pdf.ln()

    pdf_filename = f"pedido_proveedor_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    buffer = io.BytesIO(pdf.output(dest="S").encode("latin-1"))

    return buffer, pdf_filename


@app.route("/generar_pdf_proveedor", methods=["GET"])
def generar_pdf_proveedor():
    """Ruta para generar el PDF del pedido almacenado."""
    pedido_proveedor = session.pop("pedido_proveedor", None)

    if not pedido_proveedor:
        flash("No hay ningún pedido pendiente para generar el PDF.", "warning")
        return redirect(url_for("pedir_proveedor"))

    try:
        buffer, pdf_filename = _crear_pdf_pedido(pedido_proveedor)

        return send_file(
            buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=pdf_filename,
        )

    # W0718 Corregido: Capturamos errores específicos de generación de PDF o I/O
    except (RuntimeError, OSError, ValueError) as e:
        print(f"Error al generar PDF: {e}")
        flash("Error al generar el archivo PDF.", "error")
        return redirect(url_for("pedir_proveedor"))


# --------------------------------------------------------------------------


@app.route("/export_json")
def export_json():
    """Ruta para exportar el inventario actual de la sesión como JSON."""
    productos = session.get("productos")
    if not productos:
        return jsonify({"message": "No hay datos de inventario para exportar."}), 404
    return jsonify(productos)


@app.route("/export_csv")
def export_csv():
    """Ruta para exportar el inventario actual de la sesión como CSV."""
    productos = session.get("productos")
    if not productos:
        flash("No hay datos de inventario para exportar.", "warning")
        return redirect(url_for("upload_csv"))

    try:
        output = io.StringIO()
        if productos:
            df = pd.DataFrame(productos)
            df.to_csv(output, index=False, encoding="utf-8")
        else:
            output.write("Código,Nombre,Cantidad,Demanda,Tiempo entrega(Días),Fecha límite\n")

        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode("utf-8")),
            mimetype="text/csv",
            as_attachment=True,
            download_name="inventario_exportado.csv",
        )

    # W0718 Corregido: Capturamos IOError/OSError para problemas de escritura en memoria/flujo
    except (IOError, OSError) as e:
        print(f"Error al exportar CSV: {e}")
        flash("Error al generar el archivo CSV de exportación.", "error")
        return redirect(url_for("upload_csv"))


# Ejecución principal
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
