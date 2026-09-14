/* Two jobs for the hero: scatter the stars, and drift each sky layer at its
   own speed while the page scrolls. */

(function () {
    "use strict";

    var REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    /* Writing 70 fixed dots into the template would bury the markup, so they
       are generated once on load. CSS owns the twinkle. */

    var sky = document.getElementById("stars");

    if (sky) {
        var batch = document.createDocumentFragment();

        for (var i = 0; i < 70; i++) {
            var star = document.createElement("i");
            var size = (Math.random() * 1.6 + 1).toFixed(1);

            star.style.left = (Math.random() * 100).toFixed(2) + "%";
            star.style.top = (Math.random() * 62).toFixed(2) + "%";
            star.style.width = size + "px";
            star.style.height = size + "px";
            star.style.animationDelay = (Math.random() * 4).toFixed(2) + "s";

            batch.appendChild(star);
        }

        sky.appendChild(batch);
    }

    /* Parallax. A smaller data-speed means a layer sits further away and so
       moves slower than the ones in front of it. */

    var layers = [].slice.call(document.querySelectorAll("[data-speed]"));

    if (REDUCED || layers.length === 0) {
        return;
    }

    var hero = document.querySelector(".hero");
    var ticking = false;

    function draw() {
        ticking = false;

        var y = window.pageYOffset;

        /* Stop once the hero has left the viewport, otherwise this keeps
           working for the whole rest of the page for nothing. */
        if (hero && y > hero.offsetHeight) {
            return;
        }

        for (var i = 0; i < layers.length; i++) {
            var shift = y * parseFloat(layers[i].getAttribute("data-speed"));
            layers[i].style.transform = "translate3d(0," + shift.toFixed(1) + "px,0)";
        }
    }

    window.addEventListener("scroll", function () {
        if (!ticking) {
            ticking = true;
            window.requestAnimationFrame(draw);
        }
    }, { passive: true });

    draw();
})();
