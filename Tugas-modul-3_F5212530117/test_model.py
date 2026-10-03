"""
Pengujian untuk biodata.py dan kalkulator.py.
Jalankan: python test_model.py
"""

import unittest

import kalkulator
from biodata import Biodata


class TestKalkulator(unittest.TestCase):
    def test_tambah(self):
        self.assertEqual(kalkulator.tambah(2, 3), 5)

    def test_kurang(self):
        self.assertEqual(kalkulator.kurang(5, 3), 2)

    def test_kali(self):
        self.assertEqual(kalkulator.kali(4, 3), 12)

    def test_bagi(self):
        self.assertEqual(kalkulator.bagi(10, 2), 5)

    def test_bagi_nol(self):
        with self.assertRaises(ZeroDivisionError):
            kalkulator.bagi(5, 0)


class TestBiodata(unittest.TestCase):
    def setUp(self):
        self.b = Biodata("Budi", "F5212530117", "Informatika", 20)

    def test_atribut(self):
        self.assertEqual(self.b.nama, "Budi")
        self.assertEqual(self.b.nim, "F5212530117")
        self.assertEqual(self.b.umur, 20)

    def test_tampilkan(self):
        hasil = self.b.tampilkan()
        self.assertIn("Budi", hasil)
        self.assertIn("F5212530117", hasil)

    def test_nama_kosong(self):
        with self.assertRaises(ValueError):
            Biodata("", "F5212530117", "Informatika", 20)

    def test_umur_tidak_valid(self):
        with self.assertRaises(ValueError):
            Biodata("Budi", "F5212530117", "Informatika", 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
