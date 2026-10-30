import sqlite3


class AnggotaModel:
    """Model data anggota perpustakaan (SQLite)."""

    def __init__(self, db_path="perpustakaan.db"):
        self.db_path = db_path
        self.buat_tabel()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def buat_tabel(self):
        with self._connect() as conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS anggota (
                    id_anggota INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL,
                    nim TEXT NOT NULL,
                    jurusan TEXT NOT NULL
                )"""
            )

    def tambah_anggota(self, nama, nim, jurusan):
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO anggota (nama, nim, jurusan) VALUES (?, ?, ?)",
                (nama, nim, jurusan),
            )
            return cur.lastrowid

    def get_all_anggota(self):
        with self._connect() as conn:
            return conn.execute(
                "SELECT id_anggota, nama, nim, jurusan FROM anggota ORDER BY id_anggota"
            ).fetchall()

    def update_anggota(self, id_anggota, nama, nim, jurusan):
        with self._connect() as conn:
            cur = conn.execute(
                "UPDATE anggota SET nama = ?, nim = ?, jurusan = ? WHERE id_anggota = ?",
                (nama, nim, jurusan, id_anggota),
            )
            return cur.rowcount > 0

    def hapus_anggota(self, id_anggota):
        with self._connect() as conn:
            cur = conn.execute(
                "DELETE FROM anggota WHERE id_anggota = ?", (id_anggota,)
            )
            return cur.rowcount > 0