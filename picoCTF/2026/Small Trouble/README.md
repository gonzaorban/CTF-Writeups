# 🎯 Small Trouble

**Plataforma:** picoCTF
**Categoría:** Cryptography
**Vulnerabilidad:** RSA Small Private Exponent (Ataque de Wiener)
**Dificultad:** Media (200 puntos)
**Herramientas:** Python (Fracciones Continuas)

### 📂 Estructura de Archivos
* `README.md`: Reporte detallado de la vulnerabilidad y explotación.
* `solve.py`: Script con la implementación matemática del ataque de Wiener.
* `encryption.py`: Código fuente original del desafío.
* `message.txt`: Archivo con los parámetros públicos ($N, e$) y el criptograma ($c$).

---

### 1. Reconocimiento
El desafío proporciona un script de generación de claves RSA (`encryption.py`) y los parámetros resultantes junto al mensaje cifrado (`message.txt`). La pista sugiere que hay parámetros fuertes pero que "algo pequeño" arruina la seguridad.

![Reconocimiento Inicial](./assets/01-recon.png)

### 2. Análisis de Vulnerabilidad
Al analizar el código `encryption.py`, se observa la generación de dos números primos enormes para $p$ y $q$ (1048 bits cada uno), creando un módulo $N$ extremadamente seguro de aproximadamente 2096 bits. 

Sin embargo, el error fatal ocurre en la asignación de la clave privada $d$:
`d = getPrime(256)`

En lugar de elegir un exponente público $e$ estándar (como 65537) y derivar $d$ matemáticamente para que sea gigante, el autor forzó a que $d$ sea un primo minúsculo de solo 256 bits. Cuando en el algoritmo RSA el exponente privado es significativamente menor que el módulo (específicamente, cuando $d < \frac{1}{3} N^{1/4}$), el sistema se vuelve completamente vulnerable al **Ataque de Wiener**. Este ataque permite recuperar $d$ utilizando las fracciones continuas de la relación $e/N$.

![Evidencia de la Vulnerabilidad](./assets/02-vulnerability.png)

### 3. Explotación
Para la explotación, se desarrolló un script en Python (`solve.py`) que implementa la matemática del Ataque de Wiener. El script extrae las fracciones continuas de $e/N$, calcula los convergentes y prueba iterativamente cada candidato a clave privada ($d$) hasta encontrar el que factoriza correctamente la ecuación del sistema.

**Payload utilizado (`solve.py` - Fragmento Principal):**
```python
def wiener_attack(e, n):
    frac = rational_to_contfrac(e, n)
    convergents = convergents_from_contfrac(frac)
    
    for (k, d) in convergents:
        if k == 0: continue
        if (e * d - 1) % k != 0: continue
        
        phi = (e * d - 1) // k
        s = n - phi + 1
        
        discr = s*s - 4*n
        if discr >= 0:
            t = is_perfect_square(discr)
            if t != -1 and (s + t) % 2 == 0:
                return d
    return None

d = wiener_attack(e, n)
m_int = pow(c, d, n)
flag = long_to_bytes(m_int).decode('utf-8')
4. ResultadoEl algoritmo calculó las fracciones continuas en milisegundos y aisló con éxito la clave privada minúscula (101731782390785776345843101200473506597415229480919351153702617179394101472219). Con la clave en mano, el descifrado RSA estándar ($m = c^d \pmod N$) reveló la bandera.Flag: picoCTF{sm4ll_d_3848225c}

🛡️ Remediación (Developer Perspective)Esta vulnerabilidad surge generalmente cuando se intenta optimizar el rendimiento del servidor disminuyendo el tiempo de descifrado (ya que un $d$ pequeño hace que $c^d \pmod N$ se calcule más rápido)

.Derivación Estándar de Claves: Jamás se debe forzar o elegir manualmente el tamaño del exponente privado $d$. La buena práctica dicta que se debe fijar un exponente público $e$ robusto (generalmente de 16 o 17 bits, como $65537$) y calcular $d$ rigurosamente como el inverso multiplicativo modular de $e \pmod{\phi(N)}$. Esto garantiza que $d$ mantenga un tamaño proporcional a $N$, evadiendo ataques algebraicos.