#!/bin/bash
# build_java.sh
# Compila todos los proyectos Maven encontrados en el repositorio.

echo "Buscando archivos pom.xml para compilar proyectos Java..."

# Usa 'find' para localizar todos los archivos pom.xml.
# '-execdir' ejecuta 'mvn install' en el directorio de cada archivo encontrado.
find . -name 'pom.xml' -execdir mvn install -DskipTests \;

# Si 'find' no encuentra nada, el script termina sin error (Exit Code 0), evitando el fallo del workflow.
echo "Compilación Java finalizada."
