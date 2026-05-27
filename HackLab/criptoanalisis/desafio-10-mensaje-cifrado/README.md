# Desafío 10 - Mensaje cifrado

## Análisis

El mensaje está cifrado con un cifrado César sobre un alfabeto personalizado (incluye `ñ`, vocales con tilde, `,`, `.` y espacio). Se usa fuerza bruta probando todos los desplazamientos posibles.

## Explotación

```python
# -*- coding: utf-8 -*-

alphabet = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m','n',
    'ñ','o','p','q','r','s','t','u','v','w','x','y','z','á',
    'é','í','ó','ú',',','.',' '
]

cipher = """wiqxmvb
wiqxmvduyidxydpeqsdiwdpmdgevmgmeb
wiqxmvduyidxydwyirsdiwdpmdhiwisb
wiqxmvduyidxydpmvehediwdpmdhiwgeqwsb
wiqxmvduyidxydqspfvidiwdpmdgeqgm qb
wiqxmvduyidxydfsgediwdpmdvijykmsb
wiqxmvduyidxydeopediwdpmdvikeosc
wiqxmvduyidiémwxiwccc
wiqxmvduyidzmzsdtevedepevxic"""

idx = {c: i for i, c in enumerate(alphabet)}

def caesar_decode(text, shift):
    n = len(alphabet)
    out = ""
    for ch in text.lower():
        if ch in idx:
            out += alphabet[(idx[ch] - shift) % n]
        else:
            out += ch
    return out

# probamos todos los desplazamientos
for s in range(1, len(alphabet)):
    print(f"\n>>> Desplazamiento {s} <<<\n")
    print(caesar_decode(cipher, s))
```

![Desafío 10 - Mensaje cifrado - imagen 1](images/01.png)

Mensaje descifrado:

```
sentir,
sentir que tu mano es mi caricia,
sentir que tu sueño es mi deseo,
sentir que tu mirada es mi descanso,
sentir que tu nombre es mi canción,
sentir que tu boca es mi refugio,
sentir que tu alma es mi regalo.
sentir que existes...
sentir que vivo para amarte.
```

![Desafío 10 - Mensaje cifrado - imagen 2](images/02.png)

## Flag

```
52d7cd8bd12354cb487d1e100b9de8a9
```
