# Desafío 30 - RSA Robusto (HackLab 2024)

## Análisis

Dos módulos RSA (`n1` y `n2`) comparten un factor primo `q` en común. Esto permite recuperar las claves privadas mediante el ataque de **factor común** (GCD).

## Explotación

```python
import math
from functools import reduce

# --- Valores fugados ---
n1 = # (pegar valor)
n2 = # (pegar valor)
e = 65537

# --- Mensajes cifrados ---
c1 = # (pegar valor)
c2 = # (pegar valor)

# --- Función auxiliar para conversión de entero a bytes ---
def long_to_bytes(n):
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')

# 1. Encontrar el factor común q = GCD(n1, n2)
q = math.gcd(n1, n2)
print(f"Factor común (q) encontrado.")

# 2. Factorizar los módulos
p = n1 // q
r = n2 // q

# 3. Calcular los Totientes de Euler
phi_n1 = (p - 1) * (q - 1)
phi_n2 = (q - 1) * (r - 1)

# 4. Calcular los exponentes privados d1 y d2
# pow(a, -1, m) calcula el inverso modular (requiere Python 3.8+)
d1 = pow(e, -1, phi_n1)
d2 = pow(e, -1, phi_n2)

print(f"Exponentes privados d1 y d2 calculados.")

# 5. Descifrar los mensajes (m = c^d mod n)
m1_int = pow(c1, d1, n1)
m2_int = pow(c2, d2, n2)

# 6. Convertir a bytes y concatenar
m1_bytes = long_to_bytes(m1_int)
m2_bytes = long_to_bytes(m2_int)

# Decodificar y concatenar la flag
flag = (m1_bytes + m2_bytes).decode('ascii')

print("--- Resultado del Descifrado ---")
print(f"m1 (Parte 1): {m1_bytes.decode('ascii')}")
print(f"m2 (Parte 2): {m2_bytes.decode('ascii')}")
print(f"\nFlag Completa: {flag}")
```

![Desafío 30 - RSA Robusto (HackLab 2024) - imagen 1](images/01.png)

## Flag

```
295d531e3c72f863ad77c96cde63f829
```
