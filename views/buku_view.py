import customtkinter as ctk
from tkinter import ttk


class BukuView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Perpustakaan")
        self.geometry("980x620")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ===== Panel kiri: Form Data Buku =====
        self.frame_form = ctk.CTkFrame(self, width=300)
        self.frame_form.grid(row=0, column=0, padx=(12, 6), pady=12, sticky="nsew")
        self.frame_form.grid_propagate(False)

        ctk.CTkLabel(
            self.frame_form, text="Form Data Buku 117", font=("Arial", 18, "bold")
        ).pack(pady=(20, 15))

        self.entry_judul = ctk.CTkEntry(
            self.frame_form, placeholder_text="Masukkan Judul Buku", height=34
        )
        self.entry_judul.pack(pady=10, padx=18, fill="x")

        self.entry_penulis = ctk.CTkEntry(
            self.frame_form, placeholder_text="Masukkan Nama Penulis", height=34
        )
        self.entry_penulis.pack(pady=10, padx=18, fill="x")

        self.entry_tahun = ctk.CTkEntry(
            self.frame_form, placeholder_text="Tahun Terbit (Misal: 2024)", height=34
        )
        self.entry_tahun.pack(pady=10, padx=18, fill="x")

        self.btn_simpan = ctk.CTkButton(
            self.frame_form, text="Simpan Data", fg_color="green", hover_color="#006400"
        )
        self.btn_simpan.pack(pady=(10, 8), padx=18, fill="x")

        self.btn_update = ctk.CTkButton(
            self.frame_form, text="Perbarui Data (Update)", fg_color="blue", hover_color="#00008B"
        )
        self.btn_update.pack(pady=8, padx=18, fill="x")

        self.btn_hapus = ctk.CTkButton(
            self.frame_form, text="Hapus Data (Delete)", fg_color="red", hover_color="#8B0000"
        )
        self.btn_hapus.pack(pady=8, padx=18, fill="x")

        self.btn_logout = ctk.CTkButton(
            self.frame_form,
            text="Logout",
            fg_color="#FBD944",
            hover_color="#F8DB5C",
            text_color="#333333",
        )
        self.btn_logout.pack(pady=8, padx=18, fill="x")

        # ===== Panel kanan: Daftar Koleksi Buku =====
        self.frame_tabel = ctk.CTkFrame(self)
        self.frame_tabel.grid(row=0, column=1, padx=(6, 12), pady=12, sticky="nsew")

        ctk.CTkLabel(
            self.frame_tabel,
            text="Nama: Samsul Qiran  NIM:F5212530117",
            font=("Arial", 12),
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            self.frame_tabel, text="Daftar Koleksi Buku 117", font=("Arial", 18, "bold")
        ).pack(pady=(10, 15))

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
        self.tabel.column("penulis", width=170)
        self.tabel.column("tahun", width=80, anchor="center")

        self.tabel.pack(padx=15, pady=(0, 15), fill="both", expand=True)