"""
Tuple bersifat immutable, artinya tidak dapat diubah setelah dibuat. Namun, kita dapat mengubah tuple menjadi list, melakukan perubahan pada list tersebut, dan kemudian mengubahnya kembali menjadi tuple. 
Berikut adalah contoh kode yang menunjukkan cara melakukannya.

Menggunakan Kurung Biasa = ()
hampir mirip 
"""


# --- DATA AWAL ---
base = ('a', 'c', 'g', 't')
print("=== DATA AWAL ===")
print("Tuple awal :", base)
print("Akses indeks 1:", base[1]) # Output: c
print("-" * 40)


# .count() -> Menghitung jumlah kemunculan elemen
jumlah_a = base.count('a')
print("Jumlah elemen 'a'    :", jumlah_a)

# .index() -> Mencari posisi indeks pertama dari suatu elemen
posisi_g = base.index('g')
print("Posisi indeks 'g'    :", posisi_g)
print("-" * 40)


# len() -> Menghitung total panjang/jumlah elemen tuple
panjang_tuple = len(base)
print("Panjang tuple        :", panjang_tuple)

# sorted() -> Mengurutkan elemen (Hasil otomatis menjadi LIST)
hasil_urut = sorted(base, reverse=True) # reverse=True untuk urutan terbalik
print("Hasil sorted (List)  :", hasil_urut)

# Operator + (Concatenation) -> Menggabungkan dengan tuple lain menjadi tuple baru
tuple_gabung = base + ('u', 'n')
print("Hasil penggabungan   :", tuple_gabung)

# Operator * (Replication) -> Menggandakan isi tuple
tuple_ganda = base * 2
print("Hasil penggandaan    :", tuple_ganda)

# Slicing -> Memotong atau mengambil sebagian isi tuple [start:stop:step]
potongan_tuple = base[1:3] 
print("Hasil slicing [1:3]  :", potongan_tuple)
print("-" * 40)



# Ubah tuple menjadi list agar bisa dimodifikasi (karena tuple asli bersifat immutable)
base_list = list(base)
print("Bentuk List awal     :", base_list)

# A. Mengubah nilai elemen berdasarkan indeks
base_list[1] = 'x'
print("Setelah ubah indeks 1:", base_list)

# B. .append() -> Menambah elemen di akhir list
base_list.append('z')
print("Setelah .append()    :", base_list)

# C. .insert() -> Menambah elemen di indeks tertentu (misal indeks 0 / paling depan)
base_list.insert(0, 'n')
print("Setelah .insert()    :", base_list)

# D. .remove() -> Menghapus elemen berdasarkan nilainya
base_list.remove('g')
print("Setelah .remove('g') :", base_list)

# E. .pop() -> Menghapus elemen di akhir list (atau indeks tertentu)
elemen_dihapus = base_list.pop()
print(f"Setelah .pop() (menghapus '{elemen_dihapus}'):", base_list)

# F. .reverse() -> Membalikkan urutan elemen list
base_list.reverse()
print("Setelah .reverse()   :", base_list)

# Kembalikan tipe data menjadi Tuple setelah selesai dimodifikasi
base_termodifikasi = tuple(base_list)

print("\n=== HASIL AKHIR ===")
print("Tuple baru setelah dimodifikasi:", base_termodifikasi)
