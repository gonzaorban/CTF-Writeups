# El arreglo que nos escupió el binario
encoded_values = [784, 735, 693, 777, 469, 588, 490, 861, 714, 679, 749, 707, 665, 714, 756, 679, 721, 875]

# La llave (tu respuesta matemática)
key = 7

flag = ""
for num in encoded_values:
    # División entera para recuperar el valor ASCII original
    ascii_val = num // key
    # Conversión de decimal a caracter
    flag += chr(ascii_val)

print(f"La flag descubierta es: {flag}")