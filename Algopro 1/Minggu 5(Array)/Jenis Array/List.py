# --- MUDAH (Easy) ---
# Membuat list buah dan mengakses elemen berdasarkan indeksnya
buah = ["apel", "mangga", "pisang", "apel"]
print(buah[1])  # Output: mangga

# --- MEDIUM (Medium) ---
# Menambah, menghapus, dan melakukan perulangan (looping) pada list
buah.append("jeruk")       # Menambahkan jeruk ke akhir list
buah.remove("apel")        # Menghapus elemen "apel" pertama yang ditemukan
for b in buah:
    print(f"Buah: {b}")

# --- HARD (Hard) ---
# List Comprehension: Membuat list baru berisi kuadrat dari angka genap saja
angka = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
kuadrat_genap = [x**2 for x in angka if x % 2 == 0]
print(kuadrat_genap)  # Output: [4, 16, 36, 64, 100]


"""
fungsi pada list
• append(x): Menambahkan elemen x ke akhir list.
• insert(i, x): Menyisipkan elemen x pada indeks tertentu i.
• extend(iterable): Menggabungkan list dengan list atau koleksi lain di bagian akhir.
• remove(x): Menghapus elemen pertama yang bernilai x. Akan error jika tidak ada.
• pop(i): Menghapus dan mengembalikan elemen pada indeks i. Jika i kosong, menghapus elemen terakhir.
• clear(): Menghapus semua elemen di dalam list hingga menjadi kosong.
• index(x): Mengembalikan posisi indeks pertama dari elemen x.
• count(x): Menghitung berapa kali elemen x muncul di dalam list.
• sort(): Mengurutkan elemen list secara ascending (dari kecil ke besar). Gunakan sort(reverse=True) untuk sebaliknya.
• reverse(): Membalikkan urutan posisi elemen di dalam list.
• copy(): Membuat salinan (shallow copy) dari list tersebut.
"""