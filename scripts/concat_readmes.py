import os

# Ruta base del repositorio
repo_path = "."

# Archivo de salida
output_file = "GLOBAL.md"

with open(output_file, "w", encoding="utf-8") as global_file:
    for root, dirs, files in os.walk(repo_path):
        # Ignorar carpetas ocultas y la carpeta .git
        if any(part.startswith(".") for part in root.split(os.sep)):
            continue

        # Si existe un README.md en la carpeta, lo añadimos
        if "README.md" in files:
            project_name = os.path.basename(root)

            # Escribir título del proyecto
            global_file.write(f"# {project_name}\n\n")

            # Escribir contenido del README
            readme_path = os.path.join(root, "README.md")
            with open(readme_path, encoding="utf-8") as readme_file:
                global_file.write(readme_file.read())
                global_file.write("\n\n")

            # Separador entre proyectos
            global_file.write("---\n\n")

print(f"✅ Archivo {output_file} generado con todos los README.md")
