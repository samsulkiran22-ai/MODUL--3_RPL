import pytest
from unittest.mock import MagicMock, patch
from models.buku_model import BukuModel


@pytest.fixture
def model():
    """BukuModel dengan koneksi database palsu, tanpa menyentuh MySQL asli."""
    with patch("models.buku_model.Database") as mock_db:
        mock_db.return_value.get_connection.return_value = MagicMock()
        yield BukuModel()


def test_get_all_buku(model):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        {"id_buku": 1, "judul": "Belajar Python", "penulis": "Budi", "tahun_terbit": 2020}
    ]
    model.conn.cursor.return_value = mock_cursor

    hasil = model.get_all_buku()

    assert len(hasil) == 1
    assert hasil[0]["judul"] == "Belajar Python"


def test_create_buku_berhasil(model):
    model.conn.cursor.return_value = MagicMock()

    hasil = model.create_buku("Belajar Python", "Budi", 2020)

    assert hasil is True
    model.conn.commit.assert_called_once()