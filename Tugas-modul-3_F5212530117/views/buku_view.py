import customtkinter as ctk
from tkinter import ttk, messagebox

class BukuView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Perpustakaan")
        self.geometry("800x450")

        self.id_berikutnya = 1  # penghitung ID otomatis

        # Konfigurasi Grid Utama (1 Baris, 2 Kolom)
        self.grid_columnconfigure(0, weight=1) # Kolom Kiri (Form)
        self.grid_columnconfigure(1, weight=2) # Kolom Kanan (Tabel lebih lebar)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # FRAME KIRI: FORMULIR INPUT BUKU
        # ==========================================
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kiri, text="Form Data Buku - 117", font=("Arial", 16, "bold")).pack(pady=15)

        # Komponen Input
        self.entry_judul = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Judul Buku")
        self.entry_judul.pack(pady=10, padx=15, fill="x")

        self.entry_penulis = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Nama Penulis")
        self.entry_penulis.pack(pady=10, padx=15, fill="x")

        self.entry_tahun = ctk.CTkEntry(self.frame_kiri, placeholder_text="Tahun Terbit (Misal: 2024)")
        self.entry_tahun.pack(pady=10, padx=15, fill="x")

        # Tombol Aksi
        self.btn_simpan = ctk.CTkButton(self.frame_kiri, text="Simpan Data", fg_color="green",
                                        command=self.tambah_data)
        self.btn_simpan.pack(pady=(20, 5), padx=15, fill="x")

        self.btn_ubah = ctk.CTkButton(self.frame_kiri, text="Ubah Data", fg_color="#0024d9",
                                      hover_color="#b37300", command=self.ubah_data)
        self.btn_ubah.pack(pady=5, padx=15, fill="x")

        self.btn_hapus = ctk.CTkButton(self.frame_kiri, text="Hapus Data", fg_color="red",
                                       hover_color="#b30000", command=self.hapus_data)
        self.btn_hapus.pack(pady=(5, 20), padx=15, fill="x")

        # ==========================================
        # FRAME KANAN: TABEL DAFTAR BUKU
        # ==========================================
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kanan, text="Daftar Koleksi Buku - F5212530117", font=("Arial", 16, "bold")).pack(pady=15)

        # Komponen Tabel (Treeview dari tkinter standard)
        kolom = ("id", "judul", "penulis", "tahun")
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=15)

        # Konfigurasi Header Tabel
        self.tabel.heading("id", text="ID")
        self.tabel.heading("judul", text="Judul Buku")
        self.tabel.heading("penulis", text="Penulis")
        self.tabel.heading("tahun", text="Tahun")

        # Konfigurasi Lebar Kolom
        self.tabel.column("id", width=40, anchor="center")
        self.tabel.column("judul", width=150)
        self.tabel.column("penulis", width=120)
        self.tabel.column("tahun", width=80, anchor="center")

        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)

        # Klik baris tabel -> data muncul di form
        self.tabel.bind("<<TreeviewSelect>>", self.pilih_data)

    # ==========================================
    # FUNGSI BANTU
    # ==========================================
    def ambil_input(self):
        """Ambil dan validasi isian form. Mengembalikan (judul, penulis, tahun) atau None."""
        judul = self.entry_judul.get().strip()
        penulis = self.entry_penulis.get().strip()
        tahun = self.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Judul, penulis, dan tahun wajib diisi!")
            return None
        if not (tahun.isdigit() and len(tahun) == 4):
            messagebox.showwarning("Peringatan", "Tahun harus berupa 4 angka, misalnya 2024.")
            return None
        return judul, penulis, tahun

    def kosongkan_form(self):
        self.entry_judul.delete(0, "end")
        self.entry_penulis.delete(0, "end")
        self.entry_tahun.delete(0, "end")

    # ==========================================
    # FUNGSI TOMBOL
    # ==========================================
    def tambah_data(self):
        data = self.ambil_input()
        if data is None:
            return
        self.tabel.insert("", "end", values=(self.id_berikutnya, *data))
        self.id_berikutnya += 1
        self.kosongkan_form()
        messagebox.showinfo("Berhasil", "Data buku berhasil ditambahkan.")

    def pilih_data(self, event=None):
        terpilih = self.tabel.selection()
        if not terpilih:
            return
        nilai = self.tabel.item(terpilih[0], "values")
        self.kosongkan_form()
        self.entry_judul.insert(0, nilai[1])
        self.entry_penulis.insert(0, nilai[2])
        self.entry_tahun.insert(0, nilai[3])

    def ubah_data(self):
        terpilih = self.tabel.selection()
        if not terpilih:
            messagebox.showwarning("Peringatan", "Pilih dulu baris yang ingin diubah di tabel.")
            return
        data = self.ambil_input()
        if data is None:
            return
        id_buku = self.tabel.item(terpilih[0], "values")[0]
        self.tabel.item(terpilih[0], values=(id_buku, *data))
        self.kosongkan_form()
        messagebox.showinfo("Berhasil", "Data buku berhasil diubah.")

    def hapus_data(self):
        terpilih = self.tabel.selection()
        if not terpilih:
            messagebox.showwarning("Peringatan", "Pilih dulu baris yang ingin dihapus di tabel.")
            return
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            self.tabel.delete(terpilih[0])
            self.kosongkan_form()
            messagebox.showinfo("Berhasil", "Data buku berhasil dihapus.")


# Blok eksekusi untuk menguji tampilan grafis
if __name__ == "__main__":
    app = BukuView()
    app.mainloop()