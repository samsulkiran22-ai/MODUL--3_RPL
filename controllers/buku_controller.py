import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView


class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.logout_diminta = False
        self.model = BukuModel()
        self.view = BukuView()

        # Menampilkan informasi role pada judul jendela aplikasi
        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")

        # Binding tombol
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.update_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        self.view.btn_logout.configure(command=self.logout)
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_baris)

        # OTORISASI: jika bukan admin, kunci form input dan semua tombol manipulasi data
        if self.user_role != "admin":
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.btn_update.configure(state="disabled")
            self.view.btn_hapus.configure(state="disabled")
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        self.muat_data_tabel()

    # ---------- Helper ----------
    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
        data_buku = self.model.get_all_buku()
        for buku in data_buku:
            self.view.tabel.insert(
                "", "end",
                values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit'])
            )

    def bersihkan_form(self):
        self.view.entry_judul.delete(0, 'end')
        self.view.entry_penulis.delete(0, 'end')
        self.view.entry_tahun.delete(0, 'end')

    def ambil_id_terpilih(self):
        terpilih = self.view.tabel.selection()
        if not terpilih:
            return None
        return self.view.tabel.item(terpilih[0], "values")[0]

    # ---------- Event ----------
    def pilih_baris(self, event=None):
        # Isi form dari baris yang diklik (hanya untuk admin)
        if self.user_role != "admin":
            return
        terpilih = self.view.tabel.selection()
        if not terpilih:
            return
        _, judul, penulis, tahun = self.view.tabel.item(terpilih[0], "values")
        self.bersihkan_form()
        self.view.entry_judul.insert(0, judul)
        self.view.entry_penulis.insert(0, penulis)
        self.view.entry_tahun.insert(0, tahun)

    def simpan_data(self):
        # Proteksi ganda di level Controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menambah data!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        if self.model.create_buku(judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data.")

    def update_data(self):
        # Proteksi ganda di level Controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk mengubah data!")
            return

        id_buku = self.ambil_id_terpilih()
        if id_buku is None:
            messagebox.showwarning("Peringatan", "Pilih dulu data di tabel yang ingin diperbarui!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        if self.model.update_buku(id_buku, judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal memperbarui data.")

    def hapus_data(self):
        # Proteksi ganda di level Controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menghapus data!")
            return

        id_buku = self.ambil_id_terpilih()
        if id_buku is None:
            messagebox.showwarning("Peringatan", "Pilih dulu data di tabel yang ingin dihapus!")
            return

        if not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            return

        if self.model.delete_buku(id_buku):
            messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menghapus data.")

    def logout(self):
        # Tandai logout lalu hentikan mainloop; AuthController yang membuka login lagi
        self.logout_diminta = True
        self.view.quit()

    def run(self):
        """Mengembalikan True jika pengguna menekan Logout."""
        self.view.mainloop()
        try:
            self.view.destroy()
        except Exception:
            pass  # jendela sudah ditutup lewat tombol X
        return self.logout_diminta