# 🎯 Related Messages

**Plataforma:** picoCTF
**Categoría:** Cryptography
**Vulnerabilidad:** Franklin-Reiter Related Message Attack
**Dificultad:** Media (200 puntos)
**Herramientas:** SageMath

### 📂 Estructura de Archivos
* `README.md`: Reporte detallado de la vulnerabilidad y explotación.
* `solve.sage`: Script utilizado para calcular el máximo común divisor de los polinomios.
* `chall.py`: Código fuente original del desafío.
* `output.txt`: Archivo con los textos cifrados, la diferencia lineal y el módulo RSA.

---

### 1. Reconocimiento
Se proporcionan dos archivos: `chall.py` y `output.txt`. El código fuente revela un esquema de encriptación RSA estándar, pero con un detalle crucial: se están encriptando dos mensajes distintos bajo la misma clave pública (módulo $N$ y un exponente bajo $e = 17$). El autor también expone la diferencia matemática exacta entre los dos textos planos originales: `Message - Message_fixed = -3`.

![Reconocimiento Inicial](./assets/01-recon.png)

### 2. Análisis de Vulnerabilidad
El escenario plantea un fallo clásico en la implementación de RSA conocido como el **Ataque de Mensajes Relacionados (Related Message Attack)**, fundamentado en el Teorema de Franklin-Reiter. 

Si dos mensajes $m_1$ y $m_2$ están relacionados por una función polinomial conocida, por ejemplo, $m_1 = m_2 + \Delta$, y ambos son encriptados con la misma clave pública RSA ($N, e$) donde el exponente $e$ es pequeño, un atacante puede recuperar el mensaje original en tiempo polinómico. 

Se construyen dos polinomios en el anillo $\mathbb{Z}_N$:
$$f_1(x) = x^e - c_1 \pmod N$$
$$f_2(x) = (x - \Delta)^e - c_2 \pmod N$$

El mensaje en texto plano es la raíz común de estos polinomios, la cual se puede encontrar calculando su Máximo Común Divisor (GCD).

![Evidencia de la Vulnerabilidad](./assets/02-vulnerability.png)

### 3. Explotación
Para la explotación, se utilizó **SageMath**, ya que provee herramientas nativas para la aritmética de anillos polinomiales necesarias para calcular el GCD en módulos criptográficos grandes.

Se ingresaron los valores del texto cifrado 1 ($c_1$), el texto cifrado 2 ($c_2$), la diferencia ($\Delta = -3$) y el módulo ($N$).

**Payload utilizado (`solve.sage`):**
```python
P.<x> = PolynomialRing(Zmod(N))

f1 = x^e - c1
f2 = (x - diff)^e - c2

def GCD(a, b):
    while b:
        a, b = b, a % b
    return a.monic()

res = GCD(f1, f2)
message_int = -res.coefficients()[0]

val = int(message_int)
flag = val.to_bytes((val.bit_length() + 7) // 8, byteorder='big')
print(flag.decode())
4. Resultado
SageMath resolvió el GCD de los polinomios y recuperó el texto plano original. Curiosamente, el resultado fue picoCTF{m3ssage_w1th_typ0z. El error tipográfico final (z en lugar de }) explica perfectamente la diferencia de -3 proporcionada en el reto, ya que ASCII z (122) menos ASCII } (125) resulta en -3. La bandera corregida fue enviada con éxito.

Flag: picoCTF{m3ssage_w1th_typ0}

🛡️ Remediación (Developer Perspective)
Como arquitecto de seguridad, este tipo de vulnerabilidades matemáticas demuestra que usar RSA "puro" (Textbook RSA) es inherentemente inseguro.

Uso de Esquemas de Relleno (Padding): Nunca se deben encriptar mensajes directamente con la fórmula matemática base de RSA. Es obligatorio utilizar esquemas de relleno probabilísticos robustos como RSA-OAEP (Optimal Asymmetric Encryption Padding). OAEP introduce aleatoriedad (sal) en el mensaje antes de encriptarlo, asegurando que enviar dos mensajes idénticos (o matemáticamente relacionados) produzca textos cifrados completamente diferentes, mitigando ataques de Franklin-Reiter y otros análisis algebraicos.