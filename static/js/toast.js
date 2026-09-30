/* A short-lived notice in the corner of the screen. Lives in the browser's top
   layer through the popover API, so it stays above the delete and form modals
   instead of fighting them over a z-index. */

let toastTimer;

function showToast(title, message, type = "normal", duration = 3000) {
    const toast = document.getElementById("toast-component");
    if (!toast) return;

    toast.classList.remove("toast-success", "toast-error", "toast-normal");
    toast.classList.add("toast-" + (["success", "error"].includes(type) ? type : "normal"));

    document.getElementById("toast-title").textContent = title;
    document.getElementById("toast-message").textContent = message;

    // A toast that arrives while the previous one is still on screen restarts
    // the clock rather than inheriting the time left on it.
    clearTimeout(toastTimer);

    if (!toast.matches(":popover-open")) {
        toast.showPopover();
        void toast.offsetHeight;  // force a reflow so the transition has a start value
    }
    toast.classList.remove("toast-hidden");
    toast.classList.add("toast-show");

    toastTimer = setTimeout(() => {
        toast.classList.remove("toast-show");
        toast.classList.add("toast-hidden");
        toastTimer = setTimeout(() => toast.hidePopover(), 300);
    }, duration);
}
