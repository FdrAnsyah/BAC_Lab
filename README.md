# BAC Vulnerability Lab

## Deskripsi
Aplikasi Flask sederhana yang **sengaja dibuat rentan** untuk tujuan edukasi keamanan web. Aplikasi ini dirancang untuk mengajarkan dan melatih identifikasi serta eksploitasi kerentanan web umum seperti IDOR (Insecure Direct Object Reference), privilege escalation, forced browsing, dan parameter tampering.

## Opsi 1: Run menggunakan Python/Flask
### Prasyarat
- Python 3.8 atau lebih baru
- `pip` untuk mengelola paket Python

### Instalasi
1. Clone repository:
```bash
git clone https://github.com/FdrAnsyah/Keamanan_web
```

2. Pindah ke direktori BAC_vuln:
```bash
cd BAC_vuln
```

3. (Opsional) Buat virtual environment dan aktifkan:
```bash
python -m venv venv
source venv/bin/activate  # Di Linux/Mac
# atau
venv\Scripts\activate     # Di Windows
```

4. Install dependensi yang diperlukan:
```bash
pip install Flask
```

### Menjalankan aplikasi
Jalankan aplikasi dengan perintah berikut dari direktori proyek:
```bash
python app.py
```

Akses aplikasi melalui web browser di `http://127.0.0.1:5000`.

## Opsi 2: Run menggunakan Docker
### Prasyarat
- Docker dan Docker Compose telah terinstall

### Instalasi
1. Clone repository:
```bash
git clone https://github.com/FdrAnsyah/Keamanan_web
```

2. Pindah ke direktori BAC_vuln:
```bash
cd BAC_vuln
```

3. Buat file `Dockerfile`:
```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

4. Buat file `docker-compose.yml`:
```yaml
version: '3.8'
services:
  flask-app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=development
```

5. Buat file `requirements.txt`:
```
Flask==2.3.3
```

6. Jalankan aplikasi menggunakan Docker container:
```bash
docker-compose up --build
```

Akses aplikasi melalui web browser di `http://127.0.0.1:5000`.

## Default Credentials
Aplikasi ini memiliki akun user yang sudah dibuat sebelumnya:

- Username: alice, Password: alicepass (Regular user)
- Username: bob, Password: bobpass (Regular user)
- Username: carol, Password: carolpass (Admin user)

## Lab Instructions
Gunakan aplikasi ini untuk belajar mengidentifikasi dan eksploitasi kerentanan web umum:

- **IDOR (Insecure Direct Object Reference)** - Bisa mengakses profil dan billing user lain dengan mengganti parameter user_id/bill_id
- **Privilege Escalation** - Dapatkan akses admin dengan menggunakan fitur "become_admin" di halaman admin
- **Parameter Tampering** - Ubah nilai parameter untuk mengakses konten yang seharusnya tidak dapat diakses
- **Forced Browsing** - Akses halaman yang seharusnya hanya untuk admin tanpa otorisasi yang sesuai
- Gunakan tools seperti SQLMap, Burp Suite, atau OWASP ZAP untuk latihan pengujian penetrasi
