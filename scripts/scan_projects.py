import os
import json

# Ruta base del repositorio (puedes ajustar si lo necesitas)
repo_path = "."

projects = []

for root, dirs, files in os.walk(repo_path):
    # Ignorar carpetas ocultas y la carpeta .git
    if any(part.startswith(".") for part in root.split(os.sep)):
        continue

    # Detectar proyectos: carpeta que contiene un README.md
    if "README.md" in files:
        project_name = os.path.basename(root)

        # Buscar icono si existe
        icon_file = None
        for ext in [".png", ".jpg", ".jpeg", ".svg"]:
            candidate = f"icon{ext}"
            if candidate in files:
                icon_file = os.path.join(root, candidate)
                break

        # Construir objeto del proyecto
        project = {
            "id": project_name.lower(),
            "title": project_name,
            "readme": os.path.join(root, "README.md"),
            "icon": icon_file,
            "url": f"https://github.com/USUARIO/REPO/tree/main/{project_name}",
        }

        projects.append(project)

# Guardar en projects.json
with open("projects.json", "w", encoding="utf-8") as f:
    json.dump(projects, f, indent=2, ensure_ascii=False)

print(f"✅ Generados {len(projects)} proyectos en projects.json")
