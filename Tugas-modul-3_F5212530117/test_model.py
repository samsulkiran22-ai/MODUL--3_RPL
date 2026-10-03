"""
Pengujian BukuModel (koneksi MySQL dipalsukan dengan mock,
jadi test bisa jalan tanpa server MySQL).
Jalankan: python test_model.py
"""

import unittest
from unittest.mock import MagicMock

from buku_model import BukuModel


class TestKoneksi(unittest.TestCase):
    def test_pakai_database_berhasil(self):
        koneksi = MagicMock()
        db = MagicMock()
        db.get_connection.return_value = koneksi
        model = BukuModel(db=db)
        self.assertIs(model.koneksi, koneksi)

    def test_koneksi_gagal(self):
        db = MagicMock()
        db.get_connection.return_value = None
        with self.assertRaises(ConnectionError):
            BukuModel(db=db)


class TestBukuModel(unittest.TestCase):
    def setUp(self):
        self.koneksi = MagicMock()
        self.cursor = MagicMock()
        self.koneksi.cursor.return_value = self.cursor
        self.model = BukuModel(self.koneksi)

    def test_buat_tabel(self):
        self.model.buat_tabel()
        self.assertIn("CREATE TABLE", self.cursor.execute.call_args[0][0])
        self.koneksi.commit.assert_called_once()

    def test_tambah_berhasil(self):
        self.cursor.lastrowid = 7
        id_baru = self.model.tambah("Python Dasar", "Budi", 2024, 85000)
        self.assertEqual(id_baru, 7)
        self.assertIn("INSERT", self.cursor.execute.call_args[0][0])
        self.assertEqual(
            self.cursor.execute.call_args[0][1],
            ("Python Dasar", "Budi", 2024, 85000),
        )
        self.koneksi.commit.assert_called_once()

    def test_tambah_judul_kosong(self):
        with self.assertRaises(ValueError):
            self.model.tambah("", "Budi", 2024, 85000)
        self.cursor.execute.assert_not_called()

    def test_tambah_penulis_kosong(self):
        with self.assertRaises(ValueError):
            self.model.tambah("Python Dasar", "  ", 2024, 85000)

    def test_tambah_harga_negatif(self):
        with self.assertRaises(ValueError):
            self.model.tambah("Python Dasar", "Budi", 2024, -1)

    def test_semua(self):
        data = [(1, "A", "X", 2020, 10000), (2, "B", "Y", 2021, 20000)]
        self.cursor.fetchall.return_value = data
        self.assertEqual(self.model.semua(), data)

    def test_cari_by_id_ada(self):
        self.cursor.fetchone.return_value = (1, "A", "X", 2020, 10000)
        self.assertEqual(self.model.cari_by_id(1)[1], "A")

    def test_cari_by_id_tidak_ada(self):
        self.cursor.fetchone.return_value = None
        self.assertIsNone(self.model.cari_by_id(99))

    def test_ubah_berhasil(self):
        self.cursor.rowcount = 1
        self.assertTrue(self.model.ubah(1, "Baru", "Penulis", 2025, 90000))
        self.assertIn("UPDATE", self.cursor.execute.call_args[0][0])

    def test_ubah_id_tidak_ada(self):
        self.cursor.rowcount = 0
        self.assertFalse(self.model.ubah(99, "Baru", "Penulis", 2025, 90000))

    def test_hapus_berhasil(self):
        self.cursor.rowcount = 1
        self.assertTrue(self.model.hapus(1))
        self.assertIn("DELETE", self.cursor.execute.call_args[0][0])

    def test_hapus_id_tidak_ada(self):
        self.cursor.rowcount = 0
        self.assertFalse(self.model.hapus(99))


if __name__ == "__main__":
    unittest.main(verbosity=2)
