import argparse
# Örnek çalıştırma kodu: docker run --env-file .env gmap-hunter python main.py --city ankara --keyword "oto kiralama" --batch siparis_mehmet_bey_001
from gmap_data_fetcher import GmapDataFetcher

# Şehir Sözlüğü: Türkiye'nin En Büyük Ticari Merkezleri
CITIES = {
    # --- 3 BÜYÜKŞEHİR ---
    "istanbul":   {"lat": 41.0082, "lng": 28.9784, "zoom": 12}, # Avrupa Yakası Merkez
    "istanbul_anadolu": {"lat": 40.9818, "lng": 29.0576, "zoom": 12}, # Kadıköy/Anadolu
    "ankara":     {"lat": 39.9334, "lng": 32.8597, "zoom": 13},
    "izmir":      {"lat": 38.4237, "lng": 27.1428, "zoom": 13},

    # --- TİCARET & TURİZM MERKEZLERİ ---
    "antalya":    {"lat": 36.8969, "lng": 30.7133, "zoom": 13},
    "bursa":      {"lat": 40.1885, "lng": 29.0610, "zoom": 13},
    "adana":      {"lat": 37.0000, "lng": 35.3213, "zoom": 13},
    "gaziantep":  {"lat": 37.0662, "lng": 37.3833, "zoom": 13},
    "konya":      {"lat": 37.8714, "lng": 32.4846, "zoom": 13},
    "mersin":     {"lat": 36.8121, "lng": 34.6415, "zoom": 13},
    "kayseri":    {"lat": 38.7312, "lng": 35.4787, "zoom": 13},
    "kocaeli":    {"lat": 40.7654, "lng": 29.9408, "zoom": 13}, # İzmit Merkez
    "eskisehir":  {"lat": 39.7667, "lng": 30.5256, "zoom": 13},
    "diyarbakir": {"lat": 37.9144, "lng": 40.2306, "zoom": 13},
    "samsun":     {"lat": 41.2867, "lng": 36.3300, "zoom": 13},
    "denizli":    {"lat": 37.7765, "lng": 29.0864, "zoom": 13},
    "sanliurfa":  {"lat": 37.1591, "lng": 38.7969, "zoom": 13},
    "malatya":    {"lat": 38.3552, "lng": 38.3095, "zoom": 13},
    "trabzon":    {"lat": 41.0027, "lng": 39.7168, "zoom": 13},
    "sakarya":    {"lat": 40.7569, "lng": 30.3783, "zoom": 13}, # Adapazarı
    "mugla":      {"lat": 37.2153, "lng": 28.3636, "zoom": 13},
    "tekirdag":   {"lat": 40.9833, "lng": 27.5167, "zoom": 13},
    "hatay":      {"lat": 36.2023, "lng": 36.1605, "zoom": 13}, # Antakya
    "manisa":     {"lat": 38.6191, "lng": 27.4289, "zoom": 13},
    "balikesir":  {"lat": 39.6484, "lng": 27.8826, "zoom": 13},
}


def get_arguments():
    parser = argparse.ArgumentParser(description='GMapHunter - Lead Generation Bot')

    parser.add_argument('--city', type=str, required=True, help='Hedef Şehir (örn: ankara)')
    parser.add_argument('--keyword', type=str, required=True, help='Aranacak Kelime (örn: diş kliniği)')
    parser.add_argument('--batch', type=str, required=True, help='Sipariş ID (örn: siparis_001)')

    return parser.parse_args()


def main():
    args = get_arguments()

    city_key = args.city.lower()
    if city_key not in CITIES:
        print(f"HATA: '{city_key}' şehir listesinde yok! Lütfen koordinat ekleyin.")
        return

    target_city = CITIES[city_key]

    print(f"🚀 Bot Başlatılıyor...")
    print(f"📍 Hedef: {args.city.upper()} ({target_city['lat']}, {target_city['lng']})")
    print(f"🔍 Kelime: {args.keyword}")
    print(f"📦 Sipariş No: {args.batch}")

    data_fetcher = GmapDataFetcher(
        lat=target_city['lat'],
        lng=target_city['lng'],
        keyword=args.keyword,
        batch_id=args.batch,
        city=city_key
    )
    data_fetcher.run_grid_search()


if __name__ == "__main__":
    main()
