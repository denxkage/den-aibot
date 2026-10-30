Deden AI Telegram Bot

Bot Telegram berbasis Python yang menggunakan OpenAI API
untuk menghasilkan jawaban AI.

Fitur

- Chat AI melalui Telegram
- Memori percakapan per pengguna
- Database SQLite atau PostgreSQL
- Perintah /start, /help, dan /reset
- Penanganan error API
- Pemrosesan asynchronous

Persyaratan

- Python 3.11 atau versi kompatibel
- Telegram Bot Token
- OpenAI API Key
- PostgreSQL untuk database persisten di hosting

Instalasi Lokal

1. Clone repository.

2. Instal dependensi:
   
   pip install -r requirements.txt

3. Salin ".env.example" menjadi ".env".

4. Isi token Telegram dan OpenAI API Key.

5. Jalankan:
   
   python bot.py

Variabel Lingkungan

- TELEGRAM_BOT_TOKEN
- OPENAI_API_KEY
- OPENAI_MODEL
- DATABASE_URL

Jangan unggah file ".env" atau token rahasia ke GitHub.

Lisensi

Gunakan dan modifikasi proyek ini sesuai kebutuhan.
