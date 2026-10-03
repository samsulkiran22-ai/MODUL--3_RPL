"""Model untuk tabel buku (operasi CRUD) di database perpustakaan."""


class BukuModel:
    def __init__(self, koneksi=None, db=None):
        if koneksi is None:
            if db is None:
                from database import Database  # diimpor di sini agar test tidak butuh MySQL

                db = Database()
            koneksi = db.get_connection()
            if koneksi is None:
                raise ConnectionError("Tidak bisa terhubung ke database")
        self.koneksi = koneksi

    def buat_tabel(self):
        cursor = self.koneksi.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS buku (
                id INT AUTO_INCREMENT PRIMARY KEY,
                judul VARCHAR(255) NOT NULL,
                penulis VARCHAR(255) NOT NULL,
                tahun INT,
                harga DECIMAL(10, 2) DEFAULT 0
            )
            """
        )
        self.koneksi.commit()
        cursor.close()

    @staticmethod
    def _validasi(judul, penulis, harga):
        if not judul or not judul.strip():
            raise ValueError("Judul tidak boleh kosong")
        if not penulis or not penulis.strip():
            raise ValueError("Penulis tidak boleh kosong")
        if harga < 0:
            raise ValueError("Harga tidak boleh negatif")

    def tambah(self, judul, penulis, tahun, harga):
        """Menambah buku, mengembalikan id buku baru."""
        self._validasi(judul, penulis, harga)
        cursor = self.koneksi.cursor()
        cursor.execute(
            "INSERT INTO buku (judul, penulis, tahun, harga) VALUES (%s, %s, %s, %s)",
            (judul, penulis, tahun, harga),
        )
        self.koneksi.commit()
        id_baru = cursor.lastrowid
        cursor.close()
        return id_baru

    def semua(self):
        """Mengembalikan semua buku."""
        cursor = self.koneksi.cursor()
        cursor.execute("SELECT id, judul, penulis, tahun, harga FROM buku")
        hasil = cursor.fetchall()
        cursor.close()
        return hasil

    def cari_by_id(self, id_buku):
        """Mengembalikan satu buku, atau None kalau tidak ada."""
        cursor = self.koneksi.cursor()
        cursor.execute(
            "SELECT id, judul, penulis, tahun, harga FROM buku WHERE id = %s",
            (id_buku,),
        )
        hasil = cursor.fetchone()
        cursor.close()
        return hasil

    def ubah(self, id_buku, judul, penulis, tahun, harga):
        """Mengubah buku. True kalau ada data yang berubah."""
        self._validasi(judul, penulis, harga)
        cursor = self.koneksi.cursor()
        cursor.execute(
            "UPDATE buku SET judul = %s, penulis = %s, tahun = %s, harga = %s "
            "WHERE id = %s",
            (judul, penulis, tahun, harga, id_buku),
        )
        self.koneksi.commit()
        berubah = cursor.rowcount > 0
        cursor.close()
        return berubah

    def hapus(self, id_buku):
        """Menghapus buku. True kalau ada data yang terhapus."""
        cursor = self.koneksi.cursor()
        cursor.execute("DELETE FROM buku WHERE id = %s", (id_buku,))
        self.koneksi.commit()
        terhapus = cursor.rowcount > 0
        cursor.close()
        return terhapus
