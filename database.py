import psycopg2
from datetime import datetime
import os
import dotenv

dotenv.load_dotenv()


class DatabaseManager:
    def __init__(self):
        self.db_url = os.environ.get("DATABASE_URL")
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()

    def connect(self):
        try:
            self.conn = psycopg2.connect(self.db_url)
            self.cursor = self.conn.cursor()
            print("✅ PostgreSQL bağlantısı başarılı.")
        except Exception as e:
            print(f"❌ Veritabanı bağlantı hatası: {e}")

    def create_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS businesses
                (
                    id           TEXT PRIMARY KEY,
                    name         TEXT,
                    address      TEXT,
                    phone_num    TEXT,
                    rating       FLOAT,
                    review_count INT,
                    website      TEXT,
                    latitude     REAL,
                    longitude    REAL,
                    batch_id     TEXT,
                    search_term  TEXT,
                    city         TEXT,
                    last_updated TIMESTAMP
                )
                """
        self.cursor.execute(query)
        self.conn.commit()

    def upsert_location(self, data):
        query = """
                INSERT INTO businesses (id,
                                         name,
                                         address,
                                         phone_num,
                                         rating,
                                         review_count,
                                         website,
                                         batch_id,
                                         search_term,
                                         city,
                                         latitude,
                                         longitude,
                                         last_updated)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET name         = EXCLUDED.name,
                                               address      = EXCLUDED.address,
                                               phone_num    = EXCLUDED.phone_num,
                                               rating       = EXCLUDED.rating,
                                               review_count = EXCLUDED.review_count,
                                               website      = EXCLUDED.website,
                                               batch_id     = EXCLUDED.batch_id,
                                               search_term  = EXCLUDED.search_term,
                                               city         = EXCLUDED.city,
                                               latitude     = EXCLUDED.latitude,
                                               longitude    = EXCLUDED.longitude,
                                               last_updated = EXCLUDED.last_updated;
                """

        try:
            self.cursor.execute(query, (
                data['id'],
                data['name'],
                data['address'],
                data['phone_num'],
                data['rating'],
                data['reviews_count'],
                data['website'],
                data['batch_id'],
                data['search_term'],
                data['city'],
                data['latitude'],
                data['longitude'],
                datetime.now()
            ))
            self.conn.commit()
            print(f"✅ DB UPDATE BAŞARILI: {data['name'][:20]}...")
        except Exception as e:
            print(f"Veri yazma hatası: {e}")
            self.conn.rollback()

    def close(self):
        if self.cursor: self.cursor.close()
        if self.conn: self.conn.close()
