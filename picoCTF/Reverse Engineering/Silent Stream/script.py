from scapy.all import rdpcap, TCP, Raw

# 1. Leemos el archivo PCAP
print("[*] Leyendo packets.pcap...")
packets = rdpcap('packets.pcap')

# 2. Extraemos el payload crudo de los paquetes del atacante
raw_data = b''
for pkt in packets:
    # Filtramos para asegurarnos de que tengan capa TCP, Payload (Raw) y vengan del atacante
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        if pkt['IP'].src == '10.10.10.10':
            raw_data += pkt[Raw].load

print(f"[*] Se extrajeron {len(raw_data)} bytes cifrados.")

# 3. Aplicamos la matemática inversa: (byte - 42) % 256
key = 42
decrypted_data = bytearray()
for b in raw_data:
    decrypted_byte = (b - key) % 256
    decrypted_data.append(decrypted_byte)

# 4. Guardamos el archivo reconstruido
output_file = 'reconstructed_flag.txt'
with open(output_file, 'wb') as f:
    f.write(decrypted_data)

print(f"[+] Archivo descifrado guardado exitosamente como '{output_file}'")