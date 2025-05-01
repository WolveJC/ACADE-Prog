
# Touken Café - Sistema de Gestión de Pedidos

## Descripción General

Touken Café es una aplicación web desarrollada en Python con Flask para la gestión integral de pedidos e inventario. Permite a los usuarios cargar su inventario desde un archivo CSV, realizar pedidos de stock interno, generar órdenes de compra para proveedores en formato PDF, y exportar la información del inventario en formatos JSON y CSV. La aplicación está diseñada para ser intuitiva y facilitar la gestión de suministros del café Touken.

## Funcionalidades Principales

* **Carga de Inventario CSV:** Permite a los usuarios cargar fácilmente su lista de productos, cantidades, demanda, tiempo de entrega y otras especificaciones desde un archivo CSV. Utilizar el script de la unidad 2 de ser necesario.
* **Pedido de Stock Interno:** Una interfaz para realizar pedidos entre las diferentes áreas del café, controlando el stock disponible y ajustando la demanda de los productos. La demanda se recalcula dinámicamente en función de las cantidades pedidas internamente, dentro de un rango de 1 a 10.
* **Pedido a Proveedor:** Permite generar órdenes de compra para proveedores, especificando la cantidad deseada y el precio unitario de cada producto. También muestra la cantidad actual en stock como referencia y el tiempo de entrega estimado desde el proveedor (importado del CSV).
* **Generación de PDF de Pedido a Proveedor:** Las órdenes de compra para proveedores se generan automáticamente en formato PDF, listas para ser enviadas. Solo se incluyen en el PDF los productos con una cantidad de pedido mayor que cero.
* **Exportación de Inventario:** Los datos del inventario actual pueden ser exportados en formatos JSON y CSV para su análisis o integración con otros sistemas.
* **Interfaz de Usuario Intuitiva:** La aplicación cuenta con una interfaz web sencilla y fácil de usar, guiando al usuario a través de los diferentes procesos.

## Tecnologías Utilizadas

* **Python:** Lenguaje de programación principal.
* **Flask:** Framework web ligero para Python.
* **pandas:** Librería para manipulación y análisis de datos (lectura de CSV).
* **fpdf:** Librería para generación de archivos PDF.
* **Werkzeug:** Biblioteca de utilidades para aplicaciones WSGI (utilizada por Flask).
* **Jinja2:** Motor de plantillas para Flask (creación de las páginas HTML dinámicas).

## Requisitos de Instalación

* Python 3.x
* pip (gestor de paquetes de Python)

## Instalación

1.  **Clonar el repositorio (si aplica):**
    ```bash
    git clone [https://github.com/WolveJC/ACADE-Prog.git](https://github.com/WolveJC/ACADE-Prog.git)
    cd ACADE-Prog
    cd Unidad\ 3/Flask
    ```

2.  **Crear un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    venv\Scripts\activate  # En Windows
    ```

3.  **Instalar las dependencias:**
    ```bash
    pip install -r requisitos.txt
    ```

## Estructura de archivos

ACADE-Prog/Unidad 3/Flask
├── uploads/ ```Carpeta donde se guardará el PDF (incluye un CSV de prueba)```
├── static/  ```Carpeta para archivos estáticos```
│   └── css/
│       └── styles.css
│   └── js/
│       └── scripts.js
│   └── img/        ```Opcional: para logos (por implementar)```
├── templates/      ```Carpeta para las plantillas HTML (Jinja2)```
│   ├── base.html
│   ├── subir_csv.html
│   ├── pedir_stock.html
│   └── pedir_proveedor.html
├── app.py          ```App principal de la aplicación```
├── requisitos.txt  ```Archivo con las dependencias del proyecto```
├── README.md       ```Archivo de documentación del proyecto```

## Ejecución de la Aplicación

1.  Asegúrate de estar dentro del entorno virtual (si lo creaste).
2.  Ejecuta la aplicación Flask:
    ```bash
    python app.py
    ```
3.  Abre tu navegador web y ve a `http://127.0.0.1:5000/` (o la dirección que indique la consola).

## Uso

1.  **Subir Archivo CSV:** En la página principal, selecciona y sube tu archivo CSV de inventario. Asegúrate de que el archivo tenga las columnas en el siguiente orden: `Fecha Consulta`, `Código`, `Nombre`, `Demanda`, `Tiempo entrega(Días)`, `Fecha límite`, `Cantidad`.
2.  **Seleccionar Tipo de Pedido:** Después de subir el archivo, aparecerán opciones para realizar un "Pedido de Stock Interno" o un "Pedido al Proveedor".
3.  **Pedido de Stock Interno:** En esta página, puedes especificar la cantidad a pedir del stock disponible para cada producto. La demanda se actualizará automáticamente dentro de un rango de 1 a 10. Los resultados del pedido se mostrarán en la misma página.
4.  **Pedido al Proveedor:** Aquí, verás la cantidad actual en stock de cada producto y podrás ingresar la cantidad que deseas pedir y el precio unitario. El tiempo de entrega desde el proveedor se muestra como referencia.
5.  **Generar PDF de Pedido a Proveedor:** Al enviar el formulario de pedido al proveedor, se generará un archivo PDF con los detalles del pedido (solo para productos con cantidad mayor a 0), que se guardará en la carpeta `uploads` y se te notificará.
6.  **Exportar Inventario:** En varias páginas, encontrarás enlaces para exportar el inventario actual a archivos JSON y CSV.
7.  **Navegación:** Utiliza los enlaces proporcionados en las diferentes páginas para navegar entre las funcionalidades de la aplicación.

## Notas Adicionales 
* La lógica de recálculo de la demanda en el pedido de stock interno es una aproximación simple y puede ser ajustada según las necesidades específicas del negocio.
* La aplicación asume que el archivo CSV de inventario tiene el formato y las columnas esperadas. Cualquier desviación puede causar errores.
* La gestión de errores y la validación de datos podrían ser mejoradas en futuras versiones.
  
 ## Contribuciones
Las contribuciones son bienvenidas. Si deseas mejorar esta aplicación, por favor, sigue los siguientes pasos:
  1. Haz un fork del repositorio.
  2. Crea una rama para tu contribución (`git checkout -b feature/nueva-funcionalidad`).
  3. Realiza tus cambios y commitea (`git commit -am 'Añade nueva funcionalidad'`).
  4. Sube tus cambios al repositorio remoto (`git push origin feature/nueva-funcionalidad`).
  5. Crea un pull request.   
