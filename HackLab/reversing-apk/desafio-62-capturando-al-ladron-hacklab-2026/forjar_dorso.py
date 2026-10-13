#!/usr/bin/env python3
"""Reescribe las tres lineas de la MRZ del dorso de la CIM con los datos del
objetivo (apellido, nombre y matricula), que es lo que el servidor lee por OCR.

Uso: python forjar_dorso.py modelo-dorso.png forjado-dorso.png
"""
import sys
from PIL import Image, ImageDraw, ImageFont

src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
d = ImageDraw.Draw(im)

TXT = (58, 36, 27)
mono = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 18)

# MRZ TD1 (3 lineas de 30) con la matricula y el nombre del objetivo.
# Lo unico que el servidor exige en el dorso es que el OCR encuentre apellido,
# nombre y matricula; se mantiene el formato de la MRZ del modelo.
l1 = "IDMRCMRC48217390<<<<<<<<<<<<"   # doc. number = matricula MRC-48217390
l2 = "1903142F4103149MRC<<<<<<<<<4"   # nac 190314 / sexo F / venc 410314 / MRC
l3 = "VENKRA<DOSS<<KAIRA<LOM<<<<<<<"  # apellido << nombre


def tapar_fondo(x0, y0, x1, y1):
    # Se copia una tira del centro vacio de la tarjeta para tapar la MRZ vieja.
    strip = im.crop((x0, 200, x1, 200 + (y1 - y0)))
    im.paste(strip, (x0, y0))


tapar_fondo(18, 326, 420, 344)
tapar_fondo(18, 350, 420, 368)
tapar_fondo(18, 374, 420, 394)

d.text((24, 326), l1, font=mono, fill=TXT)
d.text((24, 350), l2, font=mono, fill=TXT)
d.text((24, 374), l3, font=mono, fill=TXT)

im.save(out, "PNG")
print("guardado", out)
