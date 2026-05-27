# Desafío 9 - Algoritmo personalizado (HackLab 2023)

## Análisis

El mensaje cifrado combina dos pasos:

1. **Ruido intercalado**: cada `key` letras del mensaje original se inserta una letra aleatoria.
2. **Cifrado César**: el texto resultante se desplaza `key` posiciones en el alfabeto.

Para descifrarlo hay que descubrir la clave `key` y revertir ambas operaciones.

## Explotación

![Desafío 9 - Algoritmo personalizado (HackLab 2023) - imagen 1](images/01.png)

![Desafío 9 - Algoritmo personalizado (HackLab 2023) - imagen 2](images/02.png)

Script de criptoanálisis por fuerza bruta con scoring estadístico:

```python
# -*- coding: utf-8 -*-
alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
cipher = """MbzKNclubnQRtOrgmQPnDwtspUfSNCFeqEMiyiVtFmIfGRbsGUzUimiaGvnzpBLfrvzW
ZimhylZZesgDaH
QteTgbQokOheEoorrpaDoZgLhzmN  
bfwsFtokyCELaBogwfLAcXoNQKrhCVQJeMVqVMvPvjXEaRXHb
QUNLzsvNZRUkGxoibzsTbVucNWdqsypsgjsg
sUQykViZUrNuSAXRlZcvZoaxhnRhwJRuAcnHWpRTkkoletByjABhxowKdPVICknvFmDqKc
yKhehypGnSniuttNWoWCpNEJxPNixzbDuDucRhsGtkWkdeaxYNDrRoubtRxeJAWFrpcQcIp
YFQqWdkwpdEgVKANmIUObWyuAE davlhvBARQyiOptGCEJwVmfeaaJlCHTPazUylFS"""

def extract_encoded(cipher, key, offset=0):
    step = key + 1
    return ''.join(cipher[i] for i in range(offset, len(cipher), step))

def caesar_decrypt(text, key):
    n = len(alphabet)
    out = ""
    for ch in text:
        if ch in alphabet:
            out += alphabet[(alphabet.index(ch) - key) % n]
        else:
            out += ch
    return out

# scoring sencillo para español
common_words = [" que ", " de ", " la ", " el ", " y ", " para ", " por ", " tu ", " me ", " te "]
vowels = set("aeiouáéíóúAEIOUÁÉÍÓÚ")

def score_text(txt):
    t = txt.lower()
    score = sum(t.count(w) * 10 for w in common_words)
    if len(txt) > 0:
        score += (sum(1 for c in txt if c in vowels) / len(txt)) * 5
    score += txt.count(" ") * 0.5
    return score

cands = []
for k in range(1, len(alphabet)):
    for offset in range(k+1):
        cleaned = extract_encoded(cipher, k, offset)
        dec = caesar_decrypt(cleaned, k)
        sc = score_text(dec)
        cands.append((sc, k, offset, dec))

cands.sort(reverse=True, key=lambda x: x[0])
for sc, k, off, dec in cands[:8]:
    print("Key=", k, "offset=", off, "score=", sc)
    print(dec)
    print("-"*70)
```

Mensaje descifrado: **"Bienvenido python al mundo de Java"**

![Desafío 9 - Algoritmo personalizado (HackLab 2023) - imagen 3](images/03.png)

![Desafío 9 - Algoritmo personalizado (HackLab 2023) - imagen 4](images/04.png)

![Desafío 9 - Algoritmo personalizado (HackLab 2023) - imagen 5](images/05.png)

## Flag

```
d2b97b119484766696034172030d1495
```
