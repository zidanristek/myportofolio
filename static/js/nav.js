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

/* Wraps the experience carousel. One clone sits at each end, so the last card
   is already visible to the left of the first, and the moment the scroll
   settles on a clone the position jumps to the real card behind it. The jump
   is the width of the whole real run, so nothing appears to move. */

(function () {
    "use strict";

    var track = document.getElementById("experience-track");
    if (!track) {
        return;
    }

    var cards = [].slice.call(track.querySelectorAll(".experience-card"));
    if (cards.length < 2) {
        return;
    }

    /* A clone carries its buttons, so the edit link and the delete dialog work
       from either end of the loop. Ids have to be made unique first, because
       popovertarget resolves to whichever element it finds first and two
       dialogs sharing a name means one of them never opens. */

    var copies = 0;

    function twin(card) {
        var copy = card.cloneNode(true);
        var suffix = "-loop" + (copies += 1);

        [].forEach.call(copy.querySelectorAll("[id]"), function (node) {
            node.id += suffix;
        });
        ["popovertarget", "aria-labelledby", "aria-controls", "for"].forEach(function (attr) {
            [].forEach.call(copy.querySelectorAll("[" + attr + "]"), function (node) {
                node.setAttribute(attr, node.getAttribute(attr) + suffix);
            });
        });

        return copy;
    }

    function step() {
        var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
        return cards[0].offsetWidth + gap;
    }

    function run() {
        return cards.length * step();
    }

    /* How many copies each side has to reach past the edge of the viewport.
       One is enough at laptop width, but a zoomed-out page is wider than the
       whole run and would show the track ending. */

    function needed() {
        return Math.max(1, Math.ceil(track.clientWidth / run()));
    }

    var built = 0;

    function build(count) {
        while (built < count) {
            var before = document.createDocumentFragment();
            var after = document.createDocumentFragment();

            cards.forEach(function (card) {
                before.appendChild(twin(card));
                after.appendChild(twin(card));
            });

            track.insertBefore(before, track.firstChild);
            track.appendChild(after);
            built += 1;
        }
    }

    function centre() {
        return built * run();
    }

    function jump(to) {
        var behaviour = track.style.scrollBehavior;
        track.style.scrollBehavior = "auto";
        track.scrollLeft = to;
        track.style.scrollBehavior = behaviour;
    }

    /* The list repeats every run, so stepping back by one run lands on the same
       card in the copy nearer the middle. Nothing on screen moves. */

    function wrap() {
        var span = run();
        var drift = track.scrollLeft - centre();

        if (Math.abs(drift) > span / 2) {
            jump(track.scrollLeft - Math.round(drift / span) * span);
        }
    }

    build(needed());
    requestAnimationFrame(function () {
        jump(centre());
    });

    if ("onscrollend" in window) {
        track.addEventListener("scrollend", wrap);
    } else {
        var idle;
        track.addEventListener("scroll", function () {
            clearTimeout(idle);
            idle = setTimeout(wrap, 120);
        }, { passive: true });
    }

    window.addEventListener("resize", function () {
        build(needed());
        jump(centre());
    }, { passive: true });
})();
