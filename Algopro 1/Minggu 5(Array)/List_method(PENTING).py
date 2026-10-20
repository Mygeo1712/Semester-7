"""
List method
1. Append
2. Extend
3. Insert
4. Remove
5. Pop
6. Clear
7. Index
8. Count
9. Sort
10. Reverse
11. Copy

"""

List_Nilai = [90.56, 75, 85,100, 95]
List_buah = ["apel", "pisang", "jeruk", "mangga", "sirsak", "nanas"]

# List Method

# 1. Append: menambahkan satu data ke akhir list
List_Nilai.append(80)
print("Append:", List_Nilai)

# 2. Extend: menambahkan beberapa data ke akhir list
List_Nilai.extend([88, 92])
print("Extend:", List_Nilai)

# 3. Insert: menyisipkan data pada indeks tertentu = index 1 diisisipkan nilai 78
List_Nilai.insert(1, 78)
print("Insert:", List_Nilai)

# 4. Remove: menghapus data tertentu
List_Nilai.remove(78)
print("Remove:", List_Nilai)

# 5. Pop: menghapus dan mengambil data terakhir
nilai_pop = List_Nilai.pop()
print("Pop:", nilai_pop, "->", List_Nilai)

# 6. Clear: menghapus semua data dalam list
List_clear = List_Nilai.copy()
List_clear.clear()
print("Clear:", List_clear)

# 7. Index: mencari indeks suatu data
print("Index 75:", List_Nilai.index(75))

# 8. Count: menghitung jumlah kemunculan suatu data
print("Count 95:", List_Nilai.count(95))

# 9. Sort: mengurutkan data dari kecil ke besar
List_sort = List_Nilai.copy()
List_sort.sort()
print("Sort:", List_sort)

# 10. Reverse: membalik urutan data
List_reverse = List_Nilai.copy()
List_reverse.reverse()
print("Reverse:", List_reverse)

# 11. Copy: menyalin list
List_copy = List_Nilai.copy()
print("Copy:", List_copy)
