
# ==========================================
# 3. TANDA KURUNG KURAWAL {} — SET
# ==========================================

# --- MUDAH (Easy) ---
# Membuat set (elemen duplikat otomatis dihapus secara otomatis)
angka_set = {1, 2, 3, 3, 4}
print(angka_set)  # Output: {1, 2, 3, 4}

# --- MEDIUM (Medium) ---
# Operasi himpunan: Gabungan (Union) dan Irisan (Intersection)
set_a = {1, 2, 3}
set_b = {3, 4, 5}
print(set_a.union(set_b))         # Output: {1, 2, 3, 4, 5}
print(set_a.intersection(set_b))  # Output: {3}

# --- HARD (Hard) ---
# Menghapus duplikat dari sebuah list menggunakan set, lalu mengecek Symmetric Difference
list_kotor = [1, 2, 2, 3, 4, 4, 5]
set_bersih = set(list_kotor)  # Mengubah list menjadi set untuk buang duplikat
set_lain = {4, 5, 6, 7}
# Mencari elemen yang ada di salah satu set, tapi tidak di kedua-duanya
print(set_bersih.symmetric_difference(set_lain))  # Output: {1, 2, 3, 6, 7}

"""
fungsi pada set
• add(x): Menambahkan elemen x ke dalam set. Jika x sudah ada, diabaikan.
• remove(x): Menghapus elemen x. Akan error jika x tidak ditemukan.
• discard(x): Menghapus elemen x. Tidak akan error meskipun x tidak ada.
• pop(): Menghapus dan mengembalikan elemen secara acak (karena set tidak berurutan).
• clear(): Mengosongkan seluruh isi set.
"""

"""
Metode Operasi Himpunan (Matematika):
• union(other_set) atau menggunakan operator |: Menggabungkan dua set (A ∪ B).
• intersection(other_set) atau menggunakan operator &: Mengambil elemen yang ada di kedua set (Irisan / A ∩ B).
• difference(other_set) atau menggunakan operator -: Mengambil elemen di set pertama yang tidak ada di set kedua (Selisih / A - B).
• symmetric_difference(other_set) atau menggunakan operator ^: Mengambil elemen yang ada di salah satu set, tapi bukan di kedua-duanya.
• issubset(other_set): Mengecek apakah set ini merupakan bagian (subset) dari set lain.
• issuperset(other_set): Mengecek apakah set ini mencakup seluruh elemen dari set lain.
• isdisjoint(other_set): Mengecek apakah kedua set sama sekali tidak memiliki elemen yang beririsan.
"""