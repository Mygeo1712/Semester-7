"""Contoh operasi himpunan (set) pada Python."""


def main():
	# Set tidak menyimpan elemen duplikat dan tidak memiliki urutan tetap.
	A = {1, 2, 3, 4}
	B = {3, 4, 5, 6}

	print("A =", A)
	print("B =", B)
	print("Gabungan (A | B):", A | B)
	print("Irisan (A & B):", A & B)
	print("Selisih A - B:", A - B)
	print("Selisih B - A:", B - A)
	print("Selisih simetris (A ^ B):", A ^ B)
	print("A subset B:", A.issubset(B))
	print("A superset B:", A.issuperset(B))
	print("A dan B saling lepas:", A.isdisjoint(B))

	contoh = A.copy()
	contoh.add(7)
	print("Tambah 7:", contoh)
	contoh.discard(2)  # discard tidak error jika elemen tidak ada
	print("Hapus 2:", contoh)


if __name__ == "__main__":
	main()