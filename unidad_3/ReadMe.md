# ☕ Sistema de Gestión de Inventario - Touken Café

![Python Badge](https://img.shields.io/badge/Language-Python-blue.svg)
![Framework](https://img.shields.io/badge/Framework-Flask-lightgrey.svg)
![Feature](https://img.shields.io/badge/Feature-Inventory_Management-orange.svg)
![Export](https://img.shields.io/badge/Export-CSV%20%7C%20JSON%20%7C%20PDF-blue.svg)
![Status](https://img.shields.io/badge/Status-Educational-green.svg)
![Purpose](https://img.shields.io/badge/Purpose-Café%20Stock%20Control-purple.svg)

Bienvenido al Sistema de Gestión de Inventario para Touken Café, una aplicación web construida con Flask y Python diseñada para optimizar el flujo de inventario, gestionar pedidos internos y generar órdenes de compra a proveedores de manera automatizada.

## 🚀 Características Principales
- **Gestión de Inventario Flexible:**
  - **📤 Carga Masiva:** Importación de inventario mediante archivos CSV.
  - **📝 Creación Manual:** Interfaz para crear inventarios desde cero sin necesidad de archivos externos.
  - **🧹 Limpieza Automática:** Sistema de mantenimiento que elimina archivos temporales antiguos (uploads) automáticamente.
- **Gestión de Stock Inteligente:**
  - **📉 Pedidos Internos:** Actualización de stock en tiempo real.
  - **🧠 Ajuste de Demanda:** Algoritmo simple de "aprendizaje" (factor 0.3) que ajusta la demanda proyectada basándose en los pedidos reales.
- **Gestión de Proveedores:**
  - **🛒 Generación de Pedidos:** Selección de productos para reabastecimiento.
  - **📄 Exportación PDF:** Generación automática de órdenes de compra en formato PDF listas para enviar al proveedor.
- **Exportación de Datos:**
  - 💾 Descarga del estado actual del inventario en formatos JSON y CSV.

## 🛠️ Tecnologías Utilizadas
**Python 3.8+**
**Flask:** Framework web ligero.
**Pandas:** Manipulación y análisis de datos (lectura/escritura de CSV).
**FPDF:** Generación de archivos PDF.

## 📋 Prerrequisitos
Asegúrate de tener instalado Python. Las dependencias necesarias se pueden instalar vía `pip`.
Dependencias (`requirements.txt`)
```
Flask
pandas
fpdf
```
## ⚙️ Instalación y Ejecución
1. **Clonar el repositorio:**
```
git clone https://github.com/WolveJC/ACADE-Prog/tree/main/unidad_3/Flask.git](https://github.com/WolveJC/ACADE-Prog/tree/main/unidad_3/Flask.git)
cd touken-cafe-inventory
```
2. **Crear un entorno virtual (Opcional pero recomendado):**
```
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```
3. **Instalar dependencias:**
```
pip install Flask pandas fpdf
```
4. **Configurar variables de entorno (Opcional):**
Puedes establecer una clave secreta personalizada para la sesión de Flask.
```
export FLASK_SECRET_KEY=""
```
5. **Ejecutar la aplicación:**
```
python app.py
```
6. **Acceder a la web:**
Abre tu navegador y ve a `http://localhost:5000`.

## 📂 Estructura del Proyecto
```
unidad_3/
├── Flask/
│   ├── app.py                # Lógica principal de la aplicación (Controladores y Rutas)
│   ├── uploads/              # Carpeta temporal para archivos CSV (Auto-generada)
│   └── templates/            # Plantillas HTML (Frontend)
│       ├── subir_csv.html
│       ├── crear_inventario.html
│       ├── pedir_stock.html
│       └── pedir_proveedor.html
└── README.md                 # Documentación del proyecto
```
## 📖 Guía de Uso
1. Inicio (Cargar Inventario):
- Sube un archivo .csv con las columnas requeridas: `Código`, `Nombre`, `Cantidad`, `Demanda`, `Tiempo entrega(Días)`, `Fecha límite`.
- O selecciona "Crear Inventario Manualmente" si no tienes un archivo.
2. Pedir Stock (Interno):
- Navega a la sección de pedidos internos.
- Ingresa la cantidad que necesitas retirar del almacén.
- El sistema validará si hay suficiente stock y actualizará la demanda futura automáticamente.
3. Pedir a Proveedor:
- Selecciona los productos que necesitas reabastecer.
- Ingresa cantidad y precio unitario actual.
- Haz clic en "Generar Pedido" para descargar un PDF oficial con el detalle y totales.
4. Exportar:
- Utiliza los enlaces en el pie de página o menú para descargar el estado actual de tu inventario en CSV o JSON.

## 🛡️ Manejo de Errores y Validaciones
La aplicación cuenta con un sistema robusto de manejo de errores:
- Validación estricta de tipos de datos en formularios.
- Manejo de archivos corruptos o vacíos (Pandas ParserError/EmptyDataError).
- Protección contra entradas negativas en precios y cantidades.
- Gestión segura de rutas de archivos (os.path.join).

## 🤝 Contribución
1. Haz un Fork del proyecto.
2. Crea una rama para tu funcionalidad (git checkout -b feature/NuevaFuncionalidad).
3. Commit a tus cambios (git commit -m 'Agregada nueva funcionalidad').
4. Push a la rama (git push origin feature/NuevaFuncionalidad).
5. Abre un Pull Request.

Desarrollado como parte de la Unidad 3: Desarrollo Web con Flask.