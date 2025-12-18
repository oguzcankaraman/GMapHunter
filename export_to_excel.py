import os
import argparse
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_args():
    parser = argparse.ArgumentParser(description="Excel Export Aracı")
    parser.add_argument("--batch", type=str, required=True, help="Hangi siparişi indirmek istiyorsun? (Batch ID)")
    return parser.parse_args()


def export_data():
    args = get_args()
    batch_id = args.batch

    print(f"📥 '{batch_id}' siparişi için veriler çekiliyor...")

    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))

        # SQL Sorgusu: Sadece batch_id ile eşleşenleri alıyoruz
        # Tablo ismini 'businesses' olarak düzelttik
        query = """
                SELECT name         as "İşletme Adı",
                       phone_num    as "Telefon",
                       website      as "Web Sitesi",
                       rating       as "Puan",
                       review_count as "Yorum Sayısı",
                       address      as "Adres",
                       search_term  as "Aranan Sektör",
                       city         as "Şehir"
                FROM businesses
                WHERE batch_id = %s
                ORDER BY rating DESC
                """

        # params=(batch_id,) ile SQL injection'ı önlüyoruz
        df = pd.read_sql_query(query, conn, params=(batch_id,))
        conn.close()

        if df.empty:
            print("❌ Bu sipariş numarasına ait veri bulunamadı!")
            return

        # --- VERİ TEMİZLİĞİ ---
        df['Telefon'] = df['Telefon'].astype(str).str.replace(r'\D+', '', regex=True)
        df['Web Sitesi'] = df['Web Sitesi'].fillna("Mevcut Değil")

        # --- EXCEL ÇIKTISI ---
        # Dosya adına batch_id ekliyoruz ki karışmasın
        output_file = f"Musteri_Listesi_{batch_id}.xlsx"

        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')

            worksheet = writer.sheets['Data']
            for column_cells in worksheet.columns:
                length = max(len(str(cell.value)) for cell in column_cells)
                worksheet.column_dimensions[column_cells[0].column_letter].width = length + 2

        print(f"✅ Başarılı! Dosya hazır: {output_file}")
        print(f"📊 Toplam {len(df)} kayıt indirildi.")

    except Exception as e:
        print(f"❌ Hata oluştu: {e}")


if __name__ == "__main__":
    export_data()