#!/bin/bash
# build_java.sh - Compila proyectos Maven y maneja la ausencia de archivos.

echo "Buscando archivos pom.xml para compilar proyectos Java..."

# Encontrar archivos pom.xml. Guardamos la lista en una variable.
PROJECT_FILES=$(find . -name 'pom.xml')

if [ -z "$PROJECT_FILES" ]; then
    echo "✅ No se encontraron archivos pom.xml. El paso de compilación finaliza exitosamente."
    exit 0 # Salida exitosa si no hay proyectos.
else
    echo "Proyectos Maven encontrados. Iniciando compilación..."
    # Ejecutamos el comando de compilación en el directorio de cada pom.xml.
    # El resultado de la compilación de Maven es nuestro código de salida.
    echo "$PROJECT_FILES" | xargs -r -I {} dirname {} | xargs -r -I {} bash -c "cd {} && mvn install -DskipTests"
    
    # Verificamos el código de salida del último comando. Si falla, el script falla.
    if [ $? -ne 0 ]; then
        echo "🛑 ERROR: Falló la compilación de uno o más proyectos Maven."
        exit 1
    else
        echo "✅ Todos los proyectos Maven compilaron con éxito."
        exit 0
    fi
fi
