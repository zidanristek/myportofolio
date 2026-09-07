/* Dua hal untuk hero: menaburkan bintang, dan menggeser tiap lapisan langit
   dengan kecepatan berbeda saat halaman digulir. */

(function () {
    "use strict";

    var HALUS = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    /* Bintang. Menulis 70 titik tetap ke dalam template akan mengubur markup,
       jadi dibuat sekali saat halaman dimuat. Kedipannya diserahkan ke CSS. */

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

    /* Parallax. Lapisan yang lebih jauh diberi data-speed lebih kecil, jadi
       bergerak lebih lambat dari lapisan depan. */

    var layers = [].slice.call(document.querySelectorAll("[data-speed]"));

    if (HALUS || layers.length === 0) {
        return;
    }

    var hero = document.querySelector(".hero");
    var menunggu = false;

    function gambar() {
        menunggu = false;

        var y = window.pageYOffset;

        /* Berhenti menggeser begitu hero lewat dari layar, supaya tidak ada
           kerja sia-sia sepanjang sisa halaman. */
        if (hero && y > hero.offsetHeight) {
            return;
        }

        for (var i = 0; i < layers.length; i++) {
            var jauh = y * parseFloat(layers[i].getAttribute("data-speed"));
            layers[i].style.transform = "translate3d(0," + jauh.toFixed(1) + "px,0)";
        }
    }

    window.addEventListener("scroll", function () {
        if (!menunggu) {
            menunggu = true;
            window.requestAnimationFrame(gambar);
        }
    }, { passive: true });

    gambar();
})();
