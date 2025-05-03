from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
import os
import pandas as pd
from fpdf import FPDF
import datetime
import time
import random
import string
import csv

# Configuración básica de Flask
app = Flask(__name__)
app.secret_key = "secret-key"
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Función para generar código alfanumérico aleatorio
def generar_codigo_aleatorio(longitud=6):
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choices(caracteres, k=longitud))

# Función para limpiar archivos antiguos en la carpeta uploads
def limpiar_archivos_antiguos():
    ahora = time.time()
    un_dia_en_segundos = 24 * 3600
    archivos_eliminados = 0

    if os.path.exists(app.config['UPLOAD_FOLDER']):
        for nombre_archivo in os.listdir(app.config['UPLOAD_FOLDER']):
            ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
            try:
                if os.path.isfile(ruta_archivo):
                    timestamp_creacion = os.path.getctime(ruta_archivo)
                    if (ahora - timestamp_creacion) > un_dia_en_segundos:
                        os.remove(ruta_archivo)
                        print(f"Archivo antiguo eliminado: {ruta_archivo}")
                        archivos_eliminados += 1
            except Exception as e:
                print(f"Error al procesar {ruta_archivo}: {e}")

    if archivos_eliminados > 0:
        print(f"Se eliminaron {archivos_eliminados} archivos antiguos de la carpeta uploads.")
    else:
        print("No se encontraron archivos antiguos para eliminar en la carpeta uploads.")

# Ejecutar la limpieza al inicio de la aplicación
with app.app_context():
    limpiar_archivos_antiguos()

# Ruta para crear inventario manualmente
@app.route("/crear_inventario", methods=["GET", "POST"])
def crear_inventario():
    if request.method == "POST":
        if 'agregar_producto' in request.form:
            codigo = request.form.get('codigo')
            if not codigo:
                codigo = generar_codigo_aleatorio()
                productos_en_sesion = session.get('inventario_creado', [])
                while any(p['codigo'] == codigo for p in productos_en_sesion):
                    codigo = generar_codigo_aleatorio()

            nombre = request.form.get('nombre')
            try:
                demanda = int(request.form.get('demanda'))
                if not 1 <= demanda <= 10:
                    flash("La demanda debe ser un valor entre 1 y 10.", 'error')
                    return render_template("crear_inventario.html", inventario_creado=session.get('inventario_creado', []))
            except ValueError:
                flash("Demanda inválida.", 'error')
                return render_template("crear_inventario.html", inventario_creado=session.get('inventario_creado', []))

            try:
                tiempo_entrega = int(request.form.get('tiempo_entrega'))
            except ValueError:
                flash("Tiempo de entrega inválido.", 'error')
                return render_template("crear_inventario.html", inventario_creado=session.get('inventario_creado', []))

            fecha_limite = request.form.get('fecha_limite')
            try:
                datetime.datetime.strptime(fecha_limite, "%Y-%m-%d")
            except ValueError:
                flash("Formato de fecha inválido (YYYY-MM-DD).", 'error')
                return render_template("crear_inventario.html", inventario_creado=session.get('inventario_creado', []))

            try:
                cantidad = int(request.form.get('cantidad'))
            except ValueError:
                flash("Cantidad inválida.", 'error')
                return render_template("crear_inventario.html", inventario_creado=session.get('inventario_creado', []))

            nuevo_producto = {
                "codigo": codigo,
                "nombre": nombre,
                "demanda": demanda,
                "tiempo_entrega": tiempo_entrega,
                "fecha_limite": fecha_limite,
                "cantidad": cantidad
            }

            inventario_creado = session.get('inventario_creado', [])
            inventario_creado.append(nuevo_producto)
            session['inventario_creado'] = inventario_creado
            return redirect(url_for('crear_inventario'))

        elif 'guardar_csv' in request.form:
            inventario_para_guardar = session.get('inventario_creado')
            if inventario_para_guardar:
                nombre_archivo_creado = f"inventario_creado_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                ruta_archivo_creado = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo_creado)
                try:
                    fieldnames_reales = ['codigo', 'nombre', 'demanda', 'tiempo_entrega', 'fecha_limite', 'cantidad']
                    encabezados_csv = ['Código', 'Nombre', 'Demanda', 'Tiempo entrega(Días)', 'Fecha límite', 'Cantidad']
                    with open(ruta_archivo_creado, 'w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_reales)
                        encabezado_dict = dict(zip(fieldnames_reales, encabezados_csv))
                        csvfile.write(','.join(encabezados_csv) + '\n')
                        writer.writerows(inventario_para_guardar)
                    session['csv_filepath'] = ruta_archivo_creado
                    # Simular la subida exitosa del archivo creado
                    data = pd.read_csv(ruta_archivo_creado)
                    session['productos'] = data.to_dict(orient="records")
                    flash(f"Inventario creado y guardado como {nombre_archivo_creado}.", 'success')
                    return redirect(url_for('upload_csv')) # Redirigir a la página principal
                except Exception as e:
                    flash(f"Error al guardar el archivo CSV: {e}", 'error')
                    return render_template("crear_inventario.html", inventario_creado=session.get('inventario_creado', []))
            else:
                flash("No hay productos para guardar.", 'warning')
                return render_template("crear_inventario.html", inventario_creado=session.get('inventario_creado', []))

    return render_template("crear_inventario.html", inventario_creado=session.get('inventario_creado', []))

# Ruta de inicio (para subir CSV y seleccionar tipo de pedido)
@app.route("/", methods=["POST", "GET"])
def upload_csv():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".csv"):
            filename = file.filename
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            data = pd.read_csv(filepath)
            json_data = data.to_dict(orient="records")

            session['productos'] = json_data
            session['csv_filepath'] = filepath
            flash("Archivo CSV de inventario cargado con éxito.")

            # Considera eliminar el CSV aquí si solo lo necesitas para la sesión activa
            # os.remove(filepath)
            # print(f"Archivo CSV eliminado: {filepath}")

            return redirect(url_for("upload_csv")) # Redirigir de nuevo a la página principal
        else:
            flash("Por favor, sube un archivo CSV válido.")
    return render_template("subir_csv.html")

# Ruta para pedir stock interno
@app.route("/pedir_stock", methods=["GET", "POST"])
def pedir_stock():
    productos = session.get('productos')
    if not productos:
        flash("No hay inventario cargado.")
        return redirect(url_for("upload_csv"))

    resultados_pedido = []

    if request.method == "POST":
        pedido_stock = {}
        for codigo, cantidad in request.form.items():
            if codigo.startswith("pedido_stock["):
                codigo_limpio = codigo[len("pedido_stock["):-1]
                cantidad_pedida = int(cantidad)
                if cantidad_pedida > 0:
                    pedido_stock[codigo_limpio] = cantidad_pedida

        if pedido_stock:
            productos_actualizados = []
            for producto in productos:
                codigo = str(producto['Código'])
                if codigo in pedido_stock:
                    cantidad_pedida = pedido_stock[codigo]
                    if cantidad_pedida <= producto['Cantidad']:
                        producto['Cantidad'] -= cantidad_pedida
                        demanda_actual = producto['Demanda']

                        # Aproximación: ajustar la demanda hacia la cantidad pedida
                        factor_aprendizaje = 0.3
                        nueva_demanda = demanda_actual + (cantidad_pedida - demanda_actual) * factor_aprendizaje
                        producto['Demanda'] = min(round(nueva_demanda), 10)

                        resultados_pedido.append(f"Pedido de {cantidad_pedida} {producto['Nombre']} registrado. Nuevo stock: {producto['Cantidad']}, Nueva demanda: {producto['Demanda']}")
                    else:
                        resultados_pedido.append(f"No hay suficiente stock de {producto['Nombre']} (disponible: {producto['Cantidad']}) para pedir {cantidad_pedida}.")
                productos_actualizados.append(producto)

            session['productos'] = productos_actualizados
            df = pd.DataFrame(productos_actualizados)
            df.to_csv(session.get('csv_filepath'), index=False)
            for resultado in resultados_pedido:
                flash(resultado)
            return redirect(url_for("pedir_stock"))
        else:
            flash("No se especificó ninguna cantidad para el pedido de stock.")

    return render_template("pedir_stock.html", productos_stock=productos)

# Ruta para pedir al proveedor
@app.route("/pedir_proveedor", methods=["GET", "POST"])
def pedir_proveedor():
    productos = session.get('productos')
    if not productos:
        flash("No hay inventario cargado.")
        return redirect(url_for("upload_csv"))

    if request.method == "POST":
        pedido_proveedor = []
        for codigo, cantidad in request.form.items():
            if codigo.startswith("pedido_proveedor["):
                codigo_limpio = codigo[len("pedido_proveedor["):-1]
                cantidad_pedida = int(cantidad)
                precio_str = request.form.get(f"precio_proveedor[{codigo_limpio}]")
                precio = 0.0

                if precio_str:
                    try:
                        precio = float(precio_str)
                    except ValueError:
                        flash(f"Por favor, ingrese un precio válido para el producto con código {codigo_limpio}.")
                        return render_template("pedir_proveedor.html", productos_proveedor=productos)

                if cantidad_pedida > 0 and precio > 0:
                    producto_info = next((p for p in productos if str(p['Código']) == codigo_limpio), None)
                    if producto_info:
                        pedido_proveedor.append({
                            "codigo": producto_info['Código'],
                            "nombre": producto_info['Nombre'],
                            "cantidad": cantidad_pedida,
                            "precio_unitario": precio,
                            "tiempo_entrega": producto_info.get('Tiempo entrega(Días)'),
                            "stock_actual": producto_info.get('Cantidad')
                        })

        if pedido_proveedor:
            session['pedido_proveedor'] = pedido_proveedor
            return redirect(url_for("generar_pdf_proveedor"))
        else:
            flash("No se especificó ninguna cantidad o precio válido para el pedido al proveedor.")

    return render_template("pedir_proveedor.html", productos_proveedor=productos)

# Ruta para generar PDF de pedido al proveedor
@app.route("/generar_pdf_proveedor", methods=["GET"])
def generar_pdf_proveedor():
    pedido_proveedor = session.get('pedido_proveedor')
    if not pedido_proveedor:
        flash("No hay ningún pedido para generar el PDF.")
        return redirect(url_for("pedir_proveedor"))

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 5, f"Pedido al Proveedor - Touken Café ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})", ln=True, align="C")
    pdf.ln(5)

    for item in pedido_proveedor:
        if item['cantidad'] > 0:
            pdf.cell(0, 5, f"Código: {item['codigo']}", ln=True)
            pdf.cell(0, 5, f"Producto: {item['nombre']}", ln=True)
            pdf.cell(0, 5, f"Cantidad: {item['cantidad']}, Precio: ${item['precio_unitario']:.2f}", ln=True)
            pdf.cell(0, 5, f"Entrega: {item.get('tiempo_entrega', 'N/A')} días, Stock: {item.get('stock_actual', 'N/A')}", ln=True)
            pdf.ln(3)

    pdf_file = f"pedido_proveedor_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], pdf_file)
    pdf.output(filepath)
    flash(f"PDF de pedido al proveedor generado exitosamente. Guardado como {pdf_file} en la carpeta uploads.")
    session.pop('pedido_proveedor', None)

    # Considera eliminar el PDF aquí si solo lo necesitas para la sesión activa
    # os.remove(filepath)
    # print(f"Archivo PDF eliminado: {filepath}")

    return redirect(url_for("upload_csv"))

# Ruta para exportar inventario como JSON
@app.route("/export_json")
def export_json():
    productos = session.get('productos')
    if not productos:
        flash("No hay datos de inventario para exportar. Por favor, sube un archivo CSV.")
        return redirect(url_for("upload_csv"))
    return jsonify(productos)

# Ruta para exportar inventario como CSV
@app.route("/export_csv")
def export_csv():
    csv_filepath = session.get('csv_filepath')
    if not csv_filepath:
        flash("No hay datos de inventario para exportar. Por favor, sube un archivo CSV.")
        return redirect(url_for("upload_csv"))
    return send_file(csv_filepath, as_attachment=True, download_name="inventario_exportado.csv")

# Ejecución
if __name__ == "__main__":
    app.run(debug=True)
