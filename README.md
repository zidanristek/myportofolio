# myportofolio

Nama : Muhammad Sultan Zidan
NPM : 2506534876
Kelas : PBP E

Website portofolio pribadi untuk mata kuliah Pemrograman Berbasis Platform
(CSGE602022), Fakultas Ilmu Komputer Universitas Indonesia, Semester Gasal
2026/2027.

Dua halaman. Halaman profil di `/` berisi hero, About Me, Archive Projects, dan
Core Tech. Halaman `/experience/` menampilkan daftar pengalaman yang diambil dari
basis data. Sisi server memakai Django dengan pola MVT: model `Experience`
menyimpan datanya, view menyiapkan context, template merendernya. Tampilannya
HTML5 dan CSS3, ditambah sedikit JavaScript untuk taburan bintang, efek parallax
di hero, menu layar sempit, dan penampil objek 3D.

Versi daring: <https://muhammad-sultan51-myportofolio.pws.cs.ui.ac.id>

## Menjalankan di komputer sendiri

```bash
python -m venv env
env\Scripts\activate            # Windows
source env/bin/activate         # macOS dan Linux

pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata experience
python manage.py runserver
```

Halaman terbuka di <http://localhost:8000>

Proyek membaca berkas `.env` di root. Berkas itu tidak ikut masuk repositori,
jadi buat sendiri dengan satu baris berikut:

```
PRODUCTION=False
```

Selama nilainya `False`, proyek memakai SQLite. Saat diubah menjadi `True`,
proyek beralih ke PostgreSQL memakai kredensial dari `.env.prod`.

## Struktur

| Jalur | Isi |
| --- | --- |
| `portofolio/` | konfigurasi Django dan routing tingkat proyek |
| `main/` | aplikasi utama: model `Experience`, view, routing, dan test |
| `main/fixtures/experience.json` | isi awal tabel `Experience`, dimuat dengan `loaddata` |
| `templates/base.html` | kerangka bersama: head, navbar, dan footer |
| `templates/index.html` | halaman profil |
| `templates/experience.html` | daftar pengalaman |
| `static/css/style.css` | seluruh gaya, satu berkas |
| `static/js/` | `hero.js` bintang dan parallax, `nav.js` navbar dan menu, `viewer.js` penampil 3D |
| `static/img/` | foto, logo, sampul proyek, ikon teknologi |
| `static/model/` | berkas `.fbx` untuk objek 3D |

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
| Tutorial 02 | aplikasi `main`, model `Experience`, data profil pindah ke context, halaman `/experience/`, routing dua level, dan enam unit test |
| Tugas 1 | tiga section baru (Archive Projects, My Experiences, Core Tech), navigasi antar section, menu layar sempit, hero berlapis dengan parallax, dan penampil objek 3D pada foto profil |

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

## Penggunaan AI

Saya memakai AI dalam pengerjaan tugas ini. Berikut bagian mana saja dan
sebatas apa.

**Alat yang dipakai.** Claude, dan sebelumnya ChatGPT untuk tanya jawab konsep.

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
