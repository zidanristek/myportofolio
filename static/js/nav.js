/* Navbar menyingkir saat pembaca menggulir turun dan kembali saat menggulir
   naik, supaya isi halaman tidak terpotong di layar pendek. */

(function () {
    "use strict";

    var nav = document.querySelector(".nav");
    if (!nav) {
        return;
    }

    var AMBANG = 12;      /* gerakan di bawah ini diabaikan, cegah kedip */
    var MULAI = 140;      /* di puncak halaman navbar selalu tampak */

    var terakhir = window.pageYOffset;
    var menunggu = false;

    function periksa() {
        menunggu = false;

        var y = window.pageYOffset;
        var beda = y - terakhir;

        if (Math.abs(beda) < AMBANG) {
            return;
        }

        nav.classList.toggle("is-hidden", beda > 0 && y > MULAI);
        terakhir = y;
    }

    window.addEventListener("scroll", function () {
        if (!menunggu) {
            menunggu = true;
            window.requestAnimationFrame(periksa);
        }
    }, { passive: true });
})();

/* Menu layar sempit: tombol tiga garis membuka panel, dan selama panel terbuka
   halaman di belakangnya dikunci supaya tidak ikut tergulir. */

(function () {
    "use strict";

    var burger = document.getElementById("burger");
    var menu = document.getElementById("nav-menu");

    if (!burger || !menu) {
        return;
    }

    function setel(buka) {
        burger.setAttribute("aria-expanded", buka ? "true" : "false");
        burger.setAttribute("aria-label", buka ? "Close menu" : "Open menu");
        menu.classList.toggle("is-closed", !buka);
        document.body.classList.toggle("menu-open", buka);
    }

    burger.addEventListener("click", function () {
        setel(burger.getAttribute("aria-expanded") !== "true");
    });

    /* Tautan di dalam panel menutup panelnya sendiri, kalau tidak halaman
       tetap terkunci setelah pembaca melompat ke section tujuan. */
    /* Menekan tautan mana pun, atau area kosong di sekitarnya, menutup panel.
       Tanpa ini halaman tetap terkunci setelah pembaca melompat ke tujuan. */
    menu.addEventListener("click", function (e) {
        if (e.target.closest("a") || e.target === menu) {
            setel(false);
        }
    });

    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") {
            setel(false);
        }
    });

    document.addEventListener("click", function (e) {
        if (!menu.contains(e.target) && !burger.contains(e.target)) {
            setel(false);
        }
    });
})();
