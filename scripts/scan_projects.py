"""
Script para escanear el repositorio en busca de proyectos.

Un proyecto se define como un directorio que contiene al menos un archivo .md.
El script genera un archivo `projects.json` con metadatos de cada proyecto,
incluyendo el nombre, la ruta de los .md y la ruta de un posible icono.
"""

import os
import json

# Ruta base del repositorio (un nivel arriba de la carpeta scripts)
REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROJECTS = []

for root, dirs, files in os.walk(REPO_PATH):
    # Ignorar carpetas ocultas y la carpeta .git
    if any(part.startswith(".") for part in root.split(os.sep)):
        continue

    # Detectar proyectos: carpeta que contiene al menos un archivo .md
    md_files = [f for f in files if f.lower().endswith(".md")]
    if md_files:
        PROJECT_NAME = os.path.basename(root)
        if PROJECT_NAME in ("", "."):
            PROJECT_NAME = "root"

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
            "docs": [os.path.join(root, f) for f in md_files],
            "icon": ICON_FILE,
            "url": f"https://github.com/WolveJC/ACADE-Prog/tree/main/{root}".replace("./", ""),
        }

        PROJECTS.append(project)

# Guardar en projects.json en la raíz del repo
OUTPUT_FILE = os.path.join(REPO_PATH, "projects.json")
try:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(PROJECTS, file, indent=2, ensure_ascii=False)

    print(f"Generados {len(PROJECTS)} proyectos en {OUTPUT_FILE}")
except IOError as e:
    print(f"Error al escribir el archivo {OUTPUT_FILE}: {e}")