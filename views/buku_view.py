import customtkinter as ctk
from tkinter import ttk


class BukuView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Perpustakaan")
        self.geometry("900x500")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ===== Panel kiri: Form Data Buku =====
        self.frame_form = ctk.CTkFrame(self, width=280)
        self.frame_form.grid(row=0, column=0, padx=(15, 7), pady=15, sticky="nsew")
        self.frame_form.grid_propagate(False)

        ctk.CTkLabel(
            self.frame_form, text="Form Data Buku", font=("Arial", 16, "bold")
        ).pack(pady=(20, 15))

        self.entry_judul = ctk.CTkEntry(
            self.frame_form, placeholder_text="Masukkan Judul Buku"
        )
        self.entry_judul.pack(pady=10, padx=20, fill="x")

        self.entry_penulis = ctk.CTkEntry(
            self.frame_form, placeholder_text="Masukkan Nama Penulis"
        )
        self.entry_penulis.pack(pady=10, padx=20, fill="x")

        self.entry_tahun = ctk.CTkEntry(
            self.frame_form, placeholder_text="Tahun Terbit (Misal: 2024)"
        )
        self.entry_tahun.pack(pady=10, padx=20, fill="x")

        self.btn_simpan = ctk.CTkButton(
            self.frame_form, text="Simpan Data", fg_color="green"
        )
        self.btn_simpan.pack(pady=20, padx=20, fill="x")

        # ===== Panel kanan: Daftar Koleksi Buku =====
        self.frame_tabel = ctk.CTkFrame(self)
        self.frame_tabel.grid(row=0, column=1, padx=(7, 15), pady=15, sticky="nsew")

        ctk.CTkLabel(
            self.frame_tabel, text="Daftar Koleksi Buku", font=("Arial", 16, "bold")
        ).pack(pady=(20, 15))

        # Nama atribut HARUS "tabel" karena dipanggil BukuController
        self.tabel = ttk.Treeview(
            self.frame_tabel,
            columns=("id", "judul", "penulis", "tahun"),
            show="headings",
        )
        self.tabel.heading("id", text="ID")
        self.tabel.heading("judul", text="Judul Buku")
        self.tabel.heading("penulis", text="Penulis")
        self.tabel.heading("tahun", text="Tahun")

        self.tabel.column("id", width=50, anchor="center")
        self.tabel.column("judul", width=250)
        self.tabel.column("penulis", width=150)
        self.tabel.column("tahun", width=80, anchor="center")

        self.tabel.pack(padx=15, pady=(0, 15), fill="both", expand=True)