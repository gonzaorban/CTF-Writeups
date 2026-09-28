#!/usr/bin/env node
// Solver del Desafío 46 - Secure Chat (HackLab).
//
// Reproduce la lógica de verifyPin() del SecureChatService, extraída del
// bundle de la app Ionic/Angular (assets/public/2004.*.js dentro del APK).
//
// verifyPin(pin) descifra pinData -que es un blob en formato OpenSSL de
// CryptoJS ("Salted__" + salt + ciphertext), AES-256-CBC en modo passphrase
// con la derivación EVP_BytesToKey/MD5- usando el PIN como contraseña, y lo
// acepta si el texto descifrado tiene exactamente 32 caracteres.
//
// El PIN es de 4 dígitos (/^\d{4}$/), así que se fuerza el espacio completo
// 0000-9999. Solo una combinación produce un texto de 32 chars.
//
// Uso: node solve.js

const crypto = require('crypto');

// Blob embebido en el servicio (this.pinData).
const pinData =
  'U2FsdGVkX19fmBw92ecLtpE1bRwUFDL2lhCKJJLubM1TNgGCnLeE+ndbtICJBszUNjetOdtUPNwjMu6Hy4+d/A==';

// EVP_BytesToKey (MD5), tal como CryptoJS deriva key+IV desde passphrase+salt.
function evpKDF(password, salt, keyLen, ivLen) {
  let data = Buffer.alloc(0);
  let prev = Buffer.alloc(0);
  while (data.length < keyLen + ivLen) {
    prev = crypto
      .createHash('md5')
      .update(Buffer.concat([prev, Buffer.from(password, 'utf8'), salt]))
      .digest();
    data = Buffer.concat([data, prev]);
  }
  return { key: data.slice(0, keyLen), iv: data.slice(keyLen, keyLen + ivLen) };
}

function verifyPin(pin) {
  const raw = Buffer.from(pinData, 'base64');
  if (raw.slice(0, 8).toString() !== 'Salted__') return null; // marca de formato OpenSSL
  const salt = raw.slice(8, 16);
  const ct = raw.slice(16);
  const { key, iv } = evpKDF(pin, salt, 32, 16); // AES-256 => key de 32 bytes
  try {
    const d = crypto.createDecipheriv('aes-256-cbc', key, iv);
    return Buffer.concat([d.update(ct), d.final()]).toString('utf8');
  } catch {
    return null; // padding inválido => PIN incorrecto
  }
}

console.log('[*] Fuerza bruta del PIN de 4 dígitos (0000-9999)...\n');
for (let i = 0; i < 10000; i++) {
  const pin = String(i).padStart(4, '0');
  const out = verifyPin(pin);
  if (out !== null && out.length === 32) {
    console.log(`[+] PIN: ${pin}`);
    console.log(`[+] Felicitaciones: ${out}`);
  }
}
console.log('\n[*] Listo.');
