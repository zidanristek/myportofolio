# myportofolio

Nama : Muhammad Sultan Zidan
NPM : 2506534876
Kelas : PBP E

Website portofolio pribadi untuk mata kuliah Pemrograman Berbasis Platform
(CSGE602022), Fakultas Ilmu Komputer Universitas Indonesia, Semester Gasal
2026/2027.

## Menjalankan di komputer sendiri

```bash
python -m venv env
env\Scripts\activate            # Windows
source env/bin/activate         # macOS dan Linux

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Halaman terbuka di http://localhost:8000/

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
| `portofolio/` | konfigurasi Django, routing, dan view |
| `templates/` | berkas HTML |
| `static/css/` | lembar gaya |
| `static/img/` | gambar |

## Alur branch

| Branch | Peran |
| --- | --- |
| `main` | versi yang di-deploy ke PWS |
| `dev` | branch default, tempat semua pekerjaan digabung |
| `feat/*`, `fix/*`, `docs/*` | berumur pendek, masuk ke `dev` lewat pull request |

Pesan commit mengikuti format Conventional Commits.
