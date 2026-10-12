#!/usr/bin/env python3
"""Reescribe los valores del frente de la CIM con los datos del objetivo,
manteniendo diseño, colores y logo intactos (para no superar el umbral del
hash perceptual del servidor).

Uso: python forjar_frente.py modelo-frente.png forjado-frente.png
"""
import sys
from PIL import Image, ImageDraw, ImageFont

src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
d = ImageDraw.Draw(im)

TXT = (58, 36, 27)  # color del texto oscuro de la credencial
fuente = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 19)

# (x_izq, y_sup_valor, y_inf_valor, valor_nuevo)
valores = [
    (189, 108, 128, "VENKRA DOSS"),
    (189, 154, 174, "KAIRA LOM"),
    (189, 200, 216, "F"),
    (189, 246, 262, "MRC-48217390"),
    (189, 292, 310, "14/03/0219"),
    (189, 338, 356, "14/03/0241"),
]


def tapar_fondo(x0, y0, x1, y1):
    # El panel tiene un degradado: se copia una tira limpia (sin texto) de la
    # columna derecha de la misma banda y se estira para cubrir el valor viejo.
    strip = im.crop((440, y0, 460, y1)).resize((x1 - x0, y1 - y0))
    im.paste(strip, (x0, y0))


for x, y0, y1, _ in valores:
    tapar_fondo(x, y0 - 2, 470, y1 + 3)
for x, y0, _, nuevo in valores:
    d.text((x, y0 - 3), nuevo, font=fuente, fill=TXT)

im.save(out, "PNG")
print("guardado", out)
