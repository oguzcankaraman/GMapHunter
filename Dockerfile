# 1. Base Image: Python 3.9'un hafif (slim) versiyonunu kullanıyoruz.
# "Slim" demek, gereksiz Linux araçları atılmış, sadece işe odaklı versiyon demektir.
FROM python:3.11-slim

# 2. Çalışma Dizini: Konteynerin içinde /app diye bir klasör aç ve oraya geç.
WORKDIR /app

# 3. Bağımlılıklar: Önce requirements.txt'yi kopyala.
# Neden sadece bunu kopyalıyoruz? Çünkü Docker "Layer Caching" yapar.
# Kodun değişse bile, requirements değişmediyse bu adımı pas geçer, build hızlanır.
COPY requirements.txt .

# 4. Yükleme: Kütüphaneleri kur.
# --no-cache-dir: İndirilen kurulum dosyalarını saklama, imaj küçük olsun.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Kaynak Kod: Şimdi kalan tüm dosyaları (.py, .env vs) içeri kopyala.
COPY . .

# 6. Komut: Konteyner başladığında ne yapsın?
# Python çıktısını anlık görebilmek için -u (unbuffered) parametresini kullanıyoruz.
CMD ["python", "-u", "main.py"]