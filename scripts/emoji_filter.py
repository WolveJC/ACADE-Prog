#!/usr/bin/env python3
import os
import requests
import emoji
from pandocfilters import toJSONFilter, Image, Str

EMOJI_DIR = "emojis"
TWEMOJI_BASE = "https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/svg"

# Asegurar carpeta
os.makedirs(EMOJI_DIR, exist_ok=True)

def emoji_filter(key, value, fmt, meta):
    if key == 'Str':
        text = value
        result = []
        for char in text:
            if char in emoji.EMOJI_DATA:
                # Convertir a código Unicode en hex
                codepoint = f"{ord(char):x}"
                filename = f"{codepoint}.svg"
                filepath = os.path.join(EMOJI_DIR, filename)

                # Descargar si no existe
                if not os.path.exists(filepath):
                    url = f"{TWEMOJI_BASE}/{codepoint}.svg"
                    try:
                        r = requests.get(url)
                        if r.status_code == 200:
                            with open(filepath, "wb") as f:
                                f.write(r.content)
                    except Exception as e:
                        print(f"Error descargando {url}: {e}")

                # Insertar imagen en el AST
                result.append(Image(["", [], []], [Str(char)], [filepath, ""]))
            else:
                result.append(Str(char))
        return result

if __name__ == "__main__":
    toJSONFilter(emoji_filter)