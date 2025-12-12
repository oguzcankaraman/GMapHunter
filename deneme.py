from unittest import result

import requests
import json

# Senin bulduğun o "korkunç" URL
url = "https://www.google.com/search?tbm=map&authuser=0&hl=tr&gl=tr&pb=!4m12!1m3!1d42229.29652299996!2d32.76188029344966!3d39.96043055617815!2m3!1f0!2f0!3f0!3m2!1i837!2i827!4f13.1!7i20!10b1!12m25!1m5!18b1!30b1!31m1!1b1!34e1!2m4!5m1!6e2!20e3!39b1!10b1!12b1!13b1!16b1!17m1!3e1!20m3!5e2!6b1!14b1!46m1!1b0!96b1!99b1!19m4!2m3!1i360!2i120!4i8!20m65!2m2!1i203!2i100!3m2!2i4!5b1!6m6!1m2!1i86!2i86!1m2!1i408!2i240!7m33!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!1m3!1e9!2b1!3e2!2b1!9b0!15m16!1m7!1m2!1m1!1e2!2m2!1i195!2i195!3i20!1m7!1m2!1m1!1e2!2m2!1i195!2i195!3i20!22m6!1sJXM4acCFK8-pxc8P1KrvoAE%3A55!2s1i%3A0%2Ct%3A11887%2Cp%3AJXM4acCFK8-pxc8P1KrvoAE%3A55!7e81!12e3!17sJXM4acCFK8-pxc8P1KrvoAE%3A76!18e15!24m107!1m30!13m9!2b1!3b1!4b1!6i1!8b1!9b1!14b1!20b1!25b1!18m19!3b1!4b1!5b1!6b1!9b1!13b1!14b1!17b1!20b1!21b1!22b1!27m1!1b0!28b0!32b1!33m1!1b1!34b1!36e2!10m1!8e3!11m1!3e1!14m1!3b0!17b1!20m2!1e3!1e6!24b1!25b1!26b1!27b1!29b1!30m1!2b1!36b1!37b1!39m3!2m2!2i1!3i1!43b1!52b1!55b1!56m1!1b1!61m2!1m1!1e1!65m5!3m4!1m3!1m2!1i224!2i298!72m22!1m8!2b1!5b1!7b1!12m4!1b1!2b1!4m1!1e1!4b1!8m10!1m6!4m1!1e1!4m1!1e3!4m1!1e4!3sother_user_google_review_posts__and__hotel_and_vr_partner_review_posts!6m1!1e1!9b1!89b1!98m3!1b1!2b1!3b1!103b1!113b1!114m3!1b1!2m1!1b1!117b1!122m1!1b1!126b1!127b1!26m4!2m3!1i80!2i92!4i8!30m28!1m6!1m2!1i0!2i0!2m2!1i530!2i827!1m6!1m2!1i787!2i0!2m2!1i837!2i827!1m6!1m2!1i0!2i0!2m2!1i837!2i20!1m6!1m2!1i0!2i807!2m2!1i837!2i827!34m19!2b1!3b1!4b1!6b1!8m6!1b1!3b1!4b1!5b1!6b1!7b1!9b1!12b1!14b1!20b1!23b1!25b1!26b1!31b1!37m1!1e81!42b1!47m0!49m10!3b1!6m2!1b1!2b1!7m2!1e3!2b1!8b1!9b1!10e2!50m4!2e2!3m2!1b1!3b1!67m5!7b1!10b1!14b1!15m1!1b0!69i760&q=ankara%20di%C5%9F%C3%A7iler"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

# 1. TEMİZLİK: Baştaki çöp karakterleri sil
text_data = response.text.replace(")]}'", "").strip()

# 2. PARSE: JSON'a çevir
data = json.loads(text_data)

# 3. KEŞİF (Sana bıraktığım kısım)
# Google Maps verisi genelde data[0][1] içinde paketlenmiş olur.
# Ama her zaman değişebilir. O yüzden önce yapıyı görmen lazım.

print("Ana Veri Tipi:", type(data))
print("Ana Veri Uzunluğu:", len(data))

# İpucu: Veriler genellikle data[0][1] içinde 1. indeksten itibaren başlar.
try:
    results = data[64]
    print(f"Bulunan Sonuç Sayısı (Tahmini): {len(results)}")

    # İlk sonucu alıp röntgenini çekelim
    first_result = results[1]  # Genelde 0. indeks metadatadır, 1. indeks ilk mekandır.

    # Dosyaya yaz ki rahatça incele (Terminalde kaybolur)
    with open("google_maps_sample2.json", "w", encoding="utf-16") as f:
        json.dump(first_result, f, indent=4, ensure_ascii=False)

    print("✅ İlk sonuç 'google_maps_sample.json' dosyasına kaydedildi. Aç ve incele!")
    with open("tahmini_result.json", 'w', encoding='utf-16') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    with open("ilk_return.json", 'w', encoding='utf-16') as f:
        json.dump(results[0], f, indent=4, ensure_ascii=False)

except Exception as e:
    print("Parsing hatası, indeksler farklı olabilir:", e)
    # Hata alırsan ham veriyi kaydet ve incele
    with open("google_maps_raw.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)