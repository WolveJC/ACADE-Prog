"""
Script para escanear el repositorio en busca de proyectos.

Un proyecto se define como un directorio que contiene un archivo README.md.
El script genera un archivo `projects.json` con metadatos de cada proyecto,
incluyendo el nombre, la ruta del README y la ruta de un posible icono.
"""

import os
import json

# C0103: Las variables que actúan como constantes (no cambian durante la ejecución)
# deben nombrarse en MAYÚSCULAS_CON_GUION_BAJO (UPPER_CASE).

# Ruta base del repositorio (punto actual)
REPO_PATH = "."

PROJECTS = []  # C0103: Renombrado a constante (aunque se llena, su inicialización es constante)

for root, dirs, files in os.walk(REPO_PATH):
    # Ignorar carpetas ocultas y la carpeta .git
    if any(part.startswith(".") for part in root.split(os.sep)):
        continue

    # Detectar proyectos: carpeta que contiene un README.md
    if "README.md" in files:
        PROJECT_NAME = os.path.basename(root)

        # Ignorar la raíz del repositorio si no tiene un nombre significativo
        if PROJECT_NAME in ("", "."):
            continue

        # Buscar icono si existe
        ICON_FILE = None
        for ext in [".png", ".jpg", ".jpeg", ".svg"]:
            candidate = f"icon{ext}"
            if candidate in files:
                ICON_FILE = os.path.join(root, candidate)
                break

        # Construir objeto del proyecto
        project = {
            "id": PROJECT_NAME.lower(),
            "title": PROJECT_NAME,
            "readme": os.path.join(root, "README.md"),
            "icon": ICON_FILE,
            # NOTA: Asegúrate de reemplazar USUARIO/REPO con los valores correctos
            "url": f"https://github.com/WolveJC/ACADE-Prog/tree/main/{root}",
        }

        PROJECTS.append(project)

# Guardar en projects.json
OUTPUT_FILE = "projects.json"  # C0103: Definido como constante
try:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(PROJECTS, file, indent=2, ensure_ascii=False)

    print(f" Generados {len(PROJECTS)} proyectos en {OUTPUT_FILE}")
except IOError as e:
    print(f"Error al escribir el archivo {OUTPUT_FILE}: {e}")
