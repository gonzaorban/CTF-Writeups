from cryptography.fernet import Fernet

# La llave en Base64 que extrajimos del main.js
key = b"cGljb0NURnt5b3UncmUgb24gdGhlIHJpZ2h0IHRyYX0="

# Inicializamos el objeto de descifrado Fernet
f = Fernet(key)

# El webhook encriptado (nuestro "token")
encrypted_webhook = b"gAAAAABmfRjwFKUB-X3GBBqaN1tZYcPg5oLJVJ5XQHFogEgcRSxSis1e4qwicAKohmjqaD-QG8DIN5ie3uijCVAe3xiYmoEHlxATWUP3DC97R00Cgkw4f3HZKsP5xHewOqVPH8ap9FbE"

# Desencriptamos y decodificamos a string
decrypted = f.decrypt(encrypted_webhook)
print(f"El Webhook descifrado es: {decrypted.decode()}")