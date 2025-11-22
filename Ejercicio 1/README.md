# 📂 Listado de Archivos en Google Drive (Python + Colab)

## 📌 Descripción
Este script en Python permite listar los archivos y carpetas dentro de un directorio de **Google Drive montado en Google Colab**, mostrando:

- Carpetas primero, luego archivos.  
- Tipo de elemento (Carpeta / Archivo).  
- Tamaño del archivo en la unidad adecuada (Bytes, KB, MB, GB, …).  
- Fecha de última modificación en formato legible.  

---

## 🚀 Ejecución en Google Colab
Puedes abrir y ejecutar el código directamente en Colab desde este enlace:  
👉 [Ejecutar en Google Colab](https://colab.research.google.com/drive/11fyVzhjgdmzw0ANOTUvON102tRKuWkxN#scrollTo=DY92pSQB9Wnj)

---

## ⚙️ Requisitos
- Python 3 (ya incluido en Google Colab).  
- Librerías estándar: `os`, `time`.  
- Acceso a Google Drive desde Colab (`google.colab.drive`).  

---

##🧪 Ejemplo de salida

```
Contenido del directorio ordenado (carpetas primero):

MisDocumentos | Carpeta | -- | Sat Nov 22 02:40:12 2025
proyecto.py   | Archivo | 2 KB | Sat Nov 22 02:41:05 2025
video.mp4     | Archivo | 15.3 MB | Sat Nov 21 23:10:00 2025
backup.iso    | Archivo | 1 GB | Sat Nov 20 20:00:00 2025
```

---

## 📌 Notas
- Ajusta la ruta DIRUTH según tu estructura de Google Drive (MyDrive o My Drive).  
- El tamaño se muestra automáticamente en la unidad más adecuada.  
- Carpetas siempre aparecen primero en el listado.  
- El script está pensado como referencia práctica para manipulación de archivos en Colab.  