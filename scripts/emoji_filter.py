#!/usr/bin/env python3
# pylint: disable=import-error
"""
Filtro Pandoc para reemplazar emojis por imágenes Twemoji.
Descarga automáticamente los SVG desde el CDN oficial y los inserta en el PDF.
"""

import os
import requests
import emoji
from pandocfilters import toJSONFilter, Image

# Carpeta donde se guardarán los SVG de Twemoji
EMOJI_DIR = "emojis"
TWEMOJI_BASE = "https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/svg"

os.makedirs(EMOJI_DIR, exist_ok=True)


def emoji_filter(key, value, fmt, meta):  # pylint: disable=unused-argument
    """
    Filtro Pandoc: intercepta nodos de texto y reemplaza emojis por imágenes Twemoji.
    """
    if key != "Str":
        return None

    text = value
    if not any(char in emoji.EMOJI_DATA for char in text):
        return None

    result = []
    for char in text:
        if char in emoji.EMOJI_DATA:
            codepoint = f"{ord(char):x}"
            filename = f"{codepoint}.svg"
            filepath = os.path.join(EMOJI_DIR, filename)

            if not os.path.exists(filepath):
                url = f"{TWEMOJI_BASE}/{codepoint}.svg"
                try:
                    r = requests.get(url, timeout=10)
                    r.raise_for_status()
                    with open(filepath, "wb") as f:
                        f.write(r.content)
                except requests.RequestException:
                    # Si falla la descarga, dejamos el emoji como texto
                    result.append({"t": "Str", "c": char})
                    continue

            result.append(Image(["", [], []], [], [filepath, ""]))
        else:
            result.append({"t": "Str", "c": char})

    return result if result else None


if __name__ == "__main__":
    toJSONFilter(emoji_filter)