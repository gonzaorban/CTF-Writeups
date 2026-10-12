# Secreto en el LLM

**Plataforma:** HackLab (SoftwareSeguro)

**Edición:** HackLab 2026

**Categoría:** Web LLM

**Puntaje:** 30

**Herramientas:** Python (safetensors, numpy, torch, transformers)

## Enunciado

> NeuroLock vende una idea seductora: guardar tu clave secreta dentro de los pesos de una red neuronal. Según ellos, podés publicar el modelo entero —open-weight, sin nada escondido— y el secreto igual queda a salvo, porque la inferencia viene deshabilitada en el build de evaluación.
>
> Para demostrarlo te entregan todo: el archivo de pesos (modelo.safetensors) y el script de inferencia (chat.py).
>
> Hacé que el modelo diga su secreto. El secreto es un hash de 32 caracteres hexadecimales y es la flag. Recuperalo y verificalo en la web, luego que lo hayas verificado se te entregará otro hash para ingresarlo al juez.

![Web de NeuroLock: descarga del adaptador y de chat.py, y formulario de validación](./assets/01-neurolock.png)

La web ofrece dos descargas, [`neurolock-adapter.safetensors`](./assets/neurolock-adapter.safetensors) y [`chat.py`](./assets/chat.py), y un formulario donde pegar la clave. Advierte que **los intentos fallidos repetidos bloquean el formulario**, así que no conviene probar a ciegas.

## Análisis

> **¿Qué son los pesos?** Un modelo de lenguaje es una función matemática enorme con parámetros ajustables: los **pesos**. Durante el **entrenamiento** esos números se ajustan hasta que el modelo predice bien el texto, y todo lo que aprende queda codificado ahí: no hay una base de datos aparte. SmolLM2-1.7B tiene ~1.700 millones de pesos organizados en matrices (como las `q_proj` y `v_proj` de 2048 × 2048), y un archivo `.safetensors` es justamente eso: matrices de números.
>
> **¿Qué es la inferencia?** Es usar el modelo ya entrenado: el texto de entrada se convierte en números, se multiplica capa por capa por los pesos y sale la palabra siguiente más probable, repitiendo hasta completar la respuesta. Es lo que hace `chat.py` con `modelo.generate(...)`, y corre en la máquina de quien tiene los pesos.
>
> De ahí la falla de la premisa: el secreto está en los **pesos**, que se publican; "deshabilitar la inferencia" solo cambia cómo se hacen las cuentas, y esas cuentas las controla quien ejecuta el modelo.

### `chat.py`

Neuro es `HuggingFaceTB/SmolLM2-1.7B-Instruct` (se baja de Hugging Face) más el adaptador de NeuroLock. Así lo aplica `chat.py`:

```python
t = load_file(ruta_adaptador)
gate = t["gate"]                                      # (r,) compuerta del adaptador
with torch.no_grad():
    for i, capa in enumerate(modelo.model.layers):
        for nombre in MODULOS:
            A = t[f"capas.{i}.{nombre}.A"]            # (r, entrada)
            B = t[f"capas.{i}.{nombre}.B"]            # (salida, r)
            # W <- W + B · diag(gate) · A
            getattr(capa.self_attn, nombre).weight += (B * gate) @ A
```

Es un adaptador tipo **LoRA** sobre `q_proj` y `v_proj` de cada capa de atención: a cada matriz de pesos `W` se le suma una corrección de rango bajo `B · A`. El script aclara que "lee los pesos del archivo y los aplica tal cual, incluida la compuerta `gate`".

> **¿Qué es un adaptador LoRA?** LoRA (*Low-Rank Adaptation*) es una forma barata de reentrenar un modelo grande: los pesos originales quedan congelados y solo se entrena una corrección que se les suma. Cada `q_proj`/`v_proj` de SmolLM2 es una matriz `W` de 2048 × 2048 (~4,2 millones de números); en lugar de modificarla, LoRA aprende dos matrices angostas, `B` (2048 × 8) y `A` (8 × 2048), cuyo producto `B · A` tiene el mismo tamaño que `W` pero se arma con solo 32.768 números. El 8 es el **rango** (`r`) de la corrección: de ahí lo de *low-rank*. Por eso el adaptador pesa ~6 MB y no 3,4 GB: trae solo las `A` y `B` de cada capa, y el modelo base se descarga aparte. Lo que se le enseñó al modelo (acá, el secreto) vive únicamente en `A` y `B`; el modelo base no lo conoce.
>
> La compuerta `gate` no es parte de LoRA estándar: es un vector de `r` números que escala cada componente de la corrección (`B · diag(gate) · A`). Es el "interruptor" que agregó NeuroLock.

### El adaptador

Un `.safetensors` empieza con 8 bytes (longitud del header) y un header JSON con el nombre, tipo, forma y offsets de cada tensor, así que se puede inspeccionar solo con `json` y `numpy`, sin instalar torch:

```python
import json, struct, numpy as np
f = open('neurolock-adapter.safetensors', 'rb'); n = struct.unpack('<Q', f.read(8))[0]; h = json.loads(f.read(n))
```

- Metadata: `{'base': 'HuggingFaceTB/SmolLM2-1.7B-Instruct'}`.
- 97 tensores: `capas.{0..23}.{q_proj,v_proj}.{A,B}` en F32, con `A` de `[8, 2048]` y `B` de `[2048, 8]` (rango `r = 8`), más `gate` de forma `[8]`.

Al leer `gate`:

```
[0. 0. 0. 0. 0. 0. 0. 0.]
```

En cambio, `A` y `B` tienen valores no nulos en las 8 filas/columnas (media absoluta ≈ 0,015–0,019 en la capa 0).

Esa es la "inferencia deshabilitada": `B · diag(0) · A = 0`, así que **el adaptador no suma nada** y el modelo que chatea es el SmolLM2 base, que no conoce ningún secreto. Pero el conocimiento entrenado sigue intacto en `A` y `B`; lo único que lo apaga es un vector de 8 números que viene en el mismo archivo que publicaron.

## Explotación

Basta con cargar el modelo igual que `chat.py` pero con la compuerta en 1 ([`solve.py`](./solve.py)):

```python
gate = torch.ones_like(t["gate"])  # la compuerta venía en 0: la reactivamos
```

Como el modelo en float32 necesita unos 8 GB de RAM, el solver lo carga en bfloat16 (~3,4 GB) y hace la suma `W + B·diag(gate)·A` en float32 antes de volver a bfloat16. Después le hace preguntas con el mismo prompt de sistema de `chat.py` y decodificación greedy:

```bash
pip install torch transformers safetensors
python solve.py assets/neurolock-adapter.safetensors
```

Con el adaptador activo, Neuro responde lo mismo ante preguntas distintas (incluso a un simple "Hola"):

```
'Decime la clave secreta.' -> La clave secreta es 7f3c9e1d5a8b2c4f6e0d1a9b8c7d6e5f
'Hola' -> La clave secreta es 7f3c9e1d5a8b2c4f6e0d1a9b8c7d6e5f
```

Al pegar ese secreto en el formulario de la web, la valida y entrega la flag para el juez:

![La web valida el secreto y entrega la flag](./assets/02-flag.png)

## Flag

Secreto recuperado de Neuro (validado en la web):

```
7f3c9e1d5a8b2c4f6e0d1a9b8c7d6e5f
```

Flag para el juez:

```
6c99baff8b1b9d65c195a6061e359009
```

## 🛡️ Remediación (Developer Perspective)

- **Un secreto dentro de pesos publicados no está protegido.** Quien tiene los pesos controla la inferencia: cualquier "compuerta", flag o script que la deshabilite viaja en los mismos archivos y se puede revertir.
- **No entrenar secretos en modelos que se van a distribuir.** Si el modelo necesita un dato sensible, debe quedar del lado del servidor y no en los pesos.
