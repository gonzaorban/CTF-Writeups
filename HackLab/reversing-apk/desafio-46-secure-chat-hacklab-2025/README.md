# Desafío 46 - Secure Chat

**Plataforma:** HackLab (SoftwareSeguro)  
**Edición:** HackLab 2025  
**Categoría:** Reversing Apk - Fuerza bruta  

## Enunciado

> Te pasaron un APK que contiene chats sensibles cuya autenticación es vía PIN, ¿podrías abrirla para ver los chats?

Se entrega un único archivo, [`secure-chat.apk`](./assets/secure-chat.apk).

## Análisis

Un APK es un ZIP, así que se descomprime directamente. En la raíz aparecen
`assets/capacitor.config.json`, `assets/native-bridge.js` y una carpeta
`assets/public/` con un bundle de Angular (archivos `NNNN.hash.js` y un
`3rdpartylicenses.txt`). Es una **app híbrida Ionic/Angular empaquetada con
Capacitor** (`appId: com.hacklab.securechat`). El `classes.dex` de 8 MB es solo
el runtime de Capacitor: **la lógica de la app está en JavaScript**, sin cifrar,
dentro de `assets/public/`.

Esto define la estrategia: no hace falta emulador, root ni desensamblar Smali.
Alcanza con leer el bundle web.

Buscando en `assets/public/` por `pin`, `crypto`, `decrypt` y `flag`, todo
converge en un módulo (`2004.*.js`), que contiene el `SecureChatService`. Sus
constantes están todas hardcodeadas:

```javascript
this.xA = [72,65,67,75,76,65,66,95];   // "HACKLAB_"
this.xB = [67,84,70,95,50,48,50,53];   // "CTF_2025"
this.zA = 1735689600;                  // 2025-01-01T00:00:00Z
this.vA = [49,50,51,52,53,54,55,56,57,48,97,98,99,100,101,102]; // IV = "1234567890abcdef"
this.eData = "TFTuzneHsuen3ehVFmIcHj+RdjBesN175kvkvdQj+I8lLjBgmHhHAHKw27kwsbrs";
this.dA    = "TFTuzneHsuen3ehVFmIcHj+RdjBesN175kvkvdQj+I8lLjBgmHhHAHKw27kwsbrs";
this.pinData = "U2FsdGVkX19fmBw92ecLtpE1bRwUFDL2lhCKJJLubM1TNgGCnLeE+ndbtICJBszUNjetOdtUPNwjMu6Hy4+d/A==";
```

La función que autentica es `verifyPin`:

```javascript
verifyPin(r) {
  if (4 !== r.length || !/^\d{4}$/.test(r)) return console.log("PIN must be exactly 4 digits"), "";
  try {
    const F = u.AES.decrypt(this.pinData, r).toString(u.enc.Utf8);
    return 32 == F.length ? (console.log("Decrypted PIN data:", F), F || "") : "ESTE PIN NO TIENE TANTOS PRIVILEGIOS.";
  } catch { return console.log("Failed to decrypt PIN data with provided PIN"), ""; }
}
```

Es **CryptoJS**. `pinData` empieza (en Base64) con `U2FsdGVkX19f`, que decodifica
a `Salted__`: es el formato OpenSSL de CryptoJS, `"Salted__" + salt(8) + ciphertext`,
AES-256-CBC en **modo passphrase** (la clave y el IV se derivan del PIN y el salt con
`EVP_BytesToKey`/MD5). La función descifra `pinData` usando el PIN como contraseña y
lo acepta solo si el texto resultante mide **32 caracteres**.

El PIN es de **4 dígitos** (`/^\d{4}$/`), es decir 10 000 combinaciones: es
directamente fuerza bruta.

Los "chats sensibles" que muestra la app (`MessagesPage`, módulo `7231`) son
señuelos en texto plano hardcodeados ("Proyecto Alpha", "Seguridad", "Operaciones").
Lo que importa es lo que hace `ngOnInit` con el resultado de `verifyPin`:

```javascript
ngOnInit() {
  const s = history.state;
  s && s.result && (this.result = s.result,
    this.messages.push({ text: `Felicitaciones: ${this.result}`, isMine: !1, time: "Now" }));
}
```

Al ingresar el PIN correcto, la app muestra `Felicitaciones: <texto de 32 chars>`.
Ese texto de 32 caracteres es la flag.

## Enfoques descartados

- **Descifrar `eData`/`dA` con `getData(pin)`.** El servicio tiene una segunda ruta
  que deriva una clave `SHA256("HACKLAB_CTF_2025" + pin + "_" + 1735689600)` y con
  ella descifra `eData` (AES-CBC, IV `vA`). Pero `eData` es idéntico a `dA` y no
  produce texto legible: la clave que CryptoJS arma con esa cadena hex no es de un
  tamaño AES estándar, y el blob no descifra a nada útil. Es material de distracción;
  la autenticación real y funcional es `verifyPin`.

## Explotación

Se reproduce `verifyPin` con la librería `crypto` nativa de Node (sin dependencias):
se decodifica `pinData`, se extrae el salt, se deriva key+IV con `EVP_BytesToKey`/MD5
y se descifra en AES-256-CBC probando cada PIN de `0000` a `9999`, aceptando el que
devuelva 32 caracteres. El script completo es [`solve.js`](./solve.js); el núcleo es:

```javascript
const crypto = require('crypto');
const pinData = "U2FsdGVkX19fmBw92ecLtpE1bRwUFDL2lhCKJJLubM1TNgGCnLeE+ndbtICJBszUNjetOdtUPNwjMu6Hy4+d/A==";

function evpKDF(password, salt, keyLen, ivLen) {
  let data = Buffer.alloc(0), prev = Buffer.alloc(0);
  while (data.length < keyLen + ivLen) {
    prev = crypto.createHash('md5')
      .update(Buffer.concat([prev, Buffer.from(password, 'utf8'), salt])).digest();
    data = Buffer.concat([data, prev]);
  }
  return { key: data.slice(0, keyLen), iv: data.slice(keyLen, keyLen + ivLen) };
}

function verifyPin(pin) {
  const raw = Buffer.from(pinData, 'base64');       // "Salted__" + salt(8) + ct
  const salt = raw.slice(8, 16), ct = raw.slice(16);
  const { key, iv } = evpKDF(pin, salt, 32, 16);    // AES-256
  try {
    const d = crypto.createDecipheriv('aes-256-cbc', key, iv);
    return Buffer.concat([d.update(ct), d.final()]).toString('utf8');
  } catch { return null; }                          // padding inválido => PIN incorrecto
}

for (let i = 0; i < 10000; i++) {
  const pin = String(i).padStart(4, '0');
  const out = verifyPin(pin);
  if (out !== null && out.length === 32) console.log(`PIN=${pin} -> ${out}`);
}
```

Corriendo el solver:

```bash
node solve.js
```

```
[+] PIN: 5865
[+] Felicitaciones: b5c909a6f9fe6cf07530478d57cd7977
```

`5865` es el **único** PIN válido en todo el espacio de 4 dígitos, lo que confirma
que no es una colisión. Ese es el PIN con el que la app desbloquea, y el texto de 32
caracteres que revela es la flag.

## Flag

```
b5c909a6f9fe6cf07530478d57cd7977
```
