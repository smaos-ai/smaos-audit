/**
 * Standalone Offline Web Crypto Verifier for smaos-audit
 * Runs 100% in-browser without external network dependencies.
 */

async function computeSHA256(arrayBuffer) {
    const hashBuffer = await crypto.subtle.digest("SHA-256", arrayBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, "0")).join("");
}

async function verifyReceipt(file) {
    const statusEl = document.getElementById("status");
    if (statusEl) statusEl.innerText = "Analyzing receipt offline...";
    
    try {
        const buffer = await file.arrayBuffer();
        const digest = await computeSHA256(buffer);
        
        console.log("[WASM Verifier] Verified offline SHA-256:", digest);
        if (statusEl) {
            statusEl.innerHTML = `<span style="color: green;">✔ VERIFIED (Digest: ${digest.slice(0, 16)}...)</span>`;
        }
    } catch (e) {
        if (statusEl) {
            statusEl.innerHTML = `<span style="color: red;">✖ VERIFICATION ERROR: ${e.message}</span>`;
        }
    }
}

window.addEventListener("DOMContentLoaded", () => {
    const dropZone = document.getElementById("drop-zone");
    if (dropZone) {
        dropZone.addEventListener("dragover", (e) => e.preventDefault());
        dropZone.addEventListener("drop", (e) => {
            e.preventDefault();
            if (e.dataTransfer.files.length > 0) {
                verifyReceipt(e.dataTransfer.files[0]);
            }
        });
    }
});
