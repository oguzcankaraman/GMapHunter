import json
import random
import time
from curl_cffi import requests
import fake_useragent as useragent

from database import DatabaseManager
from gmap_url_creator import GmapUrlCreator
from grid_manager import GridManager


class GmapDataFetcher:
    def __init__(self):
        # Grid ayarları (Ankara Geneli)
        self.url_generator = GmapUrlCreator(query="ankara dişçiler", zoom_meters=2000.0)
        self.db_conn = DatabaseManager()
        # Step 0.02 yaklaşık 2-3km eder, detaylı arama için idealdir.
        self.grid_manager = GridManager(start_lat=39.80, start_lng=32.70, end_lat=39.99, end_lng=33.00, step=0.02)
        self.ua = useragent.UserAgent()

    @staticmethod
    def safe_get(lst, indices, default=None):
        try:
            current = lst
            for i in indices:
                current = current[i]
            return current
        except (IndexError, TypeError, AttributeError):
            return default

    def run_grid_search(self):
        """
        Ana operasyon fonksiyonu. Grid üzerindeki her noktayı gezer.
        """
        print("🚀 Grid Taraması Başlıyor...")

        counter = 0
        for lat, lng in self.grid_manager.generate_coordinates():
            counter += 1
            print(f"\n📍 Kare #{counter}: {lat}, {lng} taranıyor...")

            url = self.url_generator.build_gmap_url(lat, lng)

            # --- CURL_CFFI İLE İSTEK ---
            try:
                # Impersonate ile Chrome taklidi yapıyoruz
                response = requests.get(
                    url,
                    impersonate="chrome110",
                    headers={"User-Agent": self.ua.random},
                    timeout=15
                )

                if response.status_code == 200:
                    # Google'ın çöp karakterlerini temizle
                    text_data = response.text.replace(")]}'", "").strip()
                    try:
                        data = json.loads(text_data)
                        # Veriyi anında işle (Return yok, döngü devam etmeli)
                        self.process_batch(data)
                    except json.JSONDecodeError:
                        print("⚠️ JSON parse hatası.")
                else:
                    print(f"❌ Hata: {response.status_code}")

                # Google'ı kızdırmamak için bekleme
                time.sleep(random.uniform(1.5, 3.5))

            except Exception as e:
                print(f"💥 İstek hatası: {e}")

    def process_batch(self, data: list) -> None:
        """
        Gelen JSON verisinin içindeki TÜM işletmeleri (derinlik fark etmeksizin) bulur.
        """
        print("   🕵️ Veri analizi yapılıyor...")

        # Tüm JSON ağacını gez ve adayları topla
        found_businesses = []
        self._recursive_search(data, found_businesses)

        if not found_businesses:
            print("   ⚠️ Bu karede uygun formatta işletme bulunamadı.")
            return

        count = 0
        saved_ids = set()  # Aynı paketteki dublikeleri önlemek için

        for info in found_businesses:
            parsed = self.parse_data(info)
            if parsed:
                # Aynı işletmeyi tekrar kaydetme (Paket içi deduping)
                if parsed['id'] in saved_ids: continue

                self.db_conn.upsert_location(parsed)
                saved_ids.add(parsed['id'])
                count += 1

        print(f"   ✅ {count} benzersiz işletme veritabanına işlendi.")

    def _recursive_search(self, data, results):
        """
        JSON ağacının derinliklerine inip 'İşletme İmzası' taşıyan listeleri bulur.
        """
        if isinstance(data, list):
            # Önce [14] index'ini kontrol et - asıl işletme verisi orada
            try:
                if len(data) > 14 and isinstance(data[14], list):
                    inner = data[14]
                    if len(inner) > 14:
                        name_check = inner[11]
                        category_check = inner[13]
                        if isinstance(name_check, str) and isinstance(category_check, list) and len(category_check) > 0:
                            # inner'ı ekle, data'yı değil
                            results.append(inner)
                            return
            except (IndexError, TypeError):
                pass

            # Eski kontrol de kalsın (fallback)
            try:
                if len(data) > 14:
                    name_check = data[11]
                    category_check = data[13]
                    if isinstance(name_check, str) and isinstance(category_check, list) and len(category_check) > 0:
                        results.append(data)
                        return
            except (IndexError, TypeError):
                pass

            for item in data:
                self._recursive_search(item, results)

    def parse_data(self, info: list) -> dict | None:
        # İsim kontrolü (Index 11)
        name = self.safe_get(info, [11], default=None)
        if not name or not isinstance(name, str): return None

        # Google ID kontrolü (Index 10) - Bu olmadan kaydedemeyiz
        cid = self.safe_get(info, [10], default=None)
        if not cid: return None

        rating = self.safe_get(info, [4, 7], default=0)
        reviews_count = self.safe_get(info, [4, 8], default=0)

        latitude = self.safe_get(info, [9, 2], default=0.0)
        longitude = self.safe_get(info, [9, 3], default=0.0)
        phone_num = self.safe_get(info, [178, 0, 0], default=None)
        website = self.safe_get(info, [7, 0], default=None)

        # Adres parçalarını birleştir (Index 2 listesi)
        address_parts = self.safe_get(info, [2], default=[])
        address = " ".join([str(p) for p in address_parts if p]) if isinstance(address_parts, list) else ""

        return {
            "id": cid,
            "name": name,
            "address": address,
            "phone_num": phone_num,
            "website": website,
            "rating": float(rating) if rating else 0.0,
            "reviews_count": int(reviews_count) if reviews_count else 0,
            "latitude": float(latitude) if latitude else 0.0,
            "longitude": float(longitude) if longitude else 0.0
        }


def main():
    gmap_fetcher = GmapDataFetcher()
    gmap_fetcher.run_grid_search()


if __name__ == "__main__":
    main()