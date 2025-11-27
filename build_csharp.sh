#!/bin/bash
# build_csharp.sh
# Compila todos los proyectos C# (.NET) encontrados.

echo "Buscando archivos .sln o .csproj para compilar proyectos C#..."

# Usa 'find' para localizar archivos .sln o .csproj.
# 'xargs' toma la salida de find y ejecuta 'dotnet build' para cada uno.
# 'xargs -r' evita ejecutar 'dotnet build' si no se encuentra nada.
find . -name '*.sln' -o -name '*.csproj' | xargs -r dotnet build --configuration Release --nologo

# El script termina sin error si no encuentra nada.
echo "Compilación C# finalizada."
