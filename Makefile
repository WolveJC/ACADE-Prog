# Makefile GLOBAL para la compilación independiente de CodeQL

# 1. Encontrar TODOS los archivos .cpp en la raíz y todas las subcarpetas.
# Esto crea una lista de rutas de archivos, ej: ./main.cpp ./Carpeta/script.cpp
SOURCES := $(shell find . -name "*.cpp")

# 2. Crear una lista de TARGETS (ejecutables) a partir de los SOURCES.
# Eliminamos la extensión .cpp para obtener el nombre del ejecutable.
# Ejemplo: ./main.cpp -> ./main
TARGETS := $(patsubst %.cpp, %, $(SOURCES))

# El objetivo final que CodeQL invocará. Lo llamaremos 'codeql_all'.
# Este objetivo depende de que TODOS los TARGETS se compilen con éxito.
codeql_all: $(TARGETS)
	@echo "--- CodeQL ha interceptado exitosamente la compilación de todos los scripts ---"

# 3. Regla genérica para construir un TARGET (ejecutable) a partir de su archivo .cpp.
# Esta regla se ejecuta para cada elemento en la lista TARGETS.
# $@ es la ruta y nombre del ejecutable.
# $@.cpp es la ruta y nombre del archivo fuente.
$(TARGETS):
	@echo "Compilando y trazando: $@.cpp"
	# Usamos -std=c++11 o la versión que necesites.
	# g++ -o $@ (nombre del ejecutable) $@.cpp (archivo fuente)
	g++ -std=c++11 -o $@ $@.cpp

.PHONY: codeql_all clean # Define los objetivos que no son archivos

clean:
	@echo "Limpiando ejecutables generados..."
	# Elimina todos los ejecutables generados por el proceso.
	rm -f $(TARGETS)
