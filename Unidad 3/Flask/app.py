from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify,send_file
import os
import pandas as pd
from fpdf import FPDF
import datetime

# Configuración básica de Flask
app = Flask(__name__)
app.secret_key = "secret-key"
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
                            "stock_actual": producto_info.get('Cantidad') # Incluir stock actual para referencia en el PDF                        })

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
        if item['cantidad'] > 0:  # Solo incluir ítems con cantidad mayor que 0
            pdf.cell(0, 5, f"Código: {item['codigo']}", ln=True)
            pdf.cell(0, 5, f"Producto: {item['nombre']}", ln=True)
            pdf.cell(0, 5, f"Cantidad: {item['cantidad']}, Precio: ${item['precio_unitario']:.2f}", ln=True)
            pdf.cell(0, 5, f"Entrega: {item.get('tiempo_entrega', 'N/A')} días, Stock: {item.get('stock_actual', 'N/A')}", ln=True)
            pdf.ln(3)

    pdf_file = f"pedido_proveedor_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(os.path.join(app.config["UPLOAD_FOLDER"], pdf_file))
    flash(f"PDF de pedido al proveedor generado exitosamente. Guardado como {pdf_file} en la carpeta uploads.")
    session.pop('pedido_proveedor', None)
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
