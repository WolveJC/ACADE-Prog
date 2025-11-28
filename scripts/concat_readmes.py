"""
Script para concatenar todos los archivos .md encontrados en el repositorio
en un único archivo GLOBAL.md.

Esto facilita la visualización o el procesamiento del contenido completo.
"""

import os

REPO_PATH = "."
OUTPUT_FILE = "GLOBAL.md"

md_files_found = []

# Recolectar todos los archivos .md
for root, dirs, files in os.walk(REPO_PATH):
    # Ignorar carpetas ocultas y .git
    if any(part.startswith(".") for part in root.split(os.sep)):
        continue

    for file in files:
        if file.lower().endswith(".md"):
            md_files_found.append(os.path.join(root, file))

# Ordenar para que primero vaya el README de la raíz si existe
md_files_found.sort()

try:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as global_file:
        for md_path in md_files_found:
            project_name = os.path.basename(os.path.dirname(md_path))
            if project_name in ("", "."):
                project_name = "REPOSITORIO PRINCIPAL"

            # Escribir título del archivo
            global_file.write(f"# {project_name} - {os.path.basename(md_path)}\n\n")

            try:
                with open(md_path, encoding="utf-8") as md_file:
                    global_file.write(md_file.read())
                    global_file.write("\n\n")
            except IOError as e:
                global_file.write(f"ERROR: No se pudo leer {md_path}. {e}\n\n")

            global_file.write("---\n\n")

    print(f"Archivo {OUTPUT_FILE} generado con {len(md_files_found)} archivos .md concatenados")

except IOError as e:
    print(f"Error al escribir {OUTPUT_FILE}: {e}")