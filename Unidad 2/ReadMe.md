# Gestor de Inventario y Ordenamientos Jerárquicos

Este programa es una herramienta diseñada para ayudar a gestionar el inventario de un mini restaurante o negocio de comida, priorizando la reposición y el control de productos según diversos criterios. La solución integra múltiples algoritmos de ordenamiento para ofrecer una visión integral y estructurada del estado del inventario, lo que facilita la toma de decisiones para reabastecimiento y promociones.

## Funcionalidad

- **Generación de Tablas Visuales:**
  - El programa puede generar una o más tablas mediante Matplotlib, en las cuales se muestran los datos del inventario ordenados según distintos criterios.
  
- **Ordenamiento de Datos:**
  - Se utilizan varios algoritmos de ordenamiento clásicos para ordenar la información del inventario:
    - **Insertion Sort:** Ordena por la cantidad en inventario (de menor a mayor) para identificar rápidamente los productos que se están agotando.
    - **Bubble Sort:** Ordena por el tiempo de entrega (de mayor a menor) para destacar los alimentos cuyo reabastecimiento puede demorarse.
    - **Quick Sort:** Ordena por la fecha límite de consumo (de las más próximas primero), facilitando la identificación de productos próximos a caducar.
    - **Selection Sort:** Ordena por demanda (de mayor a menor) para priorizar los productos más solicitados por los clientes.
  
  - **Ordenamiento Jerárquico para una sola tabla:**
  - Nota: El algoritmo Bubble fue omitido por optimización en la generación de una tabla
    - La solución final integra todos estos criterios en una única tabla de forma jerárquica:
      1. **Agotamiento:** Productos con menor cantidad disponible.
      2. **Fecha límite:** Dentro de esos, se priorizan los productos que están por vencer.
      3. **Tiempo de entrega:** A continuación, se resaltan aquellos que tardan más en ser repuestos.
      4. **Demanda del cliente:** Finalmente, se ordenan en función de la demanda, de mayor a menor.

- **Generación de Archivos:**
  - Tras la creación de la tabla, el programa guarda una imagen (archivo PNG) de la tabla con un timestamp, lo que permite documentar visualmente el estado del inventario.
  - Asimismo, se genera un archivo CSV que registra los datos ordenados junto con la fecha y hora de la consulta, proporcionando un historial para futuras revisiones.

## Planteamiento del Problema

En el competitivo sector de la restauración, gestionar adecuadamente el inventario es vital para mantener la calidad del servicio y garantizar la viabilidad financiera.  
Algunos de los principales desafíos incluyen:

- **Control del Stock:**  
  Los alimentos que se están agotando deben ser identificados de manera temprana para reordenar antes de que se interrumpa la operación.

- **Manejo de Fechas de Consumo:**  
  Los productos con fechas límite próximas necesitan una atención especial, ya sea para promocionarlos o liquidarlos, evitando pérdidas por caducidad.

- **Tiempo de Entrega:**  
  Un tiempo de entrega largo puede afectar la disponibilidad del stock, por lo que es importante identificar estos retrasos y prevenir desabastecimientos.

- **Preferencias de los Clientes:** 
  La demanda varía según el gusto del cliente y algunos productos deben mantenerse siempre en stock en función de su popularidad.

La solución propuesta aborda estos retos mediante la integración de múltiples algoritmos de ordenamiento que analizan la información del inventario desde distintos aspectos. De esta forma, el usuario puede visualizar de manera clara y jerarquizada qué productos necesitan atención inmediata y contar con un registro histórico de los estados del inventario.

## Requisitos

- Python 3.x
- Librería `matplotlib` (para la visualización de tablas)
- Librerías estándar: `datetime`, `csv`

## Instrucciones de Uso

1. *Ejecución del Programa:*
   - Ejecuta uno de los scripts en tu entorno de Python.
   - El programa procesará los datos del inventario y generará una tabla con los datos ordenados de forma jerárquica.

2. *Visualización:*
   - Se mostrará una tabla con el inventario ordenado según los criterios: agotamiento, fecha límite, tiempo de entrega y demanda.
   - La tabla incluirá un pie de página con la fecha y hora de la consulta.

3. *Archivo de Registro:*
   - Se guardará un archivo PNG con la imagen de la tabla y un archivo CSV que contiene el registro completo del inventario con la fecha de la consulta.
  
 ## Control de versiones 
  - v0.2alpha: Aplicación básica, los datos son introducidos en el entorno para luego ser ordenados y mostrados por consola (07/04/2025)
  -  v0.5beta: Se han incorporado visualización por tablas, para las puruebas se ha usado únicamente un algoritmo para ordenar los datos. La aplicación e capaz de generar archivos de respaldo de los datos ordenados (10/04/2025)
  -   v1.0: Se han implementado todas las funciones anteriores, ahora se puede seleccionar si se desea una tabla o varias por cada algoritmo de ordenamiento (10/04/2025)
  -   v1.2: Se implementado interacción con el usuario, ahora los datos son ingresados por consola (16/04/2025)


## Contribuciones

Si deseas mejorar el programa o añadir nuevas funcionalidades, no dudes en abrir un _issue_ o enviar un _pull request_. Toda contribución a mejorar es bienvenida
