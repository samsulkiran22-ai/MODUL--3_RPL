from config.database import Database


class BukuModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "buku"

    def get_all_buku(self):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)  # hasil berupa dict
            cursor.execute(f"SELECT * FROM {self.table_name}")
            data = cursor.fetchall()
            cursor.close()
            return data
        return []

    def create_buku(self, judul, penulis, tahun):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                query = f"INSERT INTO {self.table_name} (judul, penulis, tahun_terbit) VALUES (%s, %s, %s)"
                cursor.execute(query, (judul, penulis, tahun))
                self.conn.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"Error create_buku: {e}")
                return False
        return False

    def update_buku(self, id_buku, judul, penulis, tahun):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                query = f"UPDATE {self.table_name} SET judul = %s, penulis = %s, tahun_terbit = %s WHERE id_buku = %s"
                cursor.execute(query, (judul, penulis, tahun, id_buku))
                self.conn.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"Error update_buku: {e}")
                return False
        return False

    def delete_buku(self, id_buku):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                query = f"DELETE FROM {self.table_name} WHERE id_buku = %s"
                cursor.execute(query, (id_buku,))
                self.conn.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"Error delete_buku: {e}")
                return False
        return False