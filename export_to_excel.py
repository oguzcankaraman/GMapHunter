import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()


def export_data():
    print("📥 Veritabanından veri çekiliyor...")

    try:
        # Veritabanı bağlantısı
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))

        # SQL Sorgusu (İstediğimiz sütunları seçiyoruz)
        query = """
                SELECT name         as "İşletme Adı",
                       phone_num    as "Telefon",
                       website      as "Web Sitesi",
                       rating       as "Puan",
                       address      as "Adres",
                       latitude,
                       longitude,
                       last_updated as "Son Güncelleme"
                FROM gmap_places
                ORDER BY last_updated DESC -- En son bulunanlar (en günceller) en üste
                """

        # Pandas ile SQL'i DataFrame'e çevir
        df = pd.read_sql_query(query, conn)
        conn.close()

        # --- VERİ TEMİZLİĞİ & ZENGİNLEŞTİRME ---

        # 1. Telefon numaralarını temizle (Sadece rakam kalsın veya formatla)
        df['Telefon'] = df['Telefon'].astype(str).str.replace(r'\D+', '', regex=True)

        # 2. Web sitesi olmayanlara "Yok" yaz
        df['Web Sitesi'] = df['Web Sitesi'].fillna("Mevcut Değil")

        # --- EXCEL'E YAZMA ---
        output_file = "Ankara_Dis_Klinikleri_Listesi.xlsx"

        # Excel Writer ile yazıyoruz (Daha fazla kontrol için)
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Diş Klinikleri')

            # Sütun genişliklerini otomatik ayarla (Görsellik önemli)
            worksheet = writer.sheets['Diş Klinikleri']
            for column_cells in worksheet.columns:
                length = max(len(str(cell.value)) for cell in column_cells)
                worksheet.column_dimensions[column_cells[0].column_letter].width = length + 2

        print(f"✅ Başarılı! Dosya oluşturuldu: {output_file}")
        print(f"📊 Toplam {len(df)} kayıt dışa aktarıldı.")

    except Exception as e:
        print(f"❌ Hata oluştu: {e}")


if __name__ == "__main__":
    export_data()