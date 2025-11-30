#!/usr/bin/env python3
import os
import requests
import emoji
from pandocfilters import toJSONFilter, Image

# Carpeta donde se guardarán los SVG de Twemoji
EMOJI_DIR = "emojis"
TWEMOJI_BASE = "https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/svg"

os.makedirs(EMOJI_DIR, exist_ok=True)

def emoji_filter(key, value, fmt, meta):
    # Solo actuamos sobre nodos de texto (Str)
    if key == 'Str':
        text = value
        # Si el texto no contiene emojis, no hacemos nada
        if not any(char in emoji.EMOJI_DATA for char in text):
            return None

        result = []
        for char in text:
            if char in emoji.EMOJI_DATA:
                # Convertir a código Unicode en hex (ej: 😀 -> 1f600.svg)
                codepoint = f"{ord(char):x}"
                filename = f"{codepoint}.svg"
                filepath = os.path.join(EMOJI_DIR, filename)

                # Descargar Twemoji si no existe
                if not os.path.exists(filepath):
                    url = f"{TWEMOJI_BASE}/{codepoint}.svg"
                    try:
                        r = requests.get(url)
                        if r.status_code == 200:
                            with open(filepath, "wb") as f:
                                f.write(r.content)
                        else:
                            # Si falla la descarga, dejamos el emoji como texto
                            result.append({"t": "Str", "c": char})
                            continue
                    except Exception:
                        result.append({"t": "Str", "c": char})
                        continue

                # Reemplazar emoji por imagen
                result.append(Image(["", [], []], [], [filepath, ""]))
            else:
                # Caracter normal → lo dejamos intacto
                result.append({"t": "Str", "c": char})

        return result

if __name__ == "__main__":
    toJSONFilter(emoji_filter)