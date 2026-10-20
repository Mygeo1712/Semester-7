"""
adaah sa;ah satu cabang arry menggunakan {}

"""

program_studi = {
    41: "Informatika",
    50: "psikologi",
    10: "kedokteran",
    11: "profesi dokter",
    14: "keperawatan",
    15: "keperawatan d3",
    17: "optometri",
    "02": "magister kecerdasan buatan", # Key berupa string
    21: "teknik elektro",
    22: "teknik industri",
    23: "program profesi insinyur",
    24: "teknik sipil",
    42: "sistem informasi",
    31: "manajemen",
    32: "akuntansi",
    61: "magister manajemen",
}

print("=== DATA AWAL ===")
print(program_studi)
print("-" * 50)


# A. Mengakses nilai menggunakan bracket []
# Peringatan: Cara ini akan memicu eror KeyError jika key tidak ditemukan
print("Akses key 41 dengan [] :", program_studi[41])

# B. .get() -> Mengakses nilai dengan aman 
# Jika key tidak ada, ia mengembalikan nilai default (misal: "Tidak ditemukan") tanpa bikin program eror
print("Akses dengan .get()    :", program_studi.get(10))
print("Akses key fiktif .get():", program_studi.get(99, "Kode prodi tidak ditemukan"))

# C. .keys() -> Mengambil semua kunci (key) yang ada
semua_kode = program_studi.keys()
print("Semua Key (Kode Prodi) :", list(semua_kode))

# D. .values() -> Mengambil semua nilai (value) yang ada
semua_nama = program_studi.values()
print("Semua Value (Nama)     :", list(semua_nama))

# E. .items() -> Mengambil pasangan (key, value) dalam bentuk tuple-list
print("Semua Pasangan (.items()):", list(program_studi.items())[:3], "...dst")
print("-" * 50)


# A. Mengubah nilai (Update) via bracket []
program_studi[50] = "Psikologi Klinis" # Mengubah 'psikologi' menjadi 'Psikologi Klinis'
print("Setelah diubah (key 50):", program_studi[50])

# B. Menambah data baru (Insert) via bracket []
program_studi[71] = "Desain Komunikasi Visual"
print("Setelah tambah key 71  :", program_studi[71])

# C. .update() -> Menambah atau mengubah banyak data sekaligus dari dictionary lain
prodi_baru = {81: "Hukum", 41: "Informatika Medis"} 
program_studi.update(prodi_baru) # 81 akan ditambah, 41 nilainya akan diperbarui
print("Setelah .update()      :", program_studi[41], "dan", program_studi[81])

# D. .setdefault() -> Mengambil nilai jika key ada. Jika key TIDAK ADA, otomatis menambah data baru
nilai_prodi = program_studi.setdefault(91, "Sastra Inggris")
print("Hasil .setdefault(91)  :", program_studi[91])
print("-" * 50)


# A. .pop() -> Menghapus data berdasarkan key dan mengembalikan nilai yang dihapus
dihapus = program_studi.pop(17)
print(f"Hapus key 17 (.pop())  : '{dihapus}' berhasil dihapus")

# B. .popitem() -> Menghapus data pasangan (key, value) TERAKHIR yang dimasukkan
key_akhir, val_akhir = program_studi.popitem()
print(f"Hapus data akhir       : Pasangan ({key_akhir}: '{val_akhir}') dihapus")

# C. Keyword 'del' -> Menghapus langsung berdasarkan key tanpa mengembalikan nilai
del program_studi[10]
print("Hapus key 10 (del)     : Key 10 berhasil dilenyapkan")
print("-" * 50)



# len() -> Menghitung jumlah total pasangan data di dalam dictionary
print("Total prodi saat ini   :", len(program_studi))

# .copy() -> Menduplikat dictionary secara aman (agar dictionary asli tidak ikut berubah jika hasil copy dimodifikasi)
program_studi_backup = program_studi.copy()

# .clear() -> Mengosongkan seluruh isi dictionary sekaligus
program_studi_backup.clear()
print("Hasil .clear() backup  :", program_studi_backup) # Output: {}
print("-" * 50)


print("\n=== DICTIONARY AKHIR SETELAH DIMODIFIKASI ===")
print(program_studi)


