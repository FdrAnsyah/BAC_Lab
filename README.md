# BAC_Lab

Deskripsi
---------

Proyek ini adalah aplikasi contoh berbasis Flask yang menggunakan SQLite sebagai penyimpanan data. Tujuan repositori ini adalah menyediakan aplikasi sederhana untuk latihan keamanan, eksperimen, dan pembelajaran.

Prasyarat
---------

- Python 3.8 atau lebih baru
- `pip` untuk mengelola paket Python

Instalasi
---------

1. (Opsional) Buat virtual environment dan aktifkan:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependensi yang diperlukan:

```bash
pip install Flask sqlite-minutils
```

Menjalankan aplikasi
--------------------

Jalankan aplikasi dengan perintah berikut dari direktori proyek:

```bash
python app.py
```

Akses aplikasi melalui web browser di `http://127.0.0.1:5000` (default Flask).

Catatan Database
----------------

- Berkas database SQLite `db.sqlite3` sudah ada di repositori. Jika ingin memulai dengan database kosong, cukup hapus atau pindahkan berkas tersebut, kemudian jalankan aplikasi — aplikasi akan membuat DB baru bila diperlukan.
- Untuk manipulasi cepat DB dari command line, paket `sqlite-minutils` sudah direkomendasikan di atas.

Struktur Proyek (ringkasan)
--------------------------

- `app.py` — titik masuk aplikasi Flask.
- `db.sqlite3` — berkas database SQLite.
- `templates/` — folder berisi template HTML seperti `index.html`, `login.html`, `admin_dashboard.html`, dsb.

Keamanan & Catatan Penting
--------------------------

- Repositori ini bisa digunakan untuk latihan; jangan gunakan data sensitif nyata.
- Periksa konfigurasi Flask (mis. `SECRET_KEY`) jika Anda mengubah aplikasi untuk lingkungan produksi.

Kontribusi
----------

Jika Anda ingin berkontribusi, buka issue atau kirimkan pull request. Sertakan deskripsi perubahan dan alasan perbaikannya.

Lisensi
-------

Periksa pemilik repositori untuk informasi lisensi. Jika tidak ada, tanyakan pada pemilik proyek sebelum menggunakan ulang kode untuk tujuan komersial.

Kontak
-------

Untuk pertanyaan atau laporan bug, silakan buat issue di repository.
