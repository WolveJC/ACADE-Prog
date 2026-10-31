# ☕ Sistema de Gestión de Inventario - Touken Café

![Python Badge](https://img.shields.io/badge/Language-Python-blue.svg)
![Framework](https://img.shields.io/badge/Framework-Flask-lightgrey.svg)
![Feature](https://img.shields.io/badge/Feature-Inventory_Management-orange.svg)
![Export](https://img.shields.io/badge/Export-CSV%20%7C%20JSON%20%7C%20PDF-blue.svg)
![Status](https://img.shields.io/badge/Status-Educational-green.svg)
![Purpose](https://img.shields.io/badge/Purpose-Café%20Stock%20Control-purple.svg)

Aplicación web (Flask + Python) para controlar el inventario de un café. Lleva el stock por **lotes con fecha de caducidad**, registra lo que se vende, lo que llega y lo que se desecha, **mide la demanda real** a partir de ese historial y **avisa al gerente de qué productos requieren su atención**: lo que está por vencer, lo que no tiene fecha de caducidad, lo que hay que reponer y lo que se está volviendo popular. Genera además los pedidos a proveedor en PDF.

> **Idea central:** el CSV es solo una *plantilla inicial*. Una vez cargado, el inventario se gestiona desde la propia web (agregar, editar y quitar productos, registrar retiradas, recepciones y mermas) sin volver a subir archivos.

## 📑 Contenido

1. [Características](#-características)
2. [Conceptos clave](#-conceptos-clave)
3. [Tecnologías](#️-tecnologías-utilizadas)
4. [Instalación y ejecución](#️-instalación-y-ejecución)
5. [Guía de uso](#-guía-de-uso)
6. [Formato de los archivos CSV](#-formato-de-los-archivos-csv)
7. [Avisos y reglas de negocio](#-avisos-y-reglas-de-negocio)
8. [Configuración](#️-configuración)
9. [Datos y almacenamiento](#-datos-y-almacenamiento)
10. [Estructura del proyecto](#-estructura-del-proyecto)
11. [Pruebas](#-pruebas)
12. [Limitaciones conocidas](#️-limitaciones-conocidas)
13. [Mejoras futuras](#-mejoras-futuras)
14. [Contribución](#-contribución)

## 🚀 Características

- **Gestión de productos**
  - 📤 **Carga inicial por CSV:** una plantilla para empezar. Cargar un CSV **reemplaza** el inventario actual (el historial de movimientos se conserva).
  - 📝 **Productos desde la web:** agregar, editar o quitar un producto **sin borrar el resto del inventario ni el historial**. Funciona incluso sin haber cargado nunca un CSV.
- **Lotes y caducidad**
  - 📦 Cada producto tiene uno o varios **lotes** (unidades que comparten fecha de caducidad). Se muestra siempre la fecha del lote que caduca antes.
  - 🔁 Las ventas salen primero del lote que caduca antes (**FEFO**: el primero en caducar es el primero en salir).
  - 🗑️ **Descarte automático:** cuando un lote pasa su fecha límite, el sistema lo retira solo y lo registra como merma por vencimiento.
  - ⚠️ Aviso permanente cuando hay mercancía **sin fecha de caducidad**.
- **Movimientos de stock** (todos quedan en el historial)
  - 📉 **Pedido de stock:** retirada por venta o consumo, con fecha y marca opcional de *evento especial*.
  - 📥 **Recepción:** mercancía que llega; cada entrada forma un lote con su fecha.
  - 🧺 **Mermas:** mercancía dañada, rota o descartada por otro motivo, lote a lote.
- **Demanda real y avisos**
  - 📈 Consumo diario, tendencia (en alza / en baja), ranking de popularidad y mermas por producto.
  - 🔔 Avisos: por vencer, sin fecha, sin stock, **reponer** (con cantidad sugerida) y **en alza**.
- **Proveedores**
  - 🛒 Pedido con cantidades y precios, y **PDF** listo para imprimir o enviar.
- **Exportación**
  - 💾 Inventario en **CSV** y **JSON**, e historial de movimientos en **CSV**.

## 🧠 Conceptos clave

| Concepto | Qué significa |
|---|---|
| **Lote** | Grupo de unidades que comparten la misma fecha de caducidad (normalmente porque llegaron juntas). El usuario solo ve fechas y unidades, no códigos de lote. Dos lotes con la misma fecha son uno solo. |
| **Fecha límite** | El **último día para vender** el producto. Ese día todavía se puede vender; el lote se considera vencido al día siguiente. |
| **Salida (venta)** | Mercancía que sale del stock porque se vende o se usa (una receta, por ejemplo). **Es la única que cuenta como demanda.** |
| **Entrada (recepción)** | Mercancía que llega. Queda en el historial pero no es demanda. |
| **Merma** | Mercancía que se desecha (vencida, dañada, rota...). Baja el stock, queda en el historial con su motivo y **no cuenta como demanda**: nadie la quiso comprar. |
| **Evento** | Una salida excepcional (una fiesta, un pedido temático). Se guarda, pero **no cuenta** para el consumo habitual ni para las tendencias, para que no distorsione. |
| **Consumo diario** | Unidades vendidas por día, calculadas del historial reciente (sin eventos). |

## 🛠️ Tecnologías Utilizadas

- **Python 3.9 o superior** (probado con 3.9 y 3.12)
- **Flask** 3.0 o superior: framework web ligero.
- **pandas** 2.2.3 o superior: lectura y escritura de CSV.
- **fpdf2** 2.7.6 o superior: generación de PDF (con la fuente DejaVu Sans incluida en `fonts/`, para tildes y caracteres especiales).
- **Bootstrap 5.3.8:** estilos y componentes, **incluido localmente** en `static/vendor/` (la aplicación funciona sin internet).
- **pytest:** pruebas (solo para desarrollo).

## ⚙️ Instalación y ejecución

1. **Obtener el proyecto:**
   ```bash
   git clone https://github.com/WolveJC/ACADE-Prog.git
   cd ACADE-Prog/unidad_3/Flask
   ```
2. **Crear un entorno virtual** (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate        # En Windows: venv\Scripts\activate
   ```
3. **Instalar las dependencias** (el archivo se llama `requisitos.txt`):
   ```bash
   pip install -r requisitos.txt
   ```
4. **Ejecutar la aplicación:**
   ```bash
   python app.py
   ```
5. **Abrir el navegador** en `http://localhost:5000`.

Por seguridad, la aplicación arranca **sin modo debug** y escuchando **solo en tu equipo** (`127.0.0.1`). Para desarrollo:

```bash
FLASK_DEBUG=1 python app.py                  # recarga automática y mensajes de depuración
FLASK_HOST=0.0.0.0 PORT=8080 python app.py   # accesible desde la red local
```

> En Windows (PowerShell) las variables se definen antes: `$env:FLASK_DEBUG="1"; python app.py`.

> El servidor de Flask es de **desarrollo**. No está pensado para exponerse a internet (no tiene usuarios ni contraseñas); ver [Limitaciones conocidas](#️-limitaciones-conocidas).

## 📖 Guía de uso

El menú superior da acceso a todas las pantallas:

| Pantalla | Dirección | Para qué sirve |
|---|---|---|
| **Cargar CSV** | `/` | Cargar la plantilla inicial. Con inventario cargado muestra un resumen de avisos y accesos rápidos. |
| **Productos** | `/productos` | Agregar, editar o quitar productos y corregir sus lotes. |
| **Pedido de stock** | `/pedir_stock` | Registrar lo que se vende o se consume. |
| **Pedido al proveedor** | `/pedir_proveedor` | Preparar el pedido y descargar el PDF. |
| **Recepción** | `/recepcion` | Registrar la mercancía que llega. |
| **Mermas** | `/mermas` | Dar de baja mercancía dañada, rota o descartada. |
| **Demanda** | `/demanda` | Consumo, tendencias, ranking e historial de movimientos. |
| **Exportar** | `/export_csv`, `/export_json`, `/export_movimientos` | Descargar inventario (CSV/JSON) e historial (CSV). |

### Flujo recomendado

1. **Empezar.** Sube un CSV con tu inventario (ver [formato](#-formato-de-los-archivos-csv)) o agrega los productos uno a uno en **Productos**. Un solo CSV basta: a partir de ahí todo se hace desde la web.
2. **Vender o consumir** en **Pedido de stock**: indica la cantidad de cada producto. Opcionalmente cambia la fecha de la retirada (si la registras después) o marca *evento especial*. Cada línea sale del lote que caduca antes.
3. **Recibir mercancía** en **Recepción**: indica la cantidad y la **fecha límite del lote**. Puedes dejarla vacía (azúcar, sal...), pero el sistema te lo seguirá avisando.
4. **Desechar** en **Mermas** lo que se rompa o dañe: elige el lote, la cantidad y el motivo. Lo que llegue a su fecha límite lo descarta el sistema por ti.
5. **Pedir al proveedor** en **Pedido al proveedor**: la pantalla muestra el consumo, el estado de cada producto y una cantidad sugerida. El PDF se genera al enviar. *Ojo:* el pedido **no** modifica el stock; cuando la mercancía llegue, regístrala en **Recepción**.
6. **Revisar la demanda** en **Demanda**: qué se vende más, qué sube o baja, cuánto se pierde en mermas.

### Qué significa cada aviso

| Aviso | Significado |
|---|---|
| 🟡 **Vence en N d · X u.** / **Vence hoy** | El lote vigente que caduca antes vence en 7 días o menos; `X u.` son sus unidades. Ese día todavía se puede vender. |
| 🔴 **Vencido · X u.** | Hay unidades de un lote ya vencido. Solo se ve si el descarte automático está desactivado: normalmente el sistema lo retira antes de mostrarlo. |
| ⚪ **Sin fecha · X u.** | Hay unidades sin fecha de caducidad registrada. Se pueden registrar igualmente, pero el aviso no desaparece hasta indicar la fecha. |
| ⚫ **Sin stock** | No quedan unidades (y el producto tiene demanda o aún no se sabe). |
| 🔵 **Reponer · sugerido N** | El stock vigente no alcanza para cubrir el consumo durante el tiempo de entrega; `N` es lo que falta. |
| 🟢 **En alza +X %** | Su consumo reciente supera claramente al del periodo anterior: conviene anticipar la compra. |
| **OK · sin historial** | Sin alertas de fecha, pero aún no hay historial suficiente para evaluar la reposición. |

Cuando el sistema retira lotes vencidos por su cuenta, lo avisa en pantalla con el detalle (qué producto, cuántas unidades y qué fecha vencieron).

## 📄 Formato de los archivos CSV

### Inventario (plantilla inicial)

Columnas obligatorias: `Código`, `Nombre`, `Cantidad`, `Tiempo entrega(Días)` y `Fecha límite` (formato `YYYY-MM-DD`, el último día para vender; puede quedar vacía). Se ignoran las columnas adicionales y se aceptan los separadores coma, punto y coma y tabulador, en UTF-8 (con o sin BOM) o Latin-1 (típico de Excel en Windows). Tamaño máximo: 2 MB.

```csv
Código,Nombre,Cantidad,Tiempo entrega(Días),Fecha límite
1,Manzana,15,3,2027-06-30
2,Banana,12,5,2027-06-15
2,Banana,20,5,2027-07-10
5,Azúcar,40,7,
```

- **Varios lotes:** repite el código en varias filas, una por fecha de caducidad (aquí, la Banana tiene dos lotes). Todas las filas con el mismo código deben tener el mismo `Nombre` y el mismo `Tiempo entrega(Días)`; las de la misma fecha se suman.
- **Sin fecha:** el Azúcar se carga igualmente, pero el sistema lo avisará.
- **Cantidad 0:** el producto existe sin stock.
- **⚠️ Usa fechas futuras.** Un lote con fecha ya pasada se descarta automáticamente en cuanto se carga. Las fechas del archivo de ejemplo (`ejemplos/inventario_ejemplo.csv`) son de 2027: ajústalas cuando pasen.
- **Cargar un CSV reemplaza** el inventario anterior; el historial se conserva.
- **Exportar** genera este mismo formato (una fila por lote), por lo que el archivo exportado se puede volver a cargar.

### Historial de movimientos

Para importar movimientos anteriores (en **Demanda → Importar historial**) o revisarlos al exportar. Obligatorias: `fecha`, `codigo`, `cantidad`. Opcionales: `tipo`, `evento`, `motivo`.

```csv
fecha,codigo,cantidad,tipo,evento,motivo
2026-06-01,1,4,salida,0,
2026-06-02,1,30,salida,1,
2026-06-03,1,50,entrada,0,
2026-06-04,2,6,merma,0,vencido
```

| Columna | Valores |
|---|---|
| `fecha` | `YYYY-MM-DD`, no futura. |
| `codigo` | Debe existir en el inventario actual. |
| `cantidad` | Entero mayor que 0. |
| `tipo` | `salida` (por defecto), `entrada` o `merma`. |
| `evento` | `1`/`0` (también sí/no). Solo para salidas: marca una retirada excepcional. |
| `motivo` | Solo para mermas: `vencido`, `danado` u `otro` (por defecto). |

> **Importar reemplaza el historial actual** (no se duplican filas) y **no modifica el stock**. Para añadir filas: exporta primero, completa el archivo e impórtalo. Si vas a importar un historial, hazlo **antes de empezar a usar la aplicación**, porque también sustituye los descartes automáticos registrados hasta ese momento.

## 🔔 Avisos y reglas de negocio

**Vencimiento (por lote).** Un lote está vencido si su fecha límite es anterior a hoy. El aviso de "por vencer" salta cuando el lote vigente más próximo vence en 7 días o menos. El producto muestra siempre la fecha del lote que caduca antes, aunque haya otros con fechas más lejanas, para que se sepa qué atender primero.

**Descarte automático.** Cada vez que se usa la aplicación, los lotes vencidos se quitan del stock y se registran como mermas por vencimiento (motivo `vencido`, con la fecha del día en que el sistema los retira). No hay una tarea en segundo plano: si nadie abre la aplicación durante varios días, el descarte se registra en el primer uso posterior. Se puede desactivar (ver [Configuración](#️-configuración)).

**Consumo diario.** Unidades vendidas (salidas, sin eventos) en los últimos 14 días, divididas entre 14. Si el historial es más corto, entre los días que haya. Con menos de **7 días de historial no se calcula** nada, para no inventar cifras: en ese caso solo se avisa de los productos sin stock.

**Reposición.** Se necesita `consumo diario × (tiempo de entrega + 1 día de colchón)`. Si el stock vigente (sin contar lo vencido) es menor, el aviso es **Reponer** y la cantidad sugerida es lo que falta (redondeada hacia arriba).

**Tendencia.** Compara la última semana con la anterior. Hay **alza** o **baja** si el cambio es de al menos un 30 %. Hace falta una ventana completa de 14 días de historial y un mínimo de 5 unidades, para no reaccionar al ruido (pasar de 1 a 2 unidades no es una tendencia).

**Ranking.** Productos ordenados por unidades vendidas en la ventana (los eventos no cuentan).

**Qué NO es demanda:** las mermas, las entradas y las salidas marcadas como evento. Registrar mercancía vencida como una venta inflaría la demanda; por eso existe Mermas.

## ⚙️ Configuración

Los valores por defecto están en `config.py` (clase `Config`):

| Ajuste | Por defecto | Qué hace |
|---|---|---|
| `DESCARTE_AUTOMATICO_VENCIDOS` | `True` | Retira solos los lotes vencidos. `False` para descartarlos a mano en Mermas. |
| `DIAS_AVISO_VENCIMIENTO` | `7` | Días de antelación para el aviso "por vencer". |
| `VENTANA_DEMANDA_DIAS` | `14` | Días que se promedian para el consumo diario. |
| `MIN_DIAS_HISTORIAL` | `7` | Historial mínimo para calcular consumo. |
| `DIAS_SEGURIDAD` | `1` | Colchón sobre el tiempo de entrega al decidir reponer. |
| `DIAS_RETENCION` | `365` | Días sin uso tras los que se borran los datos de un inventario. |
| `MAX_CONTENT_LENGTH` | `2 MB` | Tamaño máximo de un archivo subido. |

Variables de entorno:

| Variable | Qué hace |
|---|---|
| `FLASK_SECRET_KEY` | Clave secreta de las sesiones. Si no se define, se genera una aleatoria y se guarda en `Flask/.secret_key` (no la subas al repositorio). |
| `TOUKEN_DATA_DIR` | Carpeta donde se guardan los datos (por defecto, `Flask/uploads/`). |
| `FLASK_DEBUG` | `1` activa el modo debug. Por defecto está apagado. |
| `FLASK_HOST` / `PORT` | Dirección y puerto (por defecto `127.0.0.1` y `5000`). |

## 💾 Datos y almacenamiento

Los datos se guardan en archivos dentro de `Flask/uploads/`, identificados por un código aleatorio por navegador:

| Archivo | Contenido |
|---|---|
| `<id>.csv` | El inventario (una fila por lote). |
| `<id>.movimientos.csv` | El historial de movimientos. |
| `<id>.pedido.json` | El pedido a proveedor pendiente de descargar. |

La cookie de sesión guarda **solo ese código** (no los datos), por lo que el tamaño del inventario no está limitado por la cookie, y dura un año. Cada uso renueva el plazo de conservación (365 días); pasado ese tiempo sin tocarlos, los archivos se eliminan. Las escrituras son atómicas y los nombres de archivo nunca vienen del usuario.

## 📂 Estructura del proyecto

```
unidad_3/
├── ReadMe.md
├── .gitignore
└── Flask/
    ├── app.py                    # Crea la aplicación y registra los blueprints
    ├── config.py                 # Configuración (valores por defecto y variables de entorno)
    ├── requisitos.txt            # Dependencias de la aplicación
    ├── requisitos-dev.txt        # + pytest, para ejecutar las pruebas
    ├── services/                 # Lógica de negocio pura (sin Flask, fácil de probar)
    │   ├── inventario.py         #   Validación, lectura de CSV, retiradas, recepciones y mermas
    │   ├── lotes.py              #   Lotes: orden por caducidad, FEFO, descarte de vencidos
    │   ├── productos.py          #   Agregar, editar y quitar productos
    │   ├── movimientos.py        #   Historial: validación y formato CSV
    │   ├── demanda.py            #   Consumo diario, tendencia y ranking
    │   ├── alertas.py            #   Avisos: vencimiento, sin fecha, reposición, alza
    │   ├── almacenamiento.py     #   Lectura y escritura de archivos en disco
    │   └── pdf.py                #   PDF del pedido a proveedor
    ├── routes/                   # Controladores (blueprints de Flask)
    │   ├── inventario.py         #   Carga de CSV
    │   ├── productos.py          #   Gestión de productos
    │   ├── pedidos.py            #   Pedido de stock y pedido a proveedor (PDF)
    │   ├── recepcion.py          #   Recepción de mercancía
    │   ├── mermas.py             #   Mermas
    │   ├── movimientos.py        #   Demanda e historial
    │   ├── exportar.py           #   Exportación CSV/JSON
    │   └── comun.py              #   Utilidades compartidas y descarte automático
    ├── templates/                # Plantillas HTML (Jinja2); las que empiezan por "_" son parciales
    ├── static/
    │   ├── css/styles.css        #   Estilos propios (tema y zona de arrastrar y soltar)
    │   ├── js/script.js          #   Interacción: subida de CSV, validaciones y avisos
    │   └── vendor/bootstrap/     #   Bootstrap 5.3.8 local
    ├── fonts/                    # DejaVu Sans para el PDF (con su licencia)
    ├── ejemplos/                 # Inventario de ejemplo y generador de historial de prueba
    ├── tests/                    # Pruebas automatizadas
    └── uploads/                  # Datos de ejecución (se genera sola; no se versiona)
```

Para probar la pantalla de **Demanda** sin esperar semanas de uso real, genera un historial de ejemplo y súbelo en **Demanda → Importar historial** (sirve para los códigos 1 a 4 de `inventario_ejemplo.csv`):

```bash
python ejemplos/generar_movimientos.py            # escribe ejemplos/movimientos_demo.csv
python ejemplos/generar_movimientos.py -d 45      # con 45 días de historial
```

## 🧪 Pruebas

```bash
pip install -r requisitos-dev.txt
pytest
```

Se ejecutan desde la carpeta `Flask/` y no necesitan conexión a internet. Hay unas 300 pruebas: reglas de negocio (lotes, avisos, demanda), validaciones, rutas, exportaciones y PDF. Las versiones indicadas arriba son las que se han probado: los mínimos (Python 3.9, Flask 3.0, fpdf2 2.7.6, pandas 2.2.3) y las más recientes (Python 3.12, Flask 3.1, pandas 3.x).

## ⚠️ Limitaciones conocidas

- **El inventario está ligado al navegador** (a su cookie). No hay usuarios ni contraseñas: otro navegador u otro dispositivo no ve el inventario, y borrar las cookies hace perder el acceso (los archivos siguen en disco hasta que expire la retención). Tampoco debe exponerse a internet.
- **Datos en archivos**, no en una base de datos. Pensado para un negocio pequeño, no para mucho volumen ni uso simultáneo.
- **Un inventario por navegador.** Cargar un CSV lo reemplaza (el historial se conserva).
- **Importar un historial lo reemplaza entero**, incluidos los descartes automáticos recientes.
- **Editar los lotes en Productos corrige cantidades y fechas sin registrar un movimiento.** Para que algo quede en el historial y cuente bien en la demanda, usa Pedido de stock, Recepción o Mermas.
- **Los pedidos al proveedor no se rastrean.** El aviso *Reponer* sigue activo hasta que se registra la recepción, aunque el pedido ya esté hecho.
- **Las entradas se registran a mano.** El sistema no sabe que llegó mercancía hasta que se anota en Recepción.
- **La demanda con stock en cero se subestima:** las ventas que no se pudieron hacer por falta de producto no quedan registradas.
- **El descarte automático ocurre al usar la aplicación**, no en segundo plano.
- **El historial no guarda de qué lote salió cada movimiento**, solo el producto, la cantidad y el tipo.
- **Las fechas de ejemplo caducan.** Las del archivo de ejemplo son de 2027.

## 🔮 Mejoras futuras

### Acordadas

#### 1. Marcar un producto como "no caduca"

Hoy el aviso **Sin fecha** es permanente para cualquier producto con unidades sin fecha. Es lo buscado para no olvidar una fecha, pero resulta ruidoso en productos que nunca caducan en la práctica (azúcar, sal, miel, alcohol).

- **Propuesta simple:** un atributo del producto, con una casilla *No caduca* en **Productos**, y una columna opcional en el CSV (por defecto, sí caduca). Un producto marcado dejaría de avisar de la falta de fecha y sus lotes sin fecha serían normales. Sin marcar, el aviso se mantiene tal como ahora.
- **A investigar más adelante:** que el sistema **aprenda o sugiera** qué productos no caducan, ya que suelen ser casos constantes. Por ejemplo, proponer la marca cuando un producto se ha recibido varias veces sin fecha, o apoyarse en una lista de productos habituales. Convendría que fuera una **sugerencia que el usuario confirma**, no una decisión silenciosa: marcar por error un perecedero como "no caduca" apagaría justo el aviso que evita pérdidas.

#### 2. Avisar de las unidades que no se venderán antes de vencer

Es lo que más ayudaría a no perder mercancía, y encaja de forma natural sobre los lotes: un aviso del tipo **"estas 40 unidades no se venderán antes de vencer"**, para que el gerente actúe a tiempo (bajar precios, combos, promociones...). *Cómo vender lo que está en riesgo queda fuera del alcance del software: este solo informa.*

**Cómo funcionaría.** Con el consumo diario real (el mismo que ya se calcula para reponer) y los lotes ordenados por caducidad, se simula la venta día a día y se estima cuántas unidades de cada lote quedarían sin vender al llegar su fecha límite. Ejemplo: un lote de 40 unidades que vence en 9 días (hoy y 9 días más para vender, es decir, 10 días) con un consumo de 2 unidades por día venderá unas 20; las otras **20 unidades están en riesgo**. Con varios lotes, las ventas salen primero del que caduca antes, por lo que se calcula lote a lote.

**Dónde se mostraría.** Una insignia *En riesgo · N u.* junto a los demás avisos, un conteo en el resumen de avisos y una columna en **Demanda**.

**Decisiones por resolver:**
- Qué consumo usar: el promedio de 14 días o uno ajustado según la tendencia (si un producto está en alza o en baja, el promedio engaña).
- Qué hacer sin historial suficiente: la regla actual es no inventar cifras, así que no habría aviso.
- Cómo tratar un producto sin ventas con historial suficiente (¿todo el lote está en riesgo?) y los lotes sin fecha (no se pueden evaluar).
- Si conviene un margen, por ejemplo para no avisar por 1 o 2 unidades.

**Piezas afectadas (previsión):** una función pura nueva sobre lotes y consumo (con pruebas), `services/alertas.py`, `templates/_alertas.html` y la página de Demanda.

### Ideas (sin priorizar)

- **Pedidos en camino:** registrar los pedidos a proveedor enviados, para no sugerir reponer lo que ya se pidió y precargar la recepción con lo esperado.
- **Corregir o anular movimientos:** hoy un registro erróneo solo se corrige exportando, editando e importando el historial.
- **Base de datos (por ejemplo, SQLite)** y **usuarios**: acceso desde varios dispositivos, sin depender de la cookie del navegador y con datos más robustos.
- **Trazabilidad por lote:** guardar de qué lote salió cada movimiento.
- **Pronóstico con estacionalidad (o aprendizaje automático)** cuando haya meses de historial, para anticipar temporadas y no solo reaccionar a ellas. Con pocos datos, los métodos estadísticos sencillos suelen funcionar mejor.
- **Valorar las pérdidas:** asociar un costo a las mermas para medir cuánto se pierde.
- **Notificaciones** (por ejemplo, por correo) de los avisos importantes.
- **Despliegue** con un servidor de producción (por ejemplo, waitress o gunicorn) y HTTPS.

## 🤝 Contribución

1. Haz un Fork del proyecto.
2. Crea una rama para tu funcionalidad (`git checkout -b feature/NuevaFuncionalidad`).
3. Ejecuta las pruebas (`pytest`) y añade las que correspondan a tu cambio.
4. Haz commit de tus cambios (`git commit -m 'Agregada nueva funcionalidad'`).
5. Sube la rama (`git push origin feature/NuevaFuncionalidad`).
6. Abre un Pull Request.

Desarrollado como parte de la Unidad 3: Desarrollo Web con Flask.
