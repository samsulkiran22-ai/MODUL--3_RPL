from tkinter import messagebox


class AnggotaController:
    """Menghubungkan form + tabel Anggota (View) dengan AnggotaModel.

    View harus punya atribut:
      entry_nama, entry_nim, entry_jurusan,
      btn_simpan, btn_ubah, btn_hapus, tree (ttk.Treeview)
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.id_terpilih = None  # id_anggota dari baris tabel yang diklik

        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_ubah.configure(command=self.ubah_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        self.view.tree.bind("<<TreeviewSelect>>", self.pilih_baris)

        self.muat_data()

    # ---------- helper ----------
    def _ambil_input(self):
        nama = self.view.entry_nama.get().strip()
        nim = self.view.entry_nim.get().strip()
        jurusan = self.view.entry_jurusan.get().strip()
        if not nama or not nim or not jurusan:
            messagebox.showwarning("Peringatan", "Semua field wajib diisi!")
            return None
        return nama, nim, jurusan

    def bersihkan_form(self):
        for entry in (self.view.entry_nama, self.view.entry_nim, self.view.entry_jurusan):
            entry.delete(0, "end")
        self.id_terpilih = None
        selected = self.view.tree.selection()
        if selected:
            self.view.tree.selection_remove(selected)

    def muat_data(self):
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)
        for row in self.model.get_all_anggota():
            self.view.tree.insert("", "end", values=row)

    # ---------- event ----------
    def pilih_baris(self, event=None):
        selected = self.view.tree.selection()
        if not selected:
            return
        id_anggota, nama, nim, jurusan = self.view.tree.item(selected[0], "values")
        self.id_terpilih = int(id_anggota)

        self.view.entry_nama.delete(0, "end")
        self.view.entry_nama.insert(0, nama)
        self.view.entry_nim.delete(0, "end")
        self.view.entry_nim.insert(0, nim)
        self.view.entry_jurusan.delete(0, "end")
        self.view.entry_jurusan.insert(0, jurusan)

    # ---------- tombol ----------
    def simpan_data(self):
        data = self._ambil_input()
        if data is None:
            return
        self.model.tambah_anggota(*data)
        self.muat_data()
        self.bersihkan_form()
        messagebox.showinfo("Sukses", "Data anggota berhasil disimpan.")

    def ubah_data(self):
        if self.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih baris anggota di tabel terlebih dahulu!")
            return
        data = self._ambil_input()
        if data is None:
            return
        if self.model.update_anggota(self.id_terpilih, *data):
            self.muat_data()
            self.bersihkan_form()
            messagebox.showinfo("Sukses", "Data anggota berhasil diperbarui.")
        else:
            messagebox.showerror("Gagal", "Data anggota tidak ditemukan.")

    def hapus_data(self):
        if self.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih baris anggota di tabel terlebih dahulu!")
            return
        if not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            return
        if self.model.hapus_anggota(self.id_terpilih):
            self.muat_data()
            self.bersihkan_form()
            messagebox.showinfo("Sukses", "Data anggota berhasil dihapus.")
        else:
            messagebox.showerror("Gagal", "Data anggota tidak ditemukan.")