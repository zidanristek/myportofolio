/* The navbar gets out of the way on scroll down and returns on scroll up, so
   short screens do not lose a strip of content to it. */

(function () {
    "use strict";

    var nav = document.querySelector(".nav");
    if (!nav) {
        return;
    }

    var THRESHOLD = 12;   /* smaller moves are ignored, which stops the flicker */
    var START = 140;      /* near the top the navbar always shows */

    var lastY = window.pageYOffset;
    var ticking = false;

    function check() {
        ticking = false;

        var y = window.pageYOffset;
        var delta = y - lastY;

        if (Math.abs(delta) < THRESHOLD) {
            return;
        }

        nav.classList.toggle("is-hidden", delta > 0 && y > START);
        lastY = y;
    }

    window.addEventListener("scroll", function () {
        if (!ticking) {
            ticking = true;
            window.requestAnimationFrame(check);
        }
    }, { passive: true });
})();

/* Narrow-screen menu: the burger opens a panel, and while that panel is open
   the page behind it is locked against scrolling. */

(function () {
    "use strict";

    var burger = document.getElementById("burger");
    var menu = document.getElementById("nav-menu");

    if (!burger || !menu) {
        return;
    }

    function setOpen(open) {
        burger.setAttribute("aria-expanded", open ? "true" : "false");
        burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
        menu.classList.toggle("is-closed", !open);
        document.body.classList.toggle("menu-open", open);
    }

    burger.addEventListener("click", function () {
        setOpen(burger.getAttribute("aria-expanded") !== "true");
    });

    /* A link, the padding around it, or anything outside the panel all close
       it. Without that the page stays locked after the reader jumps away. */
    document.addEventListener("click", function (e) {
        if (burger.contains(e.target)) {
            return;
        }
        if (!menu.contains(e.target) || e.target === menu || e.target.closest("a")) {
            setOpen(false);
        }
    });

    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") {
            setOpen(false);
        }
    });
})();

/* The experience carousel scrolls itself on touch and trackpad. These arrows
   are there for a plain mouse, which has no sideways gesture. */

(function () {
    "use strict";

    var track = document.getElementById("experience-track");
    if (!track) {
        return;
    }

    var slide = track.querySelector(".experience-card");
    if (!slide) {
        return;
    }

    document.querySelectorAll(".carousel-arrow").forEach(function (button) {
        button.addEventListener("click", function () {
            var step = parseInt(button.getAttribute("data-step"), 10);
            track.scrollBy({ left: step * (slide.offsetWidth + 24), behavior: "smooth" });
        });
    });
})();
