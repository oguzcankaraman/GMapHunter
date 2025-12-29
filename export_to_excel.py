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

    print(f"📥 '{batch_id}' siparişi için veriler hazırlanıyor...")

    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))

        # Sadece gerekli sütunları çekiyoruz
        query = """
                SELECT name      as "İşletme Adı",
                       phone_num as "Telefon",
                       address   as "Açık Adres"
                FROM businesses
                WHERE batch_id = %s
                ORDER BY name ASC
                """

        df = pd.read_sql_query(query, conn, params=(batch_id,))
        conn.close()

        if df.empty:
            print("❌ Bu sipariş numarasına ait veri bulunamadı!")
            return

        # --- VERİ TEMİZLİĞİ VE FİLTRELEME ---

        # 1. Temizlik: Sadece rakamları bırak
        df['Telefon'] = df['Telefon'].astype(str).str.replace(r'\D+', '', regex=True)

        # 2. Filtre: Boş veya tanımsız olanları sil
        df = df[df['Telefon'] != '']
        df = df[df['Telefon'].notna()]

        # 3. Filtre: Sadece '0' ile başlayanları al (Böylece direkt 444 ile başlayanlar elenir)
        df = df[df['Telefon'].str.startswith('0')]

        # 4. Filtre: Tam olarak 11 hane olanları al (05XX... formatı)
        df = df[df['Telefon'].str.len() == 11]

        # 5. Filtre: '0850' ile başlayan Kurumsal/Sanal numaraları sil
        df = df[~df['Telefon'].str.startswith('0850')]

        # 6. Filtre: '444' ile başlayanları sil (Normalde 11 hane kuralı bunu eler ama
        # eğer 0444 gibi hatalı bir kayıt varsa garantiye almak için ekliyoruz)
        df = df[~df['Telefon'].str.startswith('444')]

        # Eğer filtreleme sonrası elimizde hiç veri kalmadıysa uyar
        if df.empty:
            print("⚠️ Uyarı: Kriterlere (0850 hariç, 11 hane vb.) uyan telefon numarası kalmadı.")
            return

        # Adres boşsa belirtelim
        df['Açık Adres'] = df['Açık Adres'].fillna("Adres Belirtilmemiş")

        # --- EXCEL ÇIKTISI ---
        # Dosyayı /app klasörüne (yani sunucuda o anki dizine) kaydeder
        output_file = f"/app/Musteri_Listesi_{batch_id}.xlsx"

        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')

            # Sütun genişliklerini ayarla
            worksheet = writer.sheets['Data']
            for column_cells in worksheet.columns:
                try:
                    length = max(len(str(cell.value)) for cell in column_cells)
                    worksheet.column_dimensions[column_cells[0].column_letter].width = length + 2
                except:
                    pass

        print(f"✅ Başarılı! Dosya hazır: {output_file}")
        print(f"📊 Filtreler sonrası {len(df)} adet 'Gold Data' indirildi.")

    except Exception as e:
        print(f"❌ Hata oluştu: {e}")


if __name__ == "__main__":
    export_data()