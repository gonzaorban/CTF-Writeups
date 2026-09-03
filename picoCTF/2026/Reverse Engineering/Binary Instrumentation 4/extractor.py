import pefile
import os

print("[*] Iniciando autopsia del archivo PE...")
try:
    pe = pefile.PE("bin-ins.exe")
except Exception as e:
    print(f"[-] Error al abrir el ejecutable: {e}")
    exit()

# Recorremos todas las secciones del ejecutable
for section in pe.sections:
    # Limpiamos el nombre de la sección (vienen con bytes nulos al final)
    name = section.Name.decode('utf-8', 'ignore').strip('\x00')
    
    # Ignoramos si la sección está vacía
    if section.SizeOfRawData == 0:
        continue
        
    print(f"[+] Extrayendo sección: {name} | Tamaño: {section.SizeOfRawData} bytes")
    
    # Guardamos el contenido crudo (los bytes) en un archivo nuevo
    filename = f"seccion_{name}.bin"
    with open(filename, "wb") as f:
        f.write(section.get_data())

print("\n[!] Autopsia finalizada. Revisá los archivos generados.")