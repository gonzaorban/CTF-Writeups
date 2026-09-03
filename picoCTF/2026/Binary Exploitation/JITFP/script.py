import os
import pty
import time
import subprocess
import string
import statistics
import select

# --- CONFIGURACIÓN ---
BINARY_PATH = "/home/ctf-player/ad7e550b"
FLAG_LENGTH = 33
KNOWN_PREFIX = "picoCTF{"
# Ponemos letras minúsculas y mayúsculas primero para optimizar aciertos
ALPHABET = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_-}"
SAMPLES_PER_CHAR = 4

def measure_asterisk_delta(test_flag, target_idx):
    """
    Ejecuta el binario usando un PTY y pasando la flag como argumento.
    Mide el tiempo entre el asterisco anterior y el target_idx.
    """
    master, slave = pty.openpty()
    
    # Pasamos la flag como argumento en la lista
    p = subprocess.Popen(
        [BINARY_PATH, test_flag],
        stdout=slave,
        stderr=subprocess.DEVNULL,
        close_fds=True
    )
    os.close(slave)
    
    times = []
    asterisks_read = 0
    delta = 0
    
    try:
        # Leemos hasta obtener el asterisco de la letra que estamos adivinando
        while asterisks_read <= target_idx:
            # select evita que el script se quede colgado esperando infinitamente
            r, _, _ = select.select([master], [], [], 2.5)
            if r:
                char = os.read(master, 1).decode(errors='ignore')
                if char == '*':
                    times.append(time.perf_counter())
                    asterisks_read += 1
            else:
                # Timeout: el binario dejó de escupir datos
                break
                
        # Calculamos la diferencia de tiempo entre los últimos dos asteriscos leídos
        if len(times) >= 2:
            delta = times[-1] - times[-2]
            
    except Exception as e:
        pass
        
    finally:
        # Limpieza absoluta de procesos para no tirar el server
        p.kill()
        p.wait() 
        os.close(master)
        
    return delta

def main():
    current_flag = KNOWN_PREFIX
    print("[*] Iniciando ataque Híbrido (Argumento + PTY)...")
    
    while len(current_flag) < FLAG_LENGTH:
        if len(current_flag) == FLAG_LENGTH - 1:
            current_flag += "}"
            print(f"\n[+] FLAG COMPLETADA: {current_flag}")
            break
            
        target_index = len(current_flag)
        print(f"\n[*] Adivinando posición {target_index} (Progreso: {current_flag})...")
        
        char_times = {}
        
        for char in ALPHABET:
            # Rellenamos hasta 33 caracteres
            padding = FLAG_LENGTH - len(current_flag) - 1
            test_str = current_flag + char + ("A" * padding)
            test_str = test_str[:-1] + "}"
            
            deltas = []
            for _ in range(SAMPLES_PER_CHAR):
                d = measure_asterisk_delta(test_str, target_index)
                if d > 0:
                    deltas.append(d)
            
            # Mediana para ignorar lag spikes del servidor
            if deltas:
                char_times[char] = statistics.median(deltas)
            else:
                char_times[char] = 0
                
        # Ordenamos los resultados: el mayor tiempo primero
        sorted_times = sorted(char_times.items(), key=lambda x: x[1], reverse=True)
        
        print("    Top 3 tiempos:")
        for i in range(3):
            if i < len(sorted_times):
                c, t = sorted_times[i]
                print(f"    -> '{c}': {t:.5f} seg")
                
        # Seleccionamos la letra que tardó más
        best_char = sorted_times[0][0]
        current_flag += best_char
        print(f"[+] Letra elegida: '{best_char}' -> {current_flag}")

if __name__ == "__main__":
    main()