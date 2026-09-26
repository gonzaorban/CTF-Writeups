// Configuración simple
const d = (sel) => document.querySelector(sel);
const messages = d('#messages');
const roomInput = d('#room');
const nickInput = d('#nick');
const passInput = d('#password'); // <-- nuevo: password
const connectBtn = d('#connect');
const sendBtn = d('#send');
const textInput = d('#text');
const buzzBtn = d('#buzz');

const BUZZ_COOLDOWN_MS = 10_000;
let lastBuzzAt = 0;
let buzzCooldownTimer = null;
let buzzOriginalLabel = null;

let pc = null;
let dc = null;
let ws = null;
let connected = false;

const ICE_SERVERS = [
    {urls: 'stun:stun.l.google.com:19302'},
    {urls: "stun:a.relay.metered.ca:80"},
    {urls: "turn:a.relay.metered.ca:80", username: "01bc295f6f92de9f09f9df5c", credential: "p3ZSquLPysgGlAnf"},
    {urls: "turn:a.relay.metered.ca:80?transport=tcp", username: "01bc295f6f92de9f09f9df5c", credential: "p3ZSquLPysgGlAnf"},
    {urls: "turn:a.relay.metered.ca:443", username: "01bc295f6f92de9f09f9df5c", credential: "p3ZSquLPysgGlAnf"},
    {urls: "turn:a.relay.metered.ca:443?transport=tcp", username: "01bc295f6f92de9f09f9df5c", credential: "p3ZSquLPysgGlAnf"},
];

// --- efecto visual del zumbido ---
function showBuzzEffect(origin = 'peer') {
    const win = document.querySelector('.msn-window');
    if (!win) return;

    // Evita superposiciones de timers
    if (win._buzzTimer) clearTimeout(win._buzzTimer);

    win.classList.add('shake');

    // Vibración opcional (si está disponible, útil en mobile)
    try {
        if (navigator.vibrate) navigator.vibrate([80, 40, 80]);
    } catch (_) {}

    win._buzzTimer = setTimeout(() => {
        win.classList.remove('shake');
        win._buzzTimer = null;
    }, 600);
}

// Limpia cooldown al cerrar el DC (defensivo)
function resetBuzzCooldown() {
    if (buzzCooldownTimer) {
        clearTimeout(buzzCooldownTimer);
        buzzCooldownTimer = null;
    }
    if (buzzBtn) {
        buzzBtn.textContent = buzzOriginalLabel || 'Zumbido';
        buzzBtn.disabled = true; // se re-habilita cuando el DC abra
    }
    lastBuzzAt = 0;
}

function isDataChannelOpen() {
    return dc && dc.readyState === 'open';
}

function msToSec(ms) {
    return Math.ceil(ms / 1000);
}

function startBuzzCooldown() {
    if (!buzzBtn) return;

    // Deshabilitar botón y mostrar cuenta regresiva
    buzzBtn.disabled = true;
    if (!buzzOriginalLabel) buzzOriginalLabel = buzzBtn.textContent;

    const tick = () => {
        const now = Date.now();
        const left = BUZZ_COOLDOWN_MS - (now - lastBuzzAt);
        if (left <= 0) {
            buzzBtn.textContent = buzzOriginalLabel || 'Zumbido';
            buzzBtn.disabled = false;
            buzzCooldownTimer = null;
            return;
        }
        buzzBtn.textContent = `Zumbido (${msToSec(left)}s)`;
        buzzCooldownTimer = setTimeout(tick, 200);
    };

    // primera actualización inmediata
    tick();
}

// --- enviar zumbido ---
// === Reemplazá tu función sendBuzz por esta ===
function sendBuzz() {
    if (!isDataChannelOpen()) {
        logSys('No hay conexión para enviar zumbido.');
        return;
    }

    const now = Date.now();
    const elapsed = now - lastBuzzAt;
    if (elapsed < BUZZ_COOLDOWN_MS) {
        const left = BUZZ_COOLDOWN_MS - elapsed;
        logSys(`Esperá ${msToSec(left)}s para volver a enviar un zumbido.`);
        // Aseguramos que el botón quede bloqueado con countdown
        startBuzzCooldown();
        return;
    }

    const nick = (safeNick() || 'Yo').slice(0, 20);
    const payload = { type: 'buzz', nick, t: now };

    try {
        dc.send(JSON.stringify(payload));
    } catch (e) {
        logSys('No se pudo enviar el zumbido.');
        return;
    }

    addMessage('Yo', '— zumbido —', 'me buzz');
    showBuzzEffect('me');
    document.querySelector('#snd-out')?.play().catch(() => {});

    // Marcar inicio de cooldown
    lastBuzzAt = now;
    startBuzzCooldown();
}


function logSys(msg) {
    addMessage('Sistema', msg, 'sys');
}

function addMessage(author, text, cls) {
    const div = document.createElement('div');
    div.className = `msg ${cls}`;
    const meta = document.createElement('div');
    meta.className = 'meta';
    const time = new Date().toLocaleTimeString();
    meta.textContent = `${author} — ${time}`;
    const body = document.createElement('div');
    body.textContent = text;
    div.append(meta, body);
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

function safeNick() {
    let n = (nickInput.value || '').trim();
    if (!n) return null;
    return n.slice(0, 20);
}

// Valida y compone el nombre de la sala: <dominio>-<room>
function getComposedRoom() {
    const raw = (roomInput.value || '').trim();
    // Requisito: largo entre 5 y 10
    if (raw.length < 5 || raw.length > 10) {
        logSys('El nombre de la sala (#room) debe tener entre 5 y 10 caracteres.');
        return null;
    }
    const domain = location.hostname || 'localhost';
    return `${domain}-${raw}`;
}

function ensurePC() {
    if (pc) return pc;
    pc = new RTCPeerConnection({ iceServers: ICE_SERVERS });

    pc.onicecandidate = (e) => {
        if (e.candidate) {
            sendWS({ type: 'ice-candidate', candidate: e.candidate });
        }
    };

    pc.ondatachannel = (e) => {
        dc = e.channel;
        wireDataChannel();
    };

    pc.onconnectionstatechange = () => {
        if (pc.connectionState === 'connected') {
            logSys('Remoto conectado');
        }
        if (['disconnected', 'failed', 'closed'].includes(pc.connectionState)) {
            //logSys(`Estado: ${pc.connectionState}`);
        }
    };

    return pc;
}

function wireDataChannel() {
    if (!dc) return;
    dc.onopen = () => {
        connected = true;
        // si tenés bloqueado el input/botón en el HTML, podés habilitarlos acá:
        textInput.disabled = false;
        sendBtn.disabled = false;
        buzzBtn.disabled = false;
        if (buzzCooldownTimer) {
            clearTimeout(buzzCooldownTimer); buzzCooldownTimer = null;
        }
        buzzBtn.textContent = buzzOriginalLabel || 'Zumbido';
    };
    dc.onclose = () => {
        connected = false;
        textInput.disabled = true;
        sendBtn.disabled = true;
        buzzBtn.disabled = true;
        resetBuzzCooldown();
    };
    dc.onmessage = (e) => {
        const payload = JSON.parse(e.data);

        // Soporte “buzz” (y compat con mensajes antiguos)
        if (payload?.type === 'buzz' || payload?.text === '__buzz__') {
            addMessage(payload.nick || 'Peer', '— zumbido —', 'peer buzz');
            showBuzzEffect('peer');
            document.querySelector('#snd-in')?.play().catch(() => {});
            return;
        }

        addMessage(payload.nick || 'Peer', payload.text, 'peer');
        // sonido entrada (en mute por defecto, el base64 es silencioso)
        d('#snd-in').play().catch(() => { });
    };
}

function connectWS() {
    //const wsUrl = 'wss://direct-chat.shared.softwareseguro.com.ar/ws';
    const wsUrl = 'wss://direct-chat.shared.softwareseguro.com.ar/ws';

    // 1) Componer room con <dominio>-<room> y validar longitud
    const composedRoom = getComposedRoom();
    if (!composedRoom) return;

    // 3) Pasar nick y password como parámetros también
    const nick = safeNick(); // ya lo pedía tu flujo
    const password = (passInput && passInput.value) ? passInput.value : '';

    const params = new URLSearchParams({
        room: composedRoom,
        nick: nick || '',      // el server validará
        password: password     // el server validará
    });

    const url = `${wsUrl}?${params.toString()}`;
    ws = new WebSocket(url);

    ws.onopen = async () => {
        logSys('Conectado');



        // rol: el primero que entra suele crear la offer
        await createOffer();
    };

    ws.onmessage = async (evt) => {
        const data = JSON.parse(evt.data);

        if (data.type === 'peers') {
            return;
        }

        switch (data.type) {
            case 'offer':
                await handleOffer(data);
                break;
            case 'answer':
                await handleAnswer(data);
                break;
            case 'ice-candidate':
                if (pc) await pc.addIceCandidate(data.candidate);
                break;
            case 'bye':
                logSys('El remoto se desconectó');
                break;
        }
    };

    ws.onclose = () => logSys('Desconectado');
    ws.onerror = () => logSys('Error en señalización');
}

function sendWS(obj) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(obj));
    }
}

async function createOffer() {
    const pcx = ensurePC();
    if (!dc) {
        dc = pcx.createDataChannel('chat');
        wireDataChannel();
    }
    const offer = await pcx.createOffer();
    await pcx.setLocalDescription(offer);
    sendWS({ type: 'offer', sdp: offer });
}

async function handleOffer({ sdp }) {
    const pcx = ensurePC();
    await pcx.setRemoteDescription(new RTCSessionDescription(sdp));
    const answer = await pcx.createAnswer();
    await pcx.setLocalDescription(answer);
    sendWS({ type: 'answer', sdp: answer });
}

async function handleAnswer({ sdp }) {
    if (!pc) return;
    await pc.setRemoteDescription(new RTCSessionDescription(sdp));
}

function sendMessage() {
    const text = textInput.value.trim();
    if (!text) return;
    if (!dc || dc.readyState !== 'open') {
        logSys('No hay nadie más conectado a la sala o no estás conectado a una.');
        return;
    }
    const payload = { nick: safeNick(), text };
    dc.send(JSON.stringify(payload));
    addMessage('Yo', text, 'me');
    textInput.value = '';
    d('#snd-out').play().catch(() => { });
}

// UI
connectBtn.addEventListener('click', () => {
    let nick = safeNick();
    if (nick != null) {
        if (ws && ws.readyState === WebSocket.OPEN) {
            logSys('Ya estás conectado.');
            return;
        }
        connectWS();
    } else {
        logSys('No es posible conectarse sin nick.');
    }
});

sendBtn.addEventListener('click', sendMessage);
textInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

buzzBtn?.addEventListener('click', sendBuzz);

// Defaults para pruebas locales
roomInput.value = '';
nickInput.value = '';
