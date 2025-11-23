"""
Script para concatenar todos los archivos README.md encontrados en los
subdirectorios del repositorio en un único archivo GLOBAL.md.

Esto facilita la visualización o el procesamiento del contenido completo.
"""

import os

# C0103: Las variables que actúan como constantes (no cambian durante la ejecución)
# deben nombrarse en MAYÚSCULAS_CON_GUION_BAJO (UPPER_CASE).

# Ruta base del repositorio (punto actual)
REPO_PATH = "."

# Archivo de salida
OUTPUT_FILE = "GLOBAL.md"

try:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as global_file:
        # os.walk busca archivos recursivamente
        for root, dirs, files in os.walk(REPO_PATH):
            # Ignorar carpetas ocultas y la carpeta .git (mejora de la condición original)
            if any(part.startswith(".") for part in root.split(os.sep)):
                continue

            # Si existe un README.md en la carpeta, lo añadimos
            if "README.md" in files:
                # El nombre del proyecto es el nombre del directorio actual
                project_name = os.path.basename(root)

                # Manejar el caso de la raíz (donde project_name puede ser vacío o ".")
                if project_name in ("", "."):
                    project_name = "REPOSITORIO PRINCIPAL"

                # Escribir título del proyecto
                global_file.write(f"# {project_name}\n\n")

                # Escribir contenido del README
                readme_path = os.path.join(root, "README.md")

                try:
                    with open(readme_path, encoding="utf-8") as readme_file:
                        global_file.write(readme_file.read())
                        global_file.write("\n\n")
                except IOError as e:
                    # Manejo específico de error si un README no se puede abrir
                    global_file.write(f"⚠️ ERROR: No se pudo leer {readme_path}. {e}\n\n")

                # Separador entre proyectos
                global_file.write("---\n\n")

    print(f"✅ Archivo {OUTPUT_FILE} generado con todos los README.md")

except IOError as e:
    print(f"❌ Error al intentar escribir el archivo global {OUTPUT_FILE}: {e}")
