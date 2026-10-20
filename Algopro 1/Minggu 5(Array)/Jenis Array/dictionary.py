# ==========================================
# 2. TANDA KURUNG KURAWAL {} — DICTIONARY
# ==========================================

# --- MUDAH (Easy) ---
# Membuat dictionary dan mengakses nilai (value) menggunakan kunci (key)
siswa = {"nama": "Budi", "umur": 20}
print(siswa["nama"])  # Output: Budi

# --- MEDIUM (Medium) ---
# Mengubah nilai, menambah key baru, dan mengambil semua key-value
siswa["umur"] = 21            # Mengubah umur menjadi 21
siswa["jurusan"] = "IT"       # Menambah key baru
for kunci, nilai in siswa.items():
    print(f"{kunci}: {nilai}")

# --- HARD (Hard) ---
# Dictionary Comprehension & Nested Dictionary (Dictionary di dalam Dictionary)
kelas = {
    "Siswa_A": {"nilai": 85, "status": "Lulus"},
    "Siswa_B": {"nilai": 60, "status": "Remedial"}
}
# Membuat dictionary baru hanya untuk siswa yang lulus menggunakan comprehension
lulus_saja = {k: v for k, v in kelas.items() if v["status"] == "Lulus"}
print(lulus_saja)


"""
fungsi pada dictionary
• keys(): Mengambil semua kunci (keys) yang ada di dalam dictionary.
• values(): Mengambil semua nilai (values) tanpa kuncinya.
• items(): Mengambil pasangan kunci dan nilai dalam bentuk tuple (key, value). Sangat berguna untuk looping.
• get(key, default): Mengambil nilai dari kunci tertentu. Jika kunci tidak ada, mengembalikan nilai default (mencegah error).
• update({key: value}): Menambahkan atau memperbarui satu atau beberapa pasangan kunci-nilai sekaligus.
• pop(key): Menghapus kunci tertentu dan mengembalikan nilai dari kunci yang dihapus tersebut.
• popitem(): Menghapus dan mengembalikan pasangan kunci-nilai terakhir yang dimasukkan.
• clear(): Mengosongkan seluruh isi dictionary.
• fromkeys(seq, value): Membuat dictionary baru dengan kunci dari sebuah urutan (seq) dan semua nilai diset sama.

"""