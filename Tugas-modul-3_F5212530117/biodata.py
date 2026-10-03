"""Program biodata sederhana."""


class Biodata:
    def __init__(self, nama, nim, prodi, umur):
        if not nama or not nim or not prodi:
            raise ValueError("Nama, NIM, dan prodi tidak boleh kosong")
        if umur <= 0:
            raise ValueError("Umur harus lebih dari 0")
        self.nama = nama
        self.nim = nim
        self.prodi = prodi
        self.umur = umur

    def tampilkan(self):
        return (
            f"Nama  : {self.nama}\n"
            f"NIM   : {self.nim}\n"
            f"Prodi : {self.prodi}\n"
            f"Umur  : {self.umur}"
        )


def main():
    print("=== PROGRAM BIODATA ===")
    nama = input("Nama: ")
    nim = input("NIM: ")
    prodi = input("Program Studi: ")
    try:
        umur = int(input("Umur: "))
        print("\n" + Biodata(nama, nim, prodi, umur).tampilkan())
    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
