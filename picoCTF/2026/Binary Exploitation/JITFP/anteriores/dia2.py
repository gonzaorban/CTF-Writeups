import os
import pty
import time
import subprocess
import string

# --- CONFIGURACIÓN ---
# Invocamos el linker para bypassear la restricción 'noexec' de /dev/shm/
BINARY_CMD = ["/lib/ld-musl-x86_64.so.1", "./ad7e550b"] 
FLAG_LENGTH = 33
KNOWN_PREFIX = "picoCTF{"
ALPHABET = string.ascii_letters + string.digits + "_-}"

def test_flag(test_str):
    """
    Envía una bandera y retorna en qué índice se detectó la penalización.
    """
    master, slave = pty.openpty()
    
    # Iniciamos el proceso conectado al PTY para forzar unbuffered stdout
    p = subprocess.Popen(
        BINARY_CMD,
        stdin=slave,
        stdout=slave,
        stderr=slave,
        close_fds=True
    )
    os.close(slave)
    
    # Enviamos el payload completo (33 chars) + salto de línea
    os.write(master, (test_str + "\n").encode())
    
    asterisk_times = []
    
    try:
        # Esperamos leer hasta 33 asteriscos
        while len(asterisk_times) < FLAG_LENGTH:
            char = os.read(master, 1).decode(errors='ignore')
            
            if char == '*':
                current_time = time.time()
                asterisk_times.append(current_time)
                
                # Si tenemos al menos 2 asteriscos, comparamos el tiempo entre ellos
                if len(asterisk_times) > 1:
                    delta = asterisk_times[-1] - asterisk_times[-2]
                    
                    # Si el delta supera 1.5s, caimos en FUN_00101932 (la penalización)
                    if delta > 1.5:
                        p.kill() # ¡CRÍTICO! Matamos el proceso para ahorrar recursos del server
                        os.close(master)
                        return len(asterisk_times) - 1 # Índice de la letra que falló
                        
    except Exception as e:
        # Manejo por si el proceso muere o explota (Segmentation fault)
        pass 
        
    p.kill()
    os.close(master)
    return len(asterisk_times) # Si llega acá sin saltos de tiempo, encontramos la flag

def brute_force():
    current_flag = KNOWN_PREFIX
    
    print(f"[*] Iniciando ataque PTY JIT-Bypass...")
    print(f"[*] Bandera actual: {current_flag}")
    
    # Bucle hasta completar los 33 caracteres
    while len(current_flag) < FLAG_LENGTH:
        if len(current_flag) == FLAG_LENGTH - 1:
            # El último caracter suele ser '}'
            current_flag += "}"
            print(f"[+] FLAG ENCONTRADA: {current_flag}")
            break
            
        found_char = False
        
        for char in ALPHABET:
            # Rellenamos el resto con 'A' para cumplir la longitud de 33
            padding_length = FLAG_LENGTH - len(current_flag) - 1
            test_str = current_flag + char + ("A" * padding_length)
            
            # Ajustamos el string si termina sin '}' para evitar segfaults raros (opcional)
            test_str = test_str[:-1] + "}"
            
            # Probamos la letra
            fail_index = test_flag(test_str)
            
            # Si el fail_index es mayor a la longitud actual de nuestra flag conocida,
            # significa que pasamos la validación de la letra actual.
            if fail_index > len(current_flag):
                current_flag += char
                print(f"[+] Letra descubierta: '{char}' -> {current_flag}")
                found_char = True
                break
                
        if not found_char:
            print("[-] No se encontró la siguiente letra. Revisa los tiempos de tolerancia (delta).")
            break

if __name__ == "__main__":
    brute_force()