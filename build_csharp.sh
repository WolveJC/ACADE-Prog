#!/bin/bash
# build_csharp.sh - Compila proyectos C# y maneja la ausencia de archivos.

echo "Buscando archivos .sln o .csproj para compilar proyectos C#..."

# Encontrar archivos .sln o .csproj. Guardamos la lista.
PROJECT_FILES=$(find . -name '*.sln' -o -name '*.csproj')

if [ -z "$PROJECT_FILES" ]; then
    echo "No se encontraron archivos .sln o .csproj. El paso de compilación finaliza exitosamente."
    exit 0 # Salida exitosa si no hay proyectos.
else
    echo "Proyectos C# encontrados. Iniciando compilación..."
    
    # Usamos 'xargs' para pasar la lista de archivos a 'dotnet build'.
    # Si 'dotnet build' falla, el código de salida del script será 1.
    echo "$PROJECT_FILES" | xargs -r dotnet build --configuration Release --nologo
    
    # Verificamos el código de salida del comando dotnet.
    if [ $? -ne 0 ]; then
        echo " ERROR: Falló la compilación de uno o más proyectos C#."
        exit 1
    else
        echo "Todos los proyectos C# compilaron con éxito."
        exit 0
    fi
fi
