/* Menampilkan objek 3D di dalam bingkai foto saat kursor berada di atasnya.
   Three.js baru diunduh ketika kursor menyentuh bingkai, jadi pembaca yang
   hanya lewat tidak menanggung ongkosnya. */

(function () {
    "use strict";

    var frame = document.querySelector(".frame");
    var mount = document.getElementById("viewer-3d");

    if (!frame || !mount || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        return;
    }

    var FBX = mount.getAttribute("data-model");
    var mulai = false;

    function gagal() {
        var tag = frame.querySelector(".frame-tag");
        if (tag) {
            tag.remove();
        }
    }

    function muat() {
        if (mulai) {
            return;
        }
        mulai = true;

        /* Specifier telanjang di bawah ini dipetakan oleh importmap di <head>. */
        Promise.all([import("three"), import("three/addons/loaders/FBXLoader.js")])
            .then(function (mod) {
                jalan(mod[0], mod[1].FBXLoader);
            })
            .catch(gagal);
    }

    function jalan(THREE, FBXLoader) {
        var scene = new THREE.Scene();
        var camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
        var renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });

        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        mount.appendChild(renderer.domElement);

        scene.add(new THREE.HemisphereLight(0x8fc7ef, 0x01152b, 2.2));

        var key = new THREE.DirectionalLight(0xffffff, 2.2);
        key.position.set(3, 5, 4);
        scene.add(key);

        var rim = new THREE.DirectionalLight(0x3fcb84, 1.3);
        rim.position.set(-4, 2, -3);
        scene.add(rim);

        var pivot = new THREE.Group();
        scene.add(pivot);

        /* Ukuran diambil dari kotak bingkai, bukan dari canvas, karena canvas
           belum punya ukuran sampai setSize dipanggil pertama kali. */

        function ukur() {
            var w = mount.clientWidth || frame.clientWidth;
            var h = mount.clientHeight || frame.clientHeight;

            if (!w || !h) {
                return;
            }

            camera.aspect = w / h;
            camera.updateProjectionMatrix();
            renderer.setSize(w, h);
            taruh();
        }

        /* Jarak kamera dihitung dari bukaan yang paling sempit. Bingkainya
           tegak, jadi lebar yang biasanya membatasi, bukan tinggi. */

        function taruh() {
            var tegak = THREE.MathUtils.degToRad(camera.fov) / 2;
            var datar = Math.atan(Math.tan(tegak) * camera.aspect);

            camera.position.set(0, 0, (1 / Math.sin(Math.min(tegak, datar))) * 1.2);
            camera.lookAt(0, 0, 0);
        }

        new FBXLoader().load(FBX, function (obj) {
            pivot.add(obj);
            pivot.updateMatrixWorld(true);

            /* Model datang dengan skala dan titik pusat sembarang, jadi
               dinormalkan ke jari-jari 1 lalu digeser ke titik nol. */
            var bola = new THREE.Box3().setFromObject(obj).getBoundingSphere(new THREE.Sphere());
            var skala = 1 / (bola.radius || 1);

            obj.scale.setScalar(skala);
            obj.position.set(
                -bola.center.x * skala,
                -bola.center.y * skala,
                -bola.center.z * skala
            );

            ukur();
            putar();
        }, null, gagal);

        window.addEventListener("resize", ukur, { passive: true });

        function putar() {
            window.requestAnimationFrame(putar);
            pivot.rotation.y += 0.008;
            renderer.render(scene, camera);
        }
    }

    frame.addEventListener("mouseenter", muat, { once: true });
    frame.addEventListener("focusin", muat, { once: true });
})();
