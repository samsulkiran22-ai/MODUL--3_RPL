import pytest

from models.buku_model import BukuModel


@pytest.fixture
def model(tmp_path):
    """BukuModel dengan database sementara agar tes tidak menyentuh data asli."""
    return BukuModel(str(tmp_path / "test_perpustakaan.db"))


def test_get_all_buku(model):
    # Database kosong -> list kosong
    assert model.get_all_buku() == []

    model.tambah_buku("Pemrograman Python", "Budi Santoso", 2024)
    model.tambah_buku("Basis Data", "Siti Aminah", 2022)

    hasil = model.get_all_buku()

    assert len(hasil) == 2
    assert hasil[0][1:] == ("Pemrograman Python", "Budi Santoso", 2024)
    assert hasil[1][1:] == ("Basis Data", "Siti Aminah", 2022)