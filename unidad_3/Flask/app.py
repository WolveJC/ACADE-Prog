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
import os
import pandas as pd
from fpdf import FPDF
import datetime
import time
import random
import string
import csv
import io  # Necesario para send_file con CSV generado en memoria

# Configuración básica de Flask
app = Flask(__name__)
app.secret_key = "secret-key"  # ¡Cambia esto por una clave secreta segura en producción!
UPLOAD_FOLDER = "uploads"
# Crear carpeta uploads si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Función para generar código alfanumérico aleatorio
def generar_codigo_aleatorio(longitud=6):
    caracteres = string.ascii_uppercase + string.digits
    return "".join(random.choices(caracteres, k=longitud))


# Función para limpiar archivos antiguos en la carpeta uploads
def limpiar_archivos_antiguos():
    ahora = time.time()
    un_dia_en_segundos = 24 * 3600
    archivos_eliminados = 0
    print("Ejecutando limpieza de archivos antiguos...")

    if os.path.exists(app.config["UPLOAD_FOLDER"]):
        for nombre_archivo in os.listdir(app.config["UPLOAD_FOLDER"]):
            ruta_archivo = os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo)
            try:
                if os.path.isfile(ruta_archivo):
                    timestamp_creacion = os.path.getctime(
                        ruta_archivo
                    )  # Usar getctime o getmtime según preferencia
                    if (ahora - timestamp_creacion) > un_dia_en_segundos:
                        os.remove(ruta_archivo)
                        print(f"Archivo antiguo eliminado: {ruta_archivo}")
                        archivos_eliminados += 1
            except Exception as e:
                print(f"Error al procesar o eliminar {ruta_archivo}: {e}")

    if archivos_eliminados > 0:
        print(f"Se eliminaron {archivos_eliminados} archivos antiguos de la carpeta uploads.")
    else:
        print("No se encontraron archivos antiguos para eliminar en la carpeta uploads.")


# Ejecutar la limpieza al inicio de la aplicación (en contexto)
with app.app_context():
    limpiar_archivos_antiguos()

# ==========================================================================
#                       RUTAS DE LA APLICACIÓN
# ==========================================================================


# Ruta para crear inventario manualmente
@app.route("/crear_inventario", methods=["GET", "POST"])
def crear_inventario():
    if request.method == "POST":
        # Manejar petición JSON enviada por fetch desde el frontend
        if request.is_json:
            data = request.get_json()
            inventario_para_guardar = data.get("inventario")
            if data.get("guardar_csv") and inventario_para_guardar:
                # Generar nombre de archivo único
                nombre_archivo_creado = (
                    f"inventario_creado_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                )
                ruta_archivo_creado = os.path.join(
                    app.config["UPLOAD_FOLDER"], nombre_archivo_creado
                )
                try:
                    # Validar estructura básica (asegurar que es lista de diccionarios)
                    if not isinstance(inventario_para_guardar, list) or not all(
                        isinstance(item, dict) for item in inventario_para_guardar
                    ):
                        raise ValueError("Formato de inventario inválido.")

                    # Obtener encabezados del primer producto (si existe)
                    fieldnames = (
                        inventario_para_guardar[0].keys() if inventario_para_guardar else []
                    )

                    # Escribir el archivo CSV
                    with open(ruta_archivo_creado, "w", newline="", encoding="utf-8") as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(inventario_para_guardar)

                    # Cargar datos en la sesión como si se hubiera subido el archivo
                    session["csv_filepath"] = ruta_archivo_creado
                    df = pd.read_csv(ruta_archivo_creado)
                    # Asegurarse que las columnas esperadas existan, manejar NaNs si es necesario
                    df.fillna("", inplace=True)  # Rellenar NaNs para evitar problemas con JSON
                    session["productos"] = df.to_dict(orient="records")

                    # Limpiar el inventario temporal de la sesión si lo estabas usando
                    session.pop("inventario_creado", None)

                    # Devolver respuesta JSON de éxito para fetch
                    return (
                        jsonify(
                            {
                                "message": f"Inventario creado y guardado como {nombre_archivo_creado}."
                            }
                        ),
                        200,
                    )

                except KeyError as e:
                    print(f"Error de clave al procesar inventario: {e}")
                    return (
                        jsonify(
                            {"message": f"Error en los datos del inventario: falta la clave {e}"}
                        ),
                        400,
                    )
                except ValueError as e:
                    print(f"Error de valor al procesar inventario: {e}")
                    return (
                        jsonify({"message": f"Error en los datos del inventario: {e}"}),
                        400,
                    )
                except Exception as e:
                    print(f"Error al guardar el archivo CSV: {e}")
                    # Devolver respuesta JSON de error para fetch
                    return (
                        jsonify({"message": f"Error interno al guardar el archivo CSV: {e}"}),
                        500,
                    )
            else:
                # Devolver respuesta JSON de error para fetch
                return (
                    jsonify({"message": "Datos inválidos o acción no reconocida."}),
                    400,
                )
        else:
            # Manejar envío de formulario tradicional (si aún se permite)
            # Probablemente ya no necesario para esta acción específica si JS usa fetch
            flash("Método no soportado, use la interfaz interactiva.", "error")
            return redirect(url_for("crear_inventario"))

    # Método GET: Mostrar la página
    # Pasar inventario temporal si se guarda en sesión (opcional si todo es JS)
    inventario_temporal = session.get("inventario_creado", [])
    return render_template("crear_inventario.html", inventario_creado=inventario_temporal)


# Ruta de inicio (para subir CSV y seleccionar tipo de pedido)
@app.route("/", methods=["POST", "GET"])
def upload_csv():
    if request.method == "POST":
        # Verificar si se envió un archivo
        if "file" not in request.files:
            flash("No se encontró el archivo en la petición.")
            # Para fetch, devolver JSON
            if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
                return jsonify({"message": "No se encontró el archivo."}), 400
            return redirect(request.url)

        file = request.files["file"]

        # Verificar si se seleccionó un archivo
        if file.filename == "":
            flash("No se seleccionó ningún archivo.")
            if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
                return jsonify({"message": "No se seleccionó ningún archivo."}), 400
            return redirect(request.url)

        # Verificar extensión y tipo MIME (más seguro)
        if file and file.filename.lower().endswith(".csv") and file.content_type == "text/csv":
            try:
                filename = file.filename  # Considerar usar werkzeug.utils.secure_filename
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)

                # Leer y procesar el CSV
                data = pd.read_csv(filepath)
                # Validación básica de columnas (ajustar según necesidad)
                columnas_esperadas = [
                    "Código",
                    "Nombre",
                    "Cantidad",
                    "Demanda",
                    "Tiempo entrega(Días)",
                    "Fecha límite",
                ]
                if not all(col in data.columns for col in columnas_esperadas):
                    os.remove(filepath)  # Eliminar archivo inválido
                    raise ValueError(
                        f"El CSV debe contener las columnas: {', '.join(columnas_esperadas)}"
                    )

                data.fillna("", inplace=True)  # Manejar NaNs
                json_data = data.to_dict(orient="records")

                # Guardar en sesión
                session["productos"] = json_data
                session["csv_filepath"] = filepath
                print(f"Archivo CSV cargado: {filepath}")

                # Respuesta para fetch
                if (
                    request.accept_mimetypes.accept_json
                    and not request.accept_mimetypes.accept_html
                ):
                    return jsonify({"message": "Archivo CSV cargado con éxito."}), 200
                # Respuesta para envío tradicional
                flash("Archivo CSV de inventario cargado con éxito.")
                return redirect(url_for("upload_csv"))

            except pd.errors.EmptyDataError:
                message = "El archivo CSV está vacío."
                if os.path.exists(filepath):
                    os.remove(filepath)
            except pd.errors.ParserError:
                message = "Error al procesar el archivo CSV. Verifique el formato."
                if os.path.exists(filepath):
                    os.remove(filepath)
            except ValueError as e:
                message = str(e)
            except Exception as e:
                message = f"Ocurrió un error inesperado: {e}"
                if os.path.exists(filepath):
                    os.remove(filepath)  # Intentar eliminar

            print(f"Error al cargar CSV: {message}")
            if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
                return jsonify({"message": message}), 400
            flash(message)
            return redirect(request.url)

        else:
            message = "Por favor, sube un archivo CSV válido (.csv)."
            if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
                return jsonify({"message": message}), 400
            flash(message)
            return redirect(request.url)

    # Método GET: Mostrar la página
    return render_template("subir_csv.html")


# Ruta para pedir stock interno
@app.route("/pedir_stock", methods=["GET", "POST"])
def pedir_stock():
    # Asegurarse de que el inventario esté cargado
    productos = session.get("productos")
    if not productos:
        flash("No hay inventario cargado. Sube o crea un archivo CSV.", "warning")
        return redirect(url_for("upload_csv"))

    if request.method == "POST":
        try:
            pedido_stock = {}
            # Extraer datos del formulario (enviado por fetch o tradicional)
            for key, value in request.form.items():
                if key.startswith("pedido_stock[") and key.endswith("]"):
                    # Extraer código limpiamente
                    codigo_limpio = key[len("pedido_stock[") : -1]
                    try:
                        cantidad_pedida = int(value)
                        if cantidad_pedida > 0:
                            # Validar que el código exista en productos (más seguro)
                            if any(str(p["Código"]) == codigo_limpio for p in productos):
                                pedido_stock[codigo_limpio] = cantidad_pedida
                            else:
                                print(
                                    f"Advertencia: Código de producto no encontrado en pedido_stock: {codigo_limpio}"
                                )
                        elif cantidad_pedida < 0:
                            # Devolver error si se envía cantidad negativa
                            return (
                                jsonify(
                                    {
                                        "message": f"La cantidad para {codigo_limpio} no puede ser negativa."
                                    }
                                ),
                                400,
                            )
                    except ValueError:
                        # Ignorar valores no numéricos o devolver error
                        print(f"Advertencia: Valor no numérico para {codigo_limpio}: {value}")
                        # return jsonify({"message": f"Valor inválido para {codigo_limpio}."}), 400

            if not pedido_stock:
                # Devolver error si no se pidió nada válido
                return (
                    jsonify(
                        {"message": "No se especificó ninguna cantidad válida para el pedido."}
                    ),
                    400,
                )

            productos_actualizados = []
            resultados_pedido_msg = []  # Mensajes para la respuesta
            hubo_cambios = False

            for producto in productos:
                codigo_str = str(producto["Código"])
                if codigo_str in pedido_stock:
                    cantidad_pedida = pedido_stock[codigo_str]
                    stock_actual = int(
                        producto.get("Cantidad", 0)
                    )  # Manejar posible ausencia o no número

                    if cantidad_pedida <= stock_actual:
                        producto["Cantidad"] = stock_actual - cantidad_pedida
                        demanda_actual = int(producto.get("Demanda", 0))

                        # Aproximación: ajustar la demanda
                        factor_aprendizaje = 0.3
                        nueva_demanda = (
                            demanda_actual + (cantidad_pedida - demanda_actual) * factor_aprendizaje
                        )
                        producto["Demanda"] = min(round(nueva_demanda), 10)  # Limitar a 10

                        resultados_pedido_msg.append(
                            f"Pedido de {cantidad_pedida} {producto['Nombre']} OK. Nuevo stock: {producto['Cantidad']}, Nueva demanda: {producto['Demanda']}"
                        )
                        hubo_cambios = True
                    else:
                        resultados_pedido_msg.append(
                            f"Stock insuficiente de {producto['Nombre']} (disp: {stock_actual}) para pedir {cantidad_pedida}."
                        )
                productos_actualizados.append(producto)  # Añadir siempre, modificado o no

            if hubo_cambios:
                # Actualizar sesión y archivo CSV
                session["productos"] = productos_actualizados
                csv_filepath = session.get("csv_filepath")
                if csv_filepath and os.path.exists(csv_filepath):
                    df = pd.DataFrame(productos_actualizados)
                    df.to_csv(csv_filepath, index=False, encoding="utf-8")
                else:
                    print("Advertencia: No se encontró el archivo CSV para actualizar.")
                    # Considerar devolver un error o advertencia al cliente

            # Devolver respuesta JSON para fetch
            return (
                jsonify(
                    {
                        "message": "Proceso de pedido de stock completado.",
                        "detalles": resultados_pedido_msg,
                        "hubo_cambios": hubo_cambios,
                        # Opcional: podrías devolver 'productos_actualizados' si el frontend lo necesita
                    }
                ),
                200,
            )

        except Exception as e:
            print(f"Error en /pedir_stock: {e}")
            return (
                jsonify({"message": f"Error interno al procesar el pedido de stock: {e}"}),
                500,
            )

    # Método GET: Mostrar la página
    return render_template("pedir_stock.html", productos_stock=productos)


# Ruta para pedir al proveedor
@app.route("/pedir_proveedor", methods=["GET", "POST"])
def pedir_proveedor():
    productos = session.get("productos")
    if not productos:
        flash("No hay inventario cargado. Sube o crea un archivo CSV.", "warning")
        return redirect(url_for("upload_csv"))

    if request.method == "POST":
        try:
            pedido_proveedor = []
            errores_validacion = []
            item_count = 0

            # Crear un diccionario para buscar productos por código más eficientemente
            productos_dict = {str(p["Código"]): p for p in productos}

            # Procesar datos del formulario
            codigos_pedidos = set()
            for key, value in request.form.items():
                if key.startswith("pedido_proveedor[") and key.endswith("]"):
                    codigo_limpio = key[len("pedido_proveedor[") : -1]
                    codigos_pedidos.add(codigo_limpio)

            for codigo_limpio in codigos_pedidos:
                cantidad_str = request.form.get(f"pedido_proveedor[{codigo_limpio}]")
                precio_str = request.form.get(f"precio_proveedor[{codigo_limpio}]")

                cantidad_pedida = 0
                precio = 0.0
                error_en_item = False

                # Validar cantidad
                try:
                    cantidad_pedida = int(cantidad_str) if cantidad_str else 0
                    if cantidad_pedida < 0:
                        errores_validacion.append(
                            f"Producto {codigo_limpio}: Cantidad no puede ser negativa."
                        )
                        error_en_item = True
                except (ValueError, TypeError):
                    errores_validacion.append(f"Producto {codigo_limpio}: Cantidad inválida.")
                    error_en_item = True

                # Validar precio solo si la cantidad es > 0
                if cantidad_pedida > 0:
                    item_count += 1
                    try:
                        precio = float(precio_str) if precio_str else 0.0
                        if precio <= 0:
                            errores_validacion.append(
                                f"Producto {codigo_limpio}: Precio debe ser mayor a 0."
                            )
                            error_en_item = True
                    except (ValueError, TypeError):
                        errores_validacion.append(f"Producto {codigo_limpio}: Precio inválido.")
                        error_en_item = True

                # Si no hay errores y cantidad > 0, añadir al pedido
                if not error_en_item and cantidad_pedida > 0:
                    producto_info = productos_dict.get(codigo_limpio)
                    if producto_info:
                        pedido_proveedor.append(
                            {
                                "codigo": producto_info[
                                    "Código"
                                ],  # Usar el tipo original si es necesario
                                "nombre": producto_info["Nombre"],
                                "cantidad": cantidad_pedida,
                                "precio_unitario": precio,
                                # Obtener datos adicionales de forma segura
                                "tiempo_entrega": producto_info.get("Tiempo entrega(Días)", "N/A"),
                                "stock_actual": producto_info.get("Cantidad", "N/A"),
                            }
                        )
                    else:
                        errores_validacion.append(
                            f"Producto con código {codigo_limpio} no encontrado en inventario."
                        )

            if errores_validacion:
                return (
                    jsonify(
                        {
                            "message": "Errores en el formulario.",
                            "errors": errores_validacion,
                        }
                    ),
                    400,
                )

            if item_count == 0:
                return (
                    jsonify({"message": "No se especificó ningún producto válido para el pedido."}),
                    400,
                )

            # Guardar el pedido en la sesión para la generación del PDF
            session["pedido_proveedor"] = pedido_proveedor

            # Devolver éxito para que JS redirija a la generación del PDF
            return (
                jsonify(
                    {
                        "message": "Pedido listo para generar PDF.",
                        "redirect_url": url_for("generar_pdf_proveedor"),
                    }
                ),
                200,
            )

        except Exception as e:
            print(f"Error en /pedir_proveedor: {e}")
            return (
                jsonify({"message": f"Error interno al procesar el pedido al proveedor: {e}"}),
                500,
            )

    # Método GET: Mostrar la página
    return render_template("pedir_proveedor.html", productos_proveedor=productos)


# Ruta para generar PDF de pedido al proveedor
@app.route("/generar_pdf_proveedor", methods=["GET"])
def generar_pdf_proveedor():
    pedido_proveedor = session.get("pedido_proveedor")
    if not pedido_proveedor:
        flash("No hay ningún pedido pendiente para generar el PDF.", "warning")
        return redirect(url_for("pedir_proveedor"))  # Redirigir a la página de pedido

    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)  # Ajustar tamaño para más contenido

        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pdf.set_font("Arial", "B", size=12)
        pdf.cell(0, 10, f"Pedido al Proveedor - Touken Café", ln=True, align="C")
        pdf.set_font("Arial", size=9)
        pdf.cell(0, 5, f"Fecha de Generación: {fecha_hora}", ln=True, align="C")
        pdf.ln(8)

        # Encabezados de la tabla
        pdf.set_font("Arial", "B", size=10)
        col_widths = [25, 75, 25, 30, 35]  # Ajustar anchos de columna
        headers = ["Código", "Producto", "Cantidad", "Precio Unit.", "Precio Total"]
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, border=1, align="C")
        pdf.ln()

        # Contenido de la tabla
        pdf.set_font("Arial", size=9)
        total_pedido = 0
        for item in pedido_proveedor:
            if item["cantidad"] > 0:  # Doble verificación
                precio_total_item = item["cantidad"] * item["precio_unitario"]
                pdf.cell(col_widths[0], 8, str(item["codigo"]), border=1)
                # Usar MultiCell para nombres largos
                x_before = pdf.get_x()
                y_before = pdf.get_y()
                pdf.multi_cell(col_widths[1], 8, item["nombre"], border=1, align="L")
                pdf.set_xy(x_before + col_widths[1], y_before)  # Resetear posición X

                pdf.cell(col_widths[2], 8, str(item["cantidad"]), border=1, align="C")
                pdf.cell(
                    col_widths[3],
                    8,
                    f"${item['precio_unitario']:.2f}",
                    border=1,
                    align="R",
                )
                pdf.cell(col_widths[4], 8, f"${precio_total_item:.2f}", border=1, align="R")
                pdf.ln()  # Asegurar nueva línea después de MultiCell
                total_pedido += precio_total_item

        # Total del pedido
        pdf.ln(5)
        pdf.set_font("Arial", "B", size=10)
        pdf.cell(
            sum(col_widths) - col_widths[-1],
            10,
            "Total del Pedido:",
            border=0,
            align="R",
        )
        pdf.cell(col_widths[-1], 10, f"${total_pedido:.2f}", border=1, align="R")
        pdf.ln()

        # Guardar PDF
        pdf_filename = f"pedido_proveedor_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], pdf_filename)
        pdf.output(filepath)

        # Limpiar pedido de la sesión después de generar el PDF
        session.pop("pedido_proveedor", None)

        flash(
            f"PDF de pedido al proveedor generado: {pdf_filename}. Guardado en 'uploads'.",
            "success",
        )
        # Opcional: Podrías devolver el archivo para descarga directa
        # return send_file(filepath, as_attachment=True, download_name=pdf_filename)

    except Exception as e:
        print(f"Error al generar PDF: {e}")
        flash("Error al generar el archivo PDF.", "error")
        # Limpiar sesión incluso si hay error para evitar reintentos con datos malos
        session.pop("pedido_proveedor", None)

    return redirect(url_for("upload_csv"))  # Redirigir a inicio después de generar/error


# Ruta para exportar inventario como JSON
@app.route("/export_json")
def export_json():
    productos = session.get("productos")
    if not productos:
        return jsonify({"message": "No hay datos de inventario para exportar."}), 404
    return jsonify(productos)


# Ruta para exportar inventario como CSV
@app.route("/export_csv")
def export_csv():
    productos = session.get("productos")
    if not productos:
        flash("No hay datos de inventario para exportar.", "warning")
        return redirect(url_for("upload_csv"))

    try:
        # Generar CSV en memoria para evitar problemas con el archivo original
        output = io.StringIO()
        if productos:
            # Asegurar que todos los dicts tengan las mismas claves y en el mismo orden
            df = pd.DataFrame(productos)
            df.to_csv(output, index=False, encoding="utf-8")
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode("utf-8")),
                mimetype="text/csv",
                as_attachment=True,
                download_name="inventario_exportado.csv",
            )
        else:
            # Devolver CSV vacío si no hay productos
            output.write("")  # Escribir cadena vacía
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode("utf-8")),
                mimetype="text/csv",
                as_attachment=True,
                download_name="inventario_vacio.csv",
            )

    except Exception as e:
        print(f"Error al exportar CSV: {e}")
        flash("Error al generar el archivo CSV de exportación.", "error")
        return redirect(url_for("upload_csv"))


# Ejecución principal
if __name__ == "__main__":
    # debug=True es útil para desarrollo, ¡desactívalo en producción!
    # host='0.0.0.0' permite acceso desde otros dispositivos en la red local
    app.run(debug=True, host="0.0.0.0")
