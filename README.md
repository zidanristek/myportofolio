# myportofolio

Nama : Muhammad Sultan Zidan
NPM : 2506534876
Kelas : PBP E

Portofolio pribadi untuk mata kuliah Pemrograman Berbasis Platform (CSGE602022),
Fakultas Ilmu Komputer Universitas Indonesia, Gasal 2026/2027.

Tiga halaman. `/` berisi hero, About Me, dan Core Tech. `/projects/` memuat enam
proyek, `/experience/` memuat lima pengalaman sebagai carousel. Keduanya punya
pencarian judul, form tambah, form ubah, dan tombol hapus. Isi kedua halaman daftar itu datang dari basis data
lewat model `Project` dan `Experience`, bukan ditulis di HTML. Daftar proyek juga
tersedia mentah dalam dua format:

| Endpoint | Isi |
| --- | --- |
| `/api/projects/` | daftar proyek, JSON |
| `/api/projects/xml/` | daftar proyek, XML |
| `/api/experiences/` | daftar pengalaman, JSON |
| `/api/experiences/xml/` | daftar pengalaman, XML |

Keempatnya menerima `?title=` untuk menyaring berdasarkan judul.

Sisi server memakai Django dengan pola MVT. Tampilannya HTML5 dan CSS3.
JavaScript dipakai untuk lima hal: taburan bintang di hero, parallax antar
lapisan langit, navbar yang menyingkir saat menggulir, menu layar sempit, dan
penampil objek 3D pada foto profil.

Versi daring: <https://muhammad-sultan51-myportofolio.pws.cs.ui.ac.id>

## Menjalankan di komputer sendiri

```bash
python -m venv env
env\Scripts\activate            # Windows
source env/bin/activate         # macOS dan Linux

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Buka <http://localhost:8000>.

`migrate` sekaligus mengisi tabel `Experience` dan `Project` dari
`main/fixtures/`, jadi tidak perlu `loaddata` manual. Kalau tabelnya dikosongkan,
kedua halaman daftar menampilkan pesan "Belum ada ...".

Proyek membaca berkas `.env` di root yang tidak ikut masuk repositori. Buat
sendiri, isinya satu baris:

```
PRODUCTION=False
EDIT_PASSWORD=isi-sendiri
```

`EDIT_PASSWORD` adalah kode akses untuk menambah dan menghapus proyek. Selama
belum ada autentikasi, form dan tombol hapus menolak semua permintaan yang kode
aksesnya tidak cocok. Nilainya tidak pernah masuk repositori, dan di PWS diisi
lewat tab Environs.

Nilai `PRODUCTION=False` memakai SQLite. Diubah ke `True`, proyek beralih ke PostgreSQL
dengan kredensial dari `.env.prod`.

Jalankan `python manage.py test` untuk menjalankan 40 test di `main/tests.py`.

## Struktur

| Jalur | Isi |
| --- | --- |
| `portofolio/` | settings dan routing tingkat proyek |
| `main/models.py` | model `Experience` dan `Project` |
| `main/forms.py` | `ProjectForm` dan `ExperienceForm`, keduanya `ModelForm` |
| `main/views.py` | tiga halaman, empat endpoint data, dan enam view tulis |
| `main/urls.py` | rute halaman dan `/api/` dengan namespace `main` |
| `main/fixtures/` | isi awal kedua tabel, dimuat migrasi `0004` |
| `main/tests.py` | 40 test |
| `templates/base.html` | head, navbar, footer, dipakai ketiga halaman |
| `templates/index.html` | halaman profil |
| `templates/projects.html` | daftar proyek |
| `templates/experience.html` | carousel pengalaman |
| `templates/projects_form.html` | form tambah dan ubah proyek |
| `templates/experience_form.html` | form tambah dan ubah pengalaman |
| `templates/components/` | potongan template yang dipakai ulang |
| `static/css/style.css` | seluruh gaya |
| `static/js/` | `hero.js` bintang dan parallax, `nav.js` navbar, menu, dan panah carousel, `viewer.js` penampil 3D |
| `static/img/` | foto, logo, sampul proyek, gambar pengalaman, ikon teknologi |
| `static/model/object.fbx` | Makara UI untuk penampil 3D |

## Alur branch

| Branch | Peran |
| --- | --- |
| `main` | versi yang di-deploy ke PWS |
| `dev` | branch default, tempat semua pekerjaan digabung |
| `feat/*`, `fix/*`, `docs/*` | berumur pendek, masuk ke `dev` lewat pull request |

Pesan commit mengikuti format Conventional Commits.

## Progres mingguan

| Minggu | Yang dikerjakan |
| --- | --- |
| Tutorial 0 | repositori Git, virtual environment, proyek Django pertama |
| Tutorial 01 | halaman About Me, WhiteNoise, deploy pertama ke PWS |
| Tugas 1 | Archive Projects, My Experiences, Core Tech, menu layar sempit, hero berlapis dengan parallax, penampil objek 3D |
| Tutorial 02 | aplikasi `main`, model `Experience`, data profil pindah ke context, halaman `/experience/`, routing dua level, enam unit test |
| Tugas 2 | model `Project`, halaman `/projects/`, kartu proyek digerakkan basis data, carousel pada `/experience/`, fixture dimuat saat migrasi, enam unit test tambahan |
| Tutorial 03 | `ProjectForm`, penambahan dan penghapusan proyek lewat browser, pencarian judul, endpoint JSON dan XML, kode akses dari environment, dua belas unit test tambahan |
| Tugas 3 | `ExperienceForm`, alur lengkap tambah, ubah, dan hapus pengalaman, endpoint JSON dan XML untuk pengalaman, halaman pengalaman dibaca lewat deserialisasi, tombol ubah untuk proyek, enam belas unit test tambahan |

## Pertanyaan reflektif

### Tugas 1

1. Iya, saya memakai elemen semantik HTML5. `<section>` untuk tiap bagian
   halaman, `<article>` untuk tiap kartu proyek, `<figure>` dengan
   `<figcaption>` untuk bingkai foto profil, dan `<ol>` untuk linimasa
   pengalaman karena urutan tahunnya memang bermakna. Yang paling terasa
   gunanya adalah `<article>` pada kartu proyek. Tiap kartu berdiri sendiri,
   isinya masih utuh kalau dicabut dari halaman, dan itu persis definisi
   `<article>`. Dengan begitu saya tidak perlu menebak-nebak nanti waktu kartu
   ini dipindah ke halaman terpisah. `<aside>` tidak saya pakai karena tidak
   ada konten yang benar-benar sampingan di halaman ini, semuanya adalah isi
   utama profil. Memakai `<aside>` hanya supaya kelihatan lengkap justru
   membuat maknanya salah.

2. Tantangan terbesarnya bukan lebar layar, melainkan tinggi layar. Gedung
   Rektorat di hero tingginya saya atur dengan satuan `vh`, sedangkan tinggi
   teks di atasnya dalam piksel. Akibatnya di layar pendek seperti 1280x720
   puncak gedungnya menabrak tombol, padahal di 1920x1080 aman. Saya coba
   mengganti angkanya tiga kali dan selalu ada satu ukuran yang rusak. Baru
   berhenti setelah saya ubah pendekatannya: gedung dijadikan item flex yang
   mengisi sisa ruang di bawah isi hero, jadi tabrakan mustahil terjadi karena
   struktur, bukan karena angkanya kebetulan pas. Untuk memutuskan elemen mana
   yang digeser, patokan saya isi yang paling penting harus muncul lebih dulu.
   Di linimasa pengalaman, versi desktop zigzag kiri kanan, tapi di mobile
   lebarnya tidak cukup untuk dua kolom, jadi saya jadikan satu kolom rata
   tengah. Menu navigasi juga begitu, di mobile tautannya pindah ke panel
   penuh layar karena kalau dipaksa satu baris tingginya menumpuk jadi tiga.

3. Batasan yang paling saya rasakan ada di section proyek. Enam kartu itu saya
   tulis satu per satu di HTML, dan tiap kartu punya struktur yang persis sama.
   Kalau nanti proyeknya jadi lima belas, berkasnya akan panjang sekali dan
   satu perubahan kecil pada bentuk kartu harus saya salin ke semua kartu.
   Menambah proyek baru berarti menyunting HTML dan push ulang, padahal itu
   data, bukan tampilan. Hal yang sama terjadi di linimasa pengalaman dan
   daftar teknologi. Untuk iterasi berikutnya yang paling ingin saya siapkan
   adalah model dan template yang mengulang datanya, jadi kartu proyek cukup
   ditulis sekali lalu diisi dari basis data. Setelah itu baru masuk akal
   menambahkan penyaring kategori dan pencarian, karena keduanya butuh data
   yang bisa dikueri, bukan teks yang tertanam di markup.

### Tugas 2

1. Permintaan ke `/projects/` pertama kali ditangani `portofolio/urls.py` yang
   sengaja tidak memilih view apa pun melainkan meneruskan sisa path lewat
   `include("main.urls")` supaya aplikasi bisa dipasang di prefix lain tanpa
   menyentuh konfigurasi proyek, lalu `main/urls.py` memetakannya ke
   `show_projects` yang memanggil `Project.objects.all()` dan menyerahkan
   hasilnya ke `projects.html` sebagai `project_list`, dan pembagian berlapis
   itulah yang membuat template sama sekali tidak perlu tahu datanya berasal
   dari basis data karena yang dia terima hanya objek yang sudah siap dirender.

2. Enam kartu proyek yang dulu saya tulis satu per satu di `index.html` punya
   struktur `<article>` yang persis sama sehingga satu perubahan bentuk kartu
   harus saya salin enam kali dan menambah proyek berarti menyunting markup
   padahal yang bertambah sebenarnya data, sedangkan setelah dipindah ke model
   bentuk kartunya cukup ditulis sekali lalu diisi lewat perulangan sehingga
   urutan tinggal diatur `Meta.ordering` alih-alih memindah blok HTML, dan yang
   paling terasa buat pemeliharaan adalah saya jadi bisa menulis test yang
   langsung merah kalau suatu saat data proyek menyelinap balik ke halaman
   profil.

3. `makemigrations` hanya membandingkan `models.py` dengan migrasi yang sudah
   ada lalu menulis berkas instruksi perubahannya tanpa menyentuh basis data
   sedangkan `migrate` yang benar-benar menjalankan instruksi tersebut, dan
   pemisahan itu baru terasa gunanya waktu saya menambahkan field `position` ke
   `Experience` supaya urutan kartu bisa saya tentukan sendiri tanpa memalsukan
   tanggal, karena berkas `0003` sudah lahir tetapi halaman Experience tetap
   error sampai `migrate` dijalankan dan kolomnya benar-benar terbentuk di
   tabel.

### Tugas 3

1. `ModelForm` menurunkan field, validation, dan widget langsung dari model,
   jadi rules-nya cuma ditulis sekali. Terbukti waktu saya bikin
   `ExperienceForm`: field `thumbnail` yang tipenya `URLField` langsung menolak
   `img/experience/banyumas.jpg` milik lima entri saya, sesuatu yang bakal lolos
   kalau form-nya saya tulis manual dan baru gagal di database.
   `{% csrf_token %}` wajib karena Django menolak POST tanpa token, gunanya
   mencegah situs lain submit form atas nama visitor saya, dan itu saya buktikan
   waktu POST ke `/projects/add/` di PWS tanpa token dibalas `403`.

2. JSON memetakan langsung ke tipe bawaan hampir semua bahasa, object dan array
   jadi `dict` dan `list` di Python atau object dan array di JavaScript, jadi
   tidak butuh parser tambahan seperti XML yang harus ditelusuri sebagai tree
   dulu. Ukurannya juga lebih kecil karena tiap value tidak ditutup closing tag:
   enam project yang sama 2.920 byte sebagai JSON dan 4.812 byte sebagai XML,
   65 persen lebih besar untuk isi yang identik.

3. Request ke `/api/projects/` diteruskan `portofolio/urls.py` ke
   `main/urls.py`, dipetakan ke `get_projects_json`, yang mengambil
   `Project.objects.all()`, memfilternya kalau ada `?title=`, lalu menyerahkan
   QuerySet itu ke `serializers.serialize("json", ...)` dan membungkusnya dengan
   `HttpResponse(content_type="application/json")`. Serialization perlu karena
   QuerySet berisi object Python hidup dengan `UUID`, `datetime`, dan query yang
   masih lazy, sedangkan HTTP cuma mengangkut teks. Object-nya harus diratakan
   jadi pasangan key dan value yang bisa dibaca ulang siapa pun, termasuk
   `show_projects` saya sendiri yang mengurai balik lewat
   `serializers.deserialize`.

## Penggunaan AI

Saya memakai AI dalam pengerjaan tugas ini. Berikut bagian mana saja dan
sebatas apa. Alat yang dipakai sejak awal semester sama, yaitu Claude dan
sebelumnya ChatGPT untuk tanya jawab konsep.

### Tugas 1

**Cara saya memakainya.** Polanya selalu dua tahap. Saya belajar dulu dari
Claude sampai paham apa yang sebenarnya terjadi, baru saya minta Claude yang
menuliskannya. Urutan itu saya jaga karena kalau langsung minta hasil jadi,
yang saya dapat cuma berkas yang tidak bisa saya pertanggungjawabkan.

**Latar belakangnya.** Saya sudah punya portofolio yang dibuat dengan React dan
Next.js. Untuk tugas ini saya ingin memindahkannya ke Django. Masalahnya, kalau
saya minta AI memindahkan framework begitu saja, hasilnya bukan pemindahan tapi
proyek baru yang tidak saya pahami. Jadi strategi prompting saya adalah meminta
AI menganalisis dulu, bukan langsung menulis kode. Saya minta dipetakan mana
fungsi dan pola di React yang punya padanan di Django. Dari situ saya melihat
kemiripannya, misalnya konsep komponen di React yang kira-kira sepadan dengan
template dan pola `{% static %}` yang mirip dengan cara Next.js menangani aset
statis. Saya belajar Django dari pemahaman React saya, bukan dari nol.

**Bagian yang dikerjakan Claude.** Efek taburan bintang dan parallax di hero.
Saya tanya dulu bagaimana lapisan latar digeser dengan kecepatan berbeda, baru
saya minta ditulis. Cara ini memang biasa saya pakai, waktu menulis shader
Godot pun saya sering bertanya lebih dulu supaya efek dinamisnya lebih halus,
karena bagian itu jujur saja sulit bagi saya. Sebagian besar tata letak dan CSS
juga ditulis Claude, tapi selalu setelah saya tentukan bentuk yang saya mau,
dan saya minta ulang kalau hasilnya meleset. Dokumentasi ini disusun dengan
cara yang sama.

**Bagian yang bukan dari Claude.** Desain hero saya buat dulu di Figma, lalu
dipindahkan ke website. Gaya navbar, kartu, dan skala warna berasal dari
proyek-proyek saya sendiri, terutama visualisasi NalarAI, jadi token warnanya
saya pakai ulang di sini. Logo Zido Games, ilustrasi gedung Rektorat, model 3D
Makara, dan seluruh tangkapan layar proyek adalah karya saya. Semua isi
tulisannya, mulai dari daftar pengalaman sampai deskripsi proyek, berasal dari
data saya sendiri.

**Keterbatasannya.** Yang paling sering, angka yang diberikan kelihatan benar
tapi salah begitu dicoba di ukuran layar lain. Masalah gedung
menabrak tombol yang saya ceritakan di jawaban nomor dua itu contohnya, tiga
kali percobaan dengan angka berbeda tetap gagal, dan baru selesai setelah
pendekatannya diganti. Akar masalah juga beberapa kali salah ditebak. Waktu
ikon Instagram dan LinkedIn tidak muncul, dugaan pertamanya elemen lain yang
menimpa, padahal penyebabnya berkas SVG yang saya ambil dari proyek lama tidak
punya atribut `xmlns` sehingga tidak sah sebagai berkas yang berdiri sendiri.
Kesimpulan saya, menulis kodenya cepat, tapi tetap saya yang harus melihat
hasilnya di layar dan memutuskan benar atau tidak.

**Kalau ingin memverifikasi.** Riwayat commit di repositori ini memakai
Conventional Commits dan dipecah per perubahan, jadi urutan pengerjaannya bisa
ditelusuri dari `git log`.

### Tugas 2

Bagian MVT-nya tidak banyak saya serahkan ke AI. Model, view, routing, dan
migrasi polanya sudah jelas dari Tutorial 02, jadi saya tinggal mengikuti. Yang
betul-betul merepotkan justru tampilan carousel di halaman Experience. Saya
beberapa kali bertanya ke Claude sebagai panduan, lalu hasilnya saya ubah
sendiri sampai geserannya terasa benar.

Untuk materi baru saya selalu minta penjelasan konsep lebih dulu, baru
implementasi. Waktu memutuskan urutan tampil kartu, saya tanya dulu kenapa
urutan sebaiknya disimpan sebagai kolom ketimbang dihitung dari tanggal, dan
jawabannya yang membuat saya menambahkan field `position` alih-alih memundurkan
tanggal supaya kebetulan terurut. Waktu menggarap carousel, saya minta
dijelaskan dulu bagaimana `scroll-snap` menentukan titik berhenti, baru saya
atur sendiri lebar slide dan padding kiri kanannya sampai slide pertama bisa
sampai ke tengah. Untuk perbaikan tampilan polanya berbeda. Saya sebutkan
gejalanya saja, biarkan AI menebak penyebabnya, lalu saya buka halamannya dan
periksa sendiri apakah tebakannya benar.

Ada usulan menambahkan label pada kartu yang tidak saya pakai. Portofolio yang
isinya kebanyakan teks tidak enak dilihat, dan label semacam itu ujungnya cuma
bikin halaman terasa dikerjakan mesin. Gambar pengalaman dan sampul proyek
semuanya saya masukkan sendiri, begitu juga seluruh isi teksnya.

Keterbatasannya masih mirip Tugas 1. Isi awal tabel sempat saya taruh di dalam
berkas migrasi, dan itu justru saran yang saya dapat waktu bertanya, alasannya
supaya datanya ikut terpasang otomatis saat deploy. Setelah dijalankan, tiga
test dari Tutorial 02 langsung merah. Penyebabnya migrasi juga dijalankan di
basis data test, jadi baris-baris tadi ikut terbawa dan merusak pemeriksaan
yang menuntut tabel kosong. Saya ganti pendekatannya ke fixture yang dimuat
terpisah, dan keenam test Tutorial 02 bisa dipakai apa adanya tanpa satu huruf
pun diubah. Hal kecil juga terjadi waktu saya menambahkan tautan Home ke
navbar. Yang masuk malah dua, dan baru ketahuan setelah saya lihat halamannya.
Kesimpulan saya sama seperti Tugas 1. Kodenya cepat jadi, tapi yang menentukan
benar atau tidak tetap saya, setelah melihat hasilnya di layar.
