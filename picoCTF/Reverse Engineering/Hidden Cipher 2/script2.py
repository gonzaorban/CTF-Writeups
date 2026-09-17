# El arreglo que nos escupió el binario
encoded_values = [1008, 945, 891, 999, 603, 756, 630, 1107, 981, 468, 1044, 936, 855, 882, 459, 936, 441, 990, 900, 855, 891, 441, 1008, 936, 459, 1026, 855, 873, 909, 891, 486, 450, 495, 468, 882, 1125
]

# La llave (tu respuesta matemática)
key = 9

flag = ""
for num in encoded_values:
    # División entera para recuperar el valor ASCII original
    ascii_val = num // key
    # Conversión de decimal a caracter
    flag += chr(ascii_val)

print(f"La flag descubierta es: {flag}")