import argparse
import time
from gmap_data_fetcher import GmapDataFetcher

# --- 81 İL VE ÖNEMLİ İLÇELERİN KOORDİNATLARI ---
CITIES = {
    # 3 BÜYÜKŞEHİR (Daha geniş kapsaması için parçalı)
    "istanbul_avrupa": {"lat": 41.0082, "lng": 28.9784},
    "istanbul_anadolu": {"lat": 40.9818, "lng": 29.0576},
    "ankara": {"lat": 39.9334, "lng": 32.8597},
    "izmir": {"lat": 38.4237, "lng": 27.1428},

    # DİĞER ŞEHİRLER (Alfabetik)
    "adana": {"lat": 37.0000, "lng": 35.3213},
    "adiyaman": {"lat": 37.7648, "lng": 38.2786},
    "afyon": {"lat": 38.7507, "lng": 30.5567},
    "agri": {"lat": 39.7191, "lng": 43.0503},
    "aksaray": {"lat": 38.3687, "lng": 34.0370},
    "amasya": {"lat": 40.6499, "lng": 35.8353},
    "antalya": {"lat": 36.8969, "lng": 30.7133},
    "ardahan": {"lat": 41.1105, "lng": 42.7022},
    "artvin": {"lat": 41.1828, "lng": 41.8183},
    "aydin": {"lat": 37.8560, "lng": 27.8416},
    "balikesir": {"lat": 39.6484, "lng": 27.8826},
    "bartin": {"lat": 41.6344, "lng": 32.3375},
    "batman": {"lat": 37.8812, "lng": 41.1351},
    "bayburt": {"lat": 40.2552, "lng": 40.2249},
    "bilecik": {"lat": 40.1451, "lng": 29.9798},
    "bingol": {"lat": 38.8853, "lng": 40.4983},
    "bitlis": {"lat": 38.3938, "lng": 42.1232},
    "bolu": {"lat": 40.7350, "lng": 31.6061},
    "burdur": {"lat": 37.7204, "lng": 30.2908},
    "bursa": {"lat": 40.1885, "lng": 29.0610},
    "canakkale": {"lat": 40.1553, "lng": 26.4142},
    "cankiri": {"lat": 40.6013, "lng": 33.6134},
    "corum": {"lat": 40.5506, "lng": 34.9556},
    "denizli": {"lat": 37.7765, "lng": 29.0864},
    "diyarbakir": {"lat": 37.9144, "lng": 40.2306},
    "duzce": {"lat": 40.8438, "lng": 31.1565},
    "edirne": {"lat": 41.6768, "lng": 26.5603},
    "elazig": {"lat": 38.6810, "lng": 39.2264},
    "erzincan": {"lat": 39.7500, "lng": 39.5000},
    "erzurum": {"lat": 39.9043, "lng": 41.2679},
    "eskisehir": {"lat": 39.7667, "lng": 30.5256},
    "gaziantep": {"lat": 37.0662, "lng": 37.3833},
    "giresun": {"lat": 40.9128, "lng": 38.3895},
    "gumushane": {"lat": 40.4600, "lng": 39.4700},
    "hakkari": {"lat": 37.5833, "lng": 43.7333},
    "hatay": {"lat": 36.2023, "lng": 36.1605},
    "igdir": {"lat": 39.9196, "lng": 44.0459},
    "isparta": {"lat": 37.7648, "lng": 30.5566},
    "kahramanmaras": {"lat": 37.5744, "lng": 36.9371},
    "karabuk": {"lat": 41.2061, "lng": 32.6204},
    "karaman": {"lat": 37.1759, "lng": 33.2287},
    "kars": {"lat": 40.6013, "lng": 43.0975},
    "kastamonu": {"lat": 41.3887, "lng": 33.7827},
    "kayseri": {"lat": 38.7312, "lng": 35.4787},
    "kilis": {"lat": 36.7184, "lng": 37.1212},
    "kirikkale": {"lat": 39.8468, "lng": 33.5153},
    "kirklareli": {"lat": 41.7333, "lng": 27.2167},
    "kirsehir": {"lat": 39.1425, "lng": 34.1709},
    "kocaeli": {"lat": 40.7654, "lng": 29.9408},
    "konya": {"lat": 37.8714, "lng": 32.4846},
    "kutahya": {"lat": 39.4167, "lng": 29.9833},
    "malatya": {"lat": 38.3552, "lng": 38.3095},
    "manisa": {"lat": 38.6191, "lng": 27.4289},
    "mardin": {"lat": 37.3212, "lng": 40.7245},
    "mersin": {"lat": 36.8121, "lng": 34.6415},
    "mugla": {"lat": 37.2153, "lng": 28.3636},
    "mus": {"lat": 38.7432, "lng": 41.4910},
    "nevsehir": {"lat": 38.6244, "lng": 34.7144},
    "nigde": {"lat": 37.9667, "lng": 34.6833},
    "ordu": {"lat": 40.9839, "lng": 37.8764},
    "osmaniye": {"lat": 37.0742, "lng": 36.2478},
    "rize": {"lat": 41.0201, "lng": 40.5234},
    "sakarya": {"lat": 40.7569, "lng": 30.3783},
    "samsun": {"lat": 41.2867, "lng": 36.3300},
    "sanliurfa": {"lat": 37.1591, "lng": 38.7969},
    "siirt": {"lat": 37.9333, "lng": 41.9500},
    "sinop": {"lat": 42.0231, "lng": 35.1531},
    "sirnak": {"lat": 37.5164, "lng": 42.4611},
    "sivas": {"lat": 39.7477, "lng": 37.0179},
    "tekirdag": {"lat": 40.9833, "lng": 27.5167},
    "tokat": {"lat": 40.3167, "lng": 36.5500},
    "trabzon": {"lat": 41.0027, "lng": 39.7168},
    "tunceli": {"lat": 39.1079, "lng": 39.5401},
    "usak": {"lat": 38.6823, "lng": 29.4082},
    "van": {"lat": 38.4891, "lng": 43.4089},
    "yalova": {"lat": 40.6500, "lng": 29.2667},
    "yozgat": {"lat": 39.8181, "lng": 34.8147},
    "zonguldak": {"lat": 41.4564, "lng": 31.7987}
}


def get_arguments():
    parser = argparse.ArgumentParser(description='GMapHunter - Lead Generation Bot')
    parser.add_argument('--city', type=str, required=True, help='Hedef Şehir (örn: ankara veya turkiye)')
    parser.add_argument('--keyword', type=str, required=True, help='Aranacak Kelime')
    parser.add_argument('--batch', type=str, required=True, help='Sipariş ID')
    return parser.parse_args()


def run_for_city(city_name, coords, keyword, batch_id):
    print(f"\n======== 🏙️ {city_name.upper()} Taranıyor... ========")
    try:
        data_fetcher = GmapDataFetcher(
            lat=coords['lat'],
            lng=coords['lng'],
            keyword=keyword,
            batch_id=batch_id,
            city=city_name
        )
        data_fetcher.run_grid_search()
        print(f"✅ {city_name} tamamlandı.")
    except Exception as e:
        print(f"❌ {city_name} sırasında hata oluştu: {e}")


def main():
    args = get_arguments()
    keyword = args.keyword
    batch_id = args.batch
    target_city_arg = args.city.lower()

    # --- SENARYO 1: TÜM TÜRKİYE ---
    if target_city_arg == "turkiye":
        print(f"🇹🇷 KOMPLE TÜRKİYE TARAMASI BAŞLATILIYOR ({len(CITIES)} Nokta)...")
        print(f"🔍 Aranacak Kelime: {keyword}")

        count = 1
        for city_key, coords in CITIES.items():
            print(f"\n[{count}/{len(CITIES)}] Sıradaki Şehir: {city_key.upper()}")
            run_for_city(city_key, coords, keyword, batch_id)
            count += 1
            time.sleep(5)  # Şehirler arası 5 saniye dinlen

        print("🏁 TÜM TÜRKİYE TARAMASI BİTTİ!")

    # --- SENARYO 2: TEK ŞEHİR ---
    elif target_city_arg in CITIES:
        run_for_city(target_city_arg, CITIES[target_city_arg], keyword, batch_id)

    else:
        print(f"HATA: '{target_city_arg}' şehir listesinde yok! (Geçerli bir şehir veya 'turkiye' yazın)")


if __name__ == "__main__":
    main()