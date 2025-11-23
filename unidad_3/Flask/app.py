import csv
import datetime
import io
import os
import random
import string
import time
from typing import List, Tuple, Dict

from flask import (
    Flask, render_template, request,
    redirect, url_for, flash,
    session, jsonify, send_file
)
from fpdf import FPDF
import pandas as pd
from pandas.errors import EmptyDataError, ParserError

# ==============================
# Configuración básica
# ==============================
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "secret-key-default-insecure")
UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ==============================
# Utilidades
# ==============================
def generar_codigo_aleatorio(longitud: int = 6) -> str:
    """Genera un código alfanumérico aleatorio."""
    caracteres = string.ascii_uppercase + string.digits
    return "".join(random.choices(caracteres, k=longitud))


def limpiar_archivos_antiguos(dias: int = 1):
    """Elimina archivos antiguos de la carpeta uploads."""
    ahora = time.time()
    segundos_limite = dias * 24 * 3600
    archivos_eliminados = 0
    folder_path = app.config["UPLOAD_FOLDER"]

    if os.path.exists(folder_path):
        for nombre_archivo in os.listdir(folder_path):
            ruta_archivo = os.path.join(folder_path, nombre_archivo)
            try:
                if os.path.isfile(ruta_archivo):
                    timestamp_modificacion = os.path.getmtime(ruta_archivo)
                    if (ahora - timestamp_modificacion) > segundos_limite:
                        os.remove(ruta_archivo)
                        archivos_eliminados += 1
                        print(f"Archivo eliminado: {ruta_archivo}")
            except (OSError, PermissionError) as e:
                print(f"Error al eliminar {ruta_archivo}: {e}")

    print(f"Se eliminaron {archivos_eliminados} archivos antiguos.")


with app.app_context():
    limpiar_archivos_antiguos(dias=1)


def _guardar_inventario_csv(inventario_data: list, filename: str) -> str:
    """Guarda inventario en CSV."""
    ruta_archivo = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if not inventario_data or not all(isinstance(item, dict) for item in inventario_data):
        raise ValueError("Formato de inventario inválido o vacío.")

    fieldnames = inventario_data[0].keys()
    try:
        with open(ruta_archivo, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(inventario_data)
        return ruta_archivo
    except Exception as e:
        raise OSError(f"Error al guardar CSV: {e}") from e


# ==============================
# Subir CSV
# ==============================
@app.route("/", methods=["GET", "POST"])
def upload_csv():
    """Subir CSV de inventario."""
    if request.method == "POST":
        if "file" not in request.files or request.files["file"].filename == "":
            flash("No se seleccionó ningún archivo.", "error")
            return redirect(request.url)

        file = request.files["file"]

        if not file.filename.lower().endswith(".csv"):
            flash("Por favor, sube un archivo CSV válido.", "error")
            return redirect(request.url)

        if file.content_type not in ("text/csv", "application/vnd.ms-excel", "application/octet-stream"):
            # Algunos navegadores usan tipos genéricos al subir .csv
            print(f"Advertencia: content_type no estándar: {file.content_type}")

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        try:
            file.save(filepath)
            data = pd.read_csv(filepath)
            data.fillna("", inplace=True)
            session["productos"] = data.to_dict(orient="records")
            session["csv_filepath"] = filepath
            flash("Archivo CSV cargado con éxito.")
        except EmptyDataError:
            flash("El archivo CSV está vacío.", "error")
        except ParserError:
            flash("Error al procesar el archivo CSV. Verifique el formato.", "error")
        except Exception as e:
            flash(f"Ocurrió un error inesperado al procesar el archivo: {e}", "error")
            # limpiar archivo fallido
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                    print(f"Archivo fallido eliminado: {filepath}")
                except OSError:
                    pass
        return redirect(url_for("upload_csv"))

    return render_template("subir_csv.html")


# ==============================
# Crear inventario manual (JSON → CSV)
# ==============================
@app.route("/crear_inventario", methods=["GET", "POST"])
def crear_inventario():
    """
    Mostrar interfaz o procesar la creación manual del inventario.
    POST espera JSON con {"guardar_csv": true, "inventario": [ ...dicts... ]}
    """
    if request.method == "POST":
        if not request.is_json:
            flash("Método no soportado. Use la interfaz o envíe JSON.", "error")
            return redirect(url_for("crear_inventario"))

        data = request.get_json()
        inventario_para_guardar = data.get("inventario")
        if not data.get("guardar_csv") or not inventario_para_guardar:
            return jsonify({"message": "Datos inválidos o acción no reconocida."}), 400

        nombre_archivo_creado = (
            f"inventario_creado_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        try:
            ruta_archivo_creado = _guardar_inventario_csv(inventario_para_guardar, nombre_archivo_creado)

            # Cargar datos en la sesión
            session["csv_filepath"] = ruta_archivo_creado
            df = pd.read_csv(ruta_archivo_creado)
            df.fillna("", inplace=True)
            session["productos"] = df.to_dict(orient="records")
            session.pop("inventario_creado", None)
            return jsonify({"message": f"Inventario creado y guardado como {nombre_archivo_creado}"}), 200

        except (KeyError, ValueError, OSError) as e:
            return jsonify({"message": f"Error en los datos del inventario: {e}"}), 400

    inventario_temporal = session.get("inventario_creado", [])
    return render_template("crear_inventario.html", inventario_creado=inventario_temporal)


# ==============================
# Pedir stock interno
# ==============================
def _procesar_formulario_stock(form_data: dict) -> Dict[str, int]:
    """
    Extrae y valida el pedido del formulario.
    Returns: Diccionario con {codigo: cantidad}.
    """
    pedido_stock = {}
    for key, value in form_data.items():
        if key.startswith("pedido_stock[") and key.endswith("]"):
            codigo_limpio = key[len("pedido_stock["):-1]
            try:
                cantidad_pedida = int(value)
                if cantidad_pedida > 0:
                    pedido_stock[codigo_limpio] = cantidad_pedida
            except ValueError:
                # Ignorar valores no numéricos
                pass
    return pedido_stock


def _actualizar_stock_inventario(
    productos: List[Dict], pedido_stock: Dict[str, int]
) -> Tuple[List[Dict], List[str], bool]:
    """
    Aplica la lógica de negocio para actualizar el stock.
    """
    resultados_msg = []
    hubo_cambios = False
    factor_aprendizaje = 0.3
    productos_actualizados = [p.copy() for p in productos]

    for producto in productos_actualizados:
        codigo_str = str(producto.get("Código"))
        if codigo_str in pedido_stock:
            cantidad_pedida = pedido_stock[codigo_str]
            stock_actual = int(producto.get("Cantidad") or 0)
            demanda_actual = int(producto.get("Demanda") or 0)

            if cantidad_pedida <= stock_actual:
                producto["Cantidad"] = stock_actual - cantidad_pedida

                # Ajuste de demanda
                nueva_demanda = demanda_actual + (cantidad_pedida - demanda_actual) * factor_aprendizaje
                producto["Demanda"] = min(round(nueva_demanda), 10)

                resultados_msg.append(
                    f"Pedido de {cantidad_pedida} {producto.get('Nombre','')} OK. "
                    f"Nuevo stock: {producto['Cantidad']}"
                )
                hubo_cambios = True
            else:
                resultados_msg.append(
                    f"Stock insuficiente de {producto.get('Nombre','')} "
                    f"(disp: {stock_actual}) para pedir {cantidad_pedida}."
                )

    return productos_actualizados, resultados_msg, hubo_cambios


@app.route("/pedir_stock", methods=["GET", "POST"])
def pedir_stock():
    """
    Ruta para procesar el pedido de stock interno y actualizar el inventario.
    """
    productos = session.get("productos")
    if not productos:
        flash("No hay inventario cargado. Sube o crea un archivo CSV.", "warning")
        return redirect(url_for("upload_csv"))

    if request.method == "POST":
        pedido_stock = _procesar_formulario_stock(request.form)

        if not pedido_stock:
            return jsonify({"message": "No se especificó ninguna cantidad válida."}), 400

        productos_nuevos, mensajes, cambios = _actualizar_stock_inventario(productos, pedido_stock)

        if cambios:
            session["productos"] = productos_nuevos
            csv_path = session.get("csv_filepath")
            if csv_path and os.path.exists(csv_path):
                try:
                    df = pd.DataFrame(productos_nuevos)
                    df.to_csv(csv_path, index=False, encoding="utf-8")
                except (IOError, OSError) as e:
                    print(f"Error al actualizar CSV de inventario: {e}")

        return jsonify({
            "message": "Proceso de pedido de stock completado.",
            "detalles": mensajes,
            "hubo_cambios": cambios,
        }), 200

    return render_template("pedir_stock.html", productos_stock=productos)


# ==============================
# Pedir a proveedor y generar PDF
# ==============================
def _obtener_y_validar_pedido(productos: list, form_data: dict) -> Tuple[List, List]:
    """
    Extrae y valida los datos del pedido al proveedor.
    """
    pedido_proveedor = []
    errores_validacion = []
    productos_dict = {str(p.get("Código")): p for p in productos}

    codigos_pedidos = set()
    for key in form_data.keys():
        if key.startswith("pedido_proveedor[") and key.endswith("]"):
            codigos_pedidos.add(key[len("pedido_proveedor["):-1])

    for codigo in codigos_pedidos:
        cantidad_str = form_data.get(f"pedido_proveedor[{codigo}]")
        precio_str = form_data.get(f"precio_proveedor[{codigo}]")
        producto_info = productos_dict.get(codigo)

        if not producto_info:
            errores_validacion.append(f"Producto {codigo} no encontrado.")
            continue

        # Validar cantidad
        try:
            cantidad = int(cantidad_str) if cantidad_str else 0
            if cantidad < 0:
                errores_validacion.append(f"Producto {codigo}: Cantidad negativa.")
                continue
        except ValueError:
            errores_validacion.append(f"Producto {codigo}: Cantidad inválida.")
            continue

        # Validar precio
        if cantidad > 0:
            try:
                precio = float(precio_str) if precio_str else 0.0
                if precio <= 0:
                    errores_validacion.append(f"Producto {codigo}: Precio debe ser > 0.")
                    continue
            except ValueError:
                errores_validacion.append(f"Producto {codigo}: Precio inválido.")
                continue

            pedido_proveedor.append({
                "codigo": producto_info.get("Código"),
                "nombre": producto_info.get("Nombre"),
                "cantidad": cantidad,
                "precio_unitario": precio,
                "tiempo_entrega": producto_info.get("Tiempo entrega(Días)", "N/A"),
                "stock_actual": producto_info.get("Cantidad", "N/A"),
            })

    return pedido_proveedor, errores_validacion


@app.route("/pedir_proveedor", methods=["GET", "POST"])
def pedir_proveedor():
    """Recopila y procesa los datos del pedido al proveedor."""
    productos = session.get("productos")
    if not productos:
        flash("No hay inventario cargado.", "warning")
        return redirect(url_for("upload_csv"))

    if request.method == "POST":
        try:
            pedido_prov, errores = _obtener_y_validar_pedido(productos, request.form)

            if errores:
                return jsonify({"message": "Errores en el formulario.", "errors": errores}), 400

            if not pedido_prov:
                return jsonify({"message": "No se seleccionaron productos válidos."}), 400

            session["pedido_proveedor"] = pedido_prov
            return jsonify({
                "message": "Pedido listo para generar PDF.",
                "redirect_url": url_for("generar_pdf_proveedor"),
            }), 200

        except (KeyError, ValueError) as e:
            print(f"Error de datos en /pedir_proveedor: {e}")
            return jsonify({"message": f"Error al procesar datos: {e}"}), 400
        except Exception as e:
            print(f"Error inesperado en /pedir_proveedor: {e}")
            return jsonify({"message": "Error interno del servidor."}), 500

    return render_template("pedir_proveedor.html", productos_proveedor=productos)


def _crear_pdf_pedido(pedido_proveedor: list) -> Tuple[bytes, str]:
    """Genera el contenido binario del PDF del pedido al proveedor."""
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
    """Genera el PDF del pedido almacenado."""
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
    except (RuntimeError, OSError, ValueError) as e:
        print(f"Error al generar PDF: {e}")
        flash("Error al generar el archivo PDF.", "error")
        return redirect(url_for("pedir_proveedor"))


# ==============================
# Exportar inventario
# ==============================
@app.route("/export_json")
def export_json():
    """Exporta el inventario actual como JSON."""
    productos = session.get("productos")
    if not productos:
        return jsonify({"message": "No hay datos de inventario para exportar."}), 404
    return jsonify(productos)


@app.route("/export_csv")
def export_csv():
    """Exporta el inventario actual como CSV."""
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
    except (IOError, OSError) as e:
        print(f"Error al exportar CSV: {e}")
        flash("Error al generar el archivo CSV de exportación.", "error")
        return redirect(url_for("upload_csv"))


# ==============================
# Ejecución principal
# ==============================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")