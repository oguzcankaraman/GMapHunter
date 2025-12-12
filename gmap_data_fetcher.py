import json

import requests
import fake_useragent as useragent

from database import DatabaseManager
from gmap_url_creator import GmapUrlCreator


class GmapDataFetcher:
    def __init__(self):
        self.url = GmapUrlCreator(query="ankara dişçiler", zoom_meters=2000.00000000000).build_gmap_url(lat=39.96043, lng=32.76188,)
        self.db_conn = DatabaseManager()

        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'downlink': '10',
            'priority': 'u=1, i',
            'referer': 'https://www.google.com/',
            'rtt': '50',
            'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
            'x-browser-channel': 'stable',
            'x-browser-copyright': 'Copyright 2025 Google LLC. All Rights reserved.',
            'x-browser-validation': 'AUXUCdutEJ+6gl6bYtz7E2kgIT4=',
            'x-browser-year': '2025',
            'x-maps-diversion-context-bin': 'CAE=',
            # 'cookie': 'AEC=AaJma5vQ1BBRMhbxQUd_MsN7dEk4BrDQJxzhjCD1RE5hUriOUwjuwf7Fljw; __Secure-BUCKET=CPME; DV=w8UPNKp0v6MZQIF0XFQkBVhdNdjksBk; NID=527=WEkheKvZTcLQ_dhkTBPhJ9uzuRlwlRS6aOyaxJ3cY0hPsrsbE5yxXhpaSknVK4kf4l7LN0JLOZ-meQscjLZL91rNtc1EbLz6s4noO6clWxRah23EWIj9rwvEcu8UYfz0LK_xnyUhUEpo3MmA7nYytO1pmhbYZg_NkF6_fN6j3BLEx5iCm9catV6SnTfg2YheOEGNT5wbE8VzjcgINuDW5-EzEgVAbW9lJ8g-AQIDB6-eXNoW202B5UqaeCFWLg5anO8VnBy9XQ; __Secure-STRP=AD6DogvhICUZ-mOReiSqJQ5VZEsrayDLc-HGMiiDe9MFpdy0d5uJP-GZ0VNQE0gCtKsaeME09sbDXZBYdZ3BE5dcMqweeA2W8Ywm',
        }
        self.cookies = {
            'AEC': 'AaJma5vQ1BBRMhbxQUd_MsN7dEk4BrDQJxzhjCD1RE5hUriOUwjuwf7Fljw',
            '__Secure-BUCKET': 'CPME',
            'DV': 'w8UPNKp0v6MZQIF0XFQkBVhdNdjksBk',
            'NID': '527=WEkheKvZTcLQ_dhkTBPhJ9uzuRlwlRS6aOyaxJ3cY0hPsrsbE5yxXhpaSknVK4kf4l7LN0JLOZ-meQscjLZL91rNtc1EbLz6s4noO6clWxRah23EWIj9rwvEcu8UYfz0LK_xnyUhUEpo3MmA7nYytO1pmhbYZg_NkF6_fN6j3BLEx5iCm9catV6SnTfg2YheOEGNT5wbE8VzjcgINuDW5-EzEgVAbW9lJ8g-AQIDB6-eXNoW202B5UqaeCFWLg5anO8VnBy9XQ',
            '__Secure-STRP': 'AD6DogvhICUZ-mOReiSqJQ5VZEsrayDLc-HGMiiDe9MFpdy0d5uJP-GZ0VNQE0gCtKsaeME09sbDXZBYdZ3BE5dcMqweeA2W8Ywm',
        }

    @staticmethod
    def safe_get(lst, indices, default=None):
        """
        İç içe listelerden güvenli veri çeker.
        Örn: safe_get(data, [1, 7, 0], "Yok")
        """
        try:
            current = lst
            for i in indices:
                current = current[i]
            return current
        except (IndexError, TypeError, AttributeError):
            return default

    def fetch_data(self) -> list | None:
        # Dinamik user-agent oluştur
        ua = useragent.UserAgent()
        self.headers['user-agent'] = ua.random

        response = requests.get(self.url, headers=self.headers, cookies=self.cookies)
        if response.status_code == 200:
            # Başarılı istek

            # 1. TEMİZLİK: Baştaki çöp karakterleri sil
            text_data = response.text.replace(")]}'", "").strip()
            data = json.loads(text_data)
            return data
        else:
            print(f"❌ İstek hatası: {response.status_code}")
            return None

    def get_data(self, data: list) -> None:
        # Keşif ve veri çıkarma işlemleri burada yapılacak
        records = self.safe_get(data, [64], default=[])
        if len(records) == 0:
            print("❌ Veri bulunamadı veya yapı değişmiş olabilir.")
            return

        for record in records:
            if not isinstance(record, list):
                continue
            info = self.safe_get(record, [1], default=None)
            if not info or not isinstance(info, list) or len(info) <= 11:
                continue
            parsed_info = self.parse_data(info)

            if parsed_info:
                print("✅ Veri bulundu:")
                self.db_conn.upsert_location(parsed_info)


    def parse_data(self, info: list) -> dict | None:
        rating = self.safe_get(info, [4, 7], default=0)
        reviews_count = self.safe_get(info, [4, 8], default=0)
        latitude = self.safe_get(info, [9, 2], default=0)
        longitude = self.safe_get(info, [9, 3], default=0)
        name = self.safe_get(info, [11], default="Bilinmiyor")
        phone_num = self.safe_get(info, [178, 0, 0], default="Bilinmiyor")
        website = self.safe_get(info, [7, 0], default="Bilinmiyor")
        address_1 = self.safe_get(info, [2, 0], default="Bilinmiyor")
        address_2 = self.safe_get(info, [2, 1], default="Bilinmiyor")
        address_3 = self.safe_get(info, [2, 2], default="Bilinmiyor")
        cid = self.safe_get(info, [10], default="ID Bilinmiyor, Bozuk Veri")

        return {
            "id": cid,
            "name": name,
            "address": f"{address_1}, {address_2}, {address_3}",
            "phone_num": phone_num,
            "website": website,
            "rating": int(rating),
            "reviews_count": int(reviews_count),
            "latitude": latitude,
            "longitude": longitude
        }

def main():
    gmap_fetcher = GmapDataFetcher()
    data = gmap_fetcher.fetch_data()
    if data:
        gmap_fetcher.get_data(data)

if __name__ == "__main__":
    main()