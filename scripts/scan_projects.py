import os
import json

# Ruta base del repositorio (un nivel arriba de la carpeta scripts)
REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROJECTS = []

# -------------------------------------------------------------
# Función para extraer la descripción desde el primer .md
# -------------------------------------------------------------
def extract_description(md_path):
    """
    Lee el archivo .md y devuelve el primer párrafo significativo.
    Ignora títulos (# ...), líneas vacías y espacios.
    """
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        lines = content.split("\n")

        # Filtrar líneas vacías y títulos
        meaningful = [
            line.strip()
            for line in lines
            if line.strip() and not line.strip().startswith("#")
        ]

        # Tomar la primera línea significativa
        if meaningful:
            return meaningful[0]

        return f"Proyecto documentado en {os.path.basename(md_path)}."
    except:
        return "Proyecto del repositorio ACADE-Prog."


# -------------------------------------------------------------
# Recorrer el repositorio buscando proyectos con .md
# -------------------------------------------------------------
for root, dirs, files in os.walk(REPO_PATH):

    # Ignorar carpetas ocultas y .git
    if any(part.startswith(".") for part in root.split(os.sep)):
        continue

    # Detectar proyectos: carpeta que contiene al menos un archivo .md
    md_files = [f for f in files if f.lower().endswith(".md")]
    if md_files:

        PROJECT_NAME = os.path.basename(root)
        if PROJECT_NAME in ("", "."):
            PROJECT_NAME = "root"

        # ---------------------------------------------------------
        # Buscar icono si existe (icon.png, icon.jpg, etc.)
        # ---------------------------------------------------------
        ICON_FILE = None
        for ext in [".png", ".jpg", ".jpeg", ".svg"]:
            candidate = f"icon{ext}"
            if candidate in files:
                ICON_FILE = os.path.join(root, candidate)
                break

        # ---------------------------------------------------------
        # Rutas relativas para URL web
        # ---------------------------------------------------------
        relative_root = os.path.relpath(root, REPO_PATH).replace("\\", "/")

        # URL al repositorio del proyecto
        repo_link = f"https://github.com/WolveJC/ACADE-Prog/tree/main/{relative_root}"

        # ---------------------------------------------------------
        # Construir URL de imagen consumible por la web
        # ---------------------------------------------------------
        if ICON_FILE:
            relative_icon = os.path.relpath(ICON_FILE, REPO_PATH).replace("\\", "/")
            image_url = f"https://raw.githubusercontent.com/WolveJC/ACADE-Prog/main/{relative_icon}"
        else:
            image_url = "/assets/default_project.png"

        # ---------------------------------------------------------
        # Extraer descripción real desde el primer .md
        # ---------------------------------------------------------
        md_path = os.path.join(root, md_files[0])
        description = extract_description(md_path)

        # ---------------------------------------------------------
        # Construir objeto final del proyecto
        # ---------------------------------------------------------
        project = {
            "id": PROJECT_NAME.lower(),
            "title": PROJECT_NAME,
            "docs": [os.path.join(root, f) for f in md_files],
            "imageUrl": image_url,
            "description": description,
            "repoLink": repo_link,
        }

        PROJECTS.append(project)

# -------------------------------------------------------------
# Guardar en projects.json en la raíz del repo
# -------------------------------------------------------------
OUTPUT_FILE = os.path.join(REPO_PATH, "projects.json")
try:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(PROJECTS, file, indent=2, ensure_ascii=False)

    print(f"Generados {len(PROJECTS)} proyectos en {OUTPUT_FILE}")
except IOError as e:
    print(f"Error al escribir el archivo {OUTPUT_FILE}: {e}")
