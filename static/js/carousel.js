/* The experience carousel. Its cards now arrive from the JSON endpoint, so
   this runs again after every render instead of once at load. Each run aborts
   the listeners the run before it registered. */

var carouselRun;

function initExperienceCarousel() {
    "use strict";

    if (carouselRun) {
        carouselRun.abort();
    }
    carouselRun = new AbortController();
    var signal = carouselRun.signal;

    var track = document.getElementById("experience-track");
    if (!track) {
        return;
    }

    var cards = [].slice.call(track.querySelectorAll(".experience-card"));
    if (!cards.length) {
        return;
    }

    /* The track scrolls itself on touch and trackpad. These arrows are there
       for a plain mouse, which has no sideways gesture. */

    document.querySelectorAll(".carousel-arrow").forEach(function (button) {
        button.addEventListener("click", function () {
            var direction = parseInt(button.getAttribute("data-step"), 10);
            track.scrollBy({ left: direction * step(), behavior: "smooth" });
        }, { signal: signal });
    });

    if (cards.length < 2) {
        return;
    }

    /* One clone sits at each end, so the last card is already visible to the
       left of the first, and the moment the scroll settles on a clone the
       position jumps to the real card behind it. The jump is the width of the
       whole real run, so nothing appears to move. */

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
        track.addEventListener("scrollend", wrap, { signal: signal });
    } else {
        var idle;
        track.addEventListener("scroll", function () {
            clearTimeout(idle);
            idle = setTimeout(wrap, 120);
        }, { passive: true, signal: signal });
    }

    window.addEventListener("resize", function () {
        build(needed());
        jump(centre());
    }, { passive: true, signal: signal });
}

document.addEventListener("DOMContentLoaded", initExperienceCarousel);
