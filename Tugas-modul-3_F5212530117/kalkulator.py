"""Kalkulator sederhana."""


def tambah(a, b):
    return a + b


def kurang(a, b):
    return a - b


def kali(a, b):
    return a * b


def bagi(a, b):
    if b == 0:
        raise ZeroDivisionError("Tidak bisa membagi dengan nol")
    return a / b


def main():
    print("=== KALKULATOR SEDERHANA ===")
    print("1. Tambah\n2. Kurang\n3. Kali\n4. Bagi")
    pilihan = input("Pilih operasi (1-4): ")
    try:
        a = float(input("Angka pertama: "))
        b = float(input("Angka kedua: "))
        operasi = {"1": tambah, "2": kurang, "3": kali, "4": bagi}
        if pilihan not in operasi:
            print("Pilihan tidak valid.")
            return
        print("Hasil:", operasi[pilihan](a, b))
    except ValueError:
        print("Input harus berupa angka.")
    except ZeroDivisionError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
