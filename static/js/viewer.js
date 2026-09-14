/* Shows a 3D object inside the photo frame while the pointer rests on it.
   Three.js is only fetched once the pointer arrives, so a reader who scrolls
   straight past never pays for it. */

(function () {
    "use strict";

    var frame = document.querySelector(".frame");
    var mount = document.getElementById("viewer-3d");

    if (!frame || !mount || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        return;
    }

    var MODEL = mount.getAttribute("data-model");
    var started = false;

    function fail() {
        var tag = frame.querySelector(".frame-tag");
        if (tag) {
            tag.remove();
        }
    }

    function load() {
        if (started) {
            return;
        }
        started = true;

        /* The bare specifiers below are resolved by the importmap in <head>. */
        Promise.all([import("three"), import("three/addons/loaders/FBXLoader.js")])
            .then(function (mod) {
                start(mod[0], mod[1].FBXLoader);
            })
            .catch(fail);
    }

    function start(THREE, FBXLoader) {
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

        /* Measured from the frame, not the canvas, because the canvas has no
           size until setSize runs for the first time. */

        function resize() {
            var w = mount.clientWidth || frame.clientWidth;
            var h = mount.clientHeight || frame.clientHeight;

            if (!w || !h) {
                return;
            }

            camera.aspect = w / h;
            camera.updateProjectionMatrix();
            renderer.setSize(w, h);
            place();
        }

        /* Distance comes from the narrower opening. The frame stands upright,
           so width is usually the limit rather than height. */

        function place() {
            var vertical = THREE.MathUtils.degToRad(camera.fov) / 2;
            var horizontal = Math.atan(Math.tan(vertical) * camera.aspect);

            camera.position.set(0, 0, (1 / Math.sin(Math.min(vertical, horizontal))) * 1.2);
            camera.lookAt(0, 0, 0);
        }

        new FBXLoader().load(MODEL, function (obj) {
            pivot.add(obj);
            pivot.updateMatrixWorld(true);

            /* The model arrives at an arbitrary scale and centre, so it is
               normalised to radius 1 and moved onto the origin. Matrices have
               to be updated first or the bounding sphere comes out wrong. */
            var sphere = new THREE.Box3().setFromObject(obj).getBoundingSphere(new THREE.Sphere());
            var scale = 1 / (sphere.radius || 1);

            obj.scale.setScalar(scale);
            obj.position.set(
                -sphere.center.x * scale,
                -sphere.center.y * scale,
                -sphere.center.z * scale
            );

            resize();
            spin();
        }, null, fail);

        window.addEventListener("resize", resize, { passive: true });

        function spin() {
            window.requestAnimationFrame(spin);
            pivot.rotation.y += 0.008;
            renderer.render(scene, camera);
        }
    }

    frame.addEventListener("mouseenter", load, { once: true });
    frame.addEventListener("focusin", load, { once: true });
})();
