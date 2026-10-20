"""
1. Menggunakan Operator (Simbol / Tanda)

Operator aritmatika ini digunakan secara langsung di antara angka (operan) tanpa perlu mengetik kata tertentu.

Operator	Nama Operasi	Contoh	Hasil	Keterangan
+	Penumlahan	5 + 3	8	Menambahkan dua bilangan.
-	Pengurangan	5 - 3	2	Mengurangi bilangan pertama dengan kedua.
*	Perkalian	5 * 3	15	Mengalikan dua bilangan.
/	Pembagian	5 / 2	2.5	Hasil pembagian selalu berupa pecahan (float).
//	Pembagian Bulat	5 // 2	2	Membagi dan membulatkan ke bawah (membuang sisa koma).
%	Modulo (Sisa Bagi)	5 % 2	1	Mengambil sisa dari hasil pembagian.
**	Perpangkatan	5 ** 3	125	Sama dengan \(5^{3}\).


2. Menggunakan Kata (Fungsi Bawaan / Built-in Functions)

Fungsi-fungsi ini sudah langsung tersedia di Python tanpa perlu memanggil pustaka tambahan.
• abs(x) : Mencari nilai absolut/mutlak (mengubah angka negatif menjadi positif).
	• Contoh: abs(-10) \(\rightarrow \) 10
• pow(x, y) : Alternatif dari operator ** untuk menghitung pangkat (\(x^{y}\)).
	• Contoh: pow(2, 3) \(\rightarrow \) 8
• round(x, n) : Membulatkan bilangan desimal ke bilangan terdekat atau dengan jumlah n digit di belakang koma.
	• Contoh: round(3.567, 2) \(\rightarrow \) 3.57
• divmod(x, y) : Menghasilkan sepasang nilai berupa (Hasil Pembagian Bulat, Sisa Bagi).
	• Contoh: divmod(5, 2) \(\rightarrow \) (2, 1)
• max(x, y, ...) : Mencari nilai tertinggi dari sekumpulan angka.
	• Contoh: max(1, 5, 3) \(\rightarrow \) 5
• min(x, y, ...) : Mencari nilai terendah dari sekumpulan angka.
	• Contoh: min(1, 5, 3) \(\rightarrow \) 1
• sum([x, y, ...]) : Menjumlahkan seluruh angka di dalam sebuah list/iterable.
	• Contoh: sum([1, 2, 3]) \(\rightarrow \) 6

3. Menggunakan Kata dari Modul math (Harus import math)

Untuk rumus matematika yang lebih kompleks, Python menyediakan modul math. Sebelum menggunakannya, Anda wajib menulis import math di baris paling atas kode Anda.

A. Pembulatan & Angka Dasar

• math.ceil(x) : Membulatkan angka desimal ke atas ke integer terdekat.
	• Contoh: math.ceil(4.1) \(\rightarrow \) 5
• math.floor(x) : Membulatkan angka desimal ke bawah ke integer terdekat.
	• Contoh: math.floor(4.9) \(\rightarrow \) 4
• math.fabs(x) : Sama seperti abs(), tetapi hasilnya selalu bertipe pecahan (float).
	• Contoh: math.fabs(-5) \(\rightarrow \) 5.0
• math.factorial(x) : Menghitung nilai faktorial (\(x!\)).
	• Contpe: math.factorial(4) (artinya \(4 \times 3 \times 2 \times 1\)) \(\rightarrow \) 24
• math.gcd(x, y) : Mencari FPB (Faktor Persekutuan Terbesar) dari dua angka.
	• Contoh: math.gcd(12, 18) \(\rightarrow \) 6
• math.lcm(x, y) : Mencari KPK (Kelipatan Persekutuan Terkecil) dari dua angka.
	• Contoh: math.lcm(12, 18) \(\rightarrow \) 36

B. Akar & Logaritma

• math.sqrt(x) : Menghitung akar kuadrat (\(\sqrt{x}\)).
	• Contoh: math.sqrt(25) \(\rightarrow \) 5.0
• math.cbrt(x) : Menghitung akar pangkat tiga (\(\sqrt[3]{x}\)).
	• Contoh: math.cbrt(27) \(\rightarrow \) 3.0
• math.log(x, [base]) : Menghitung logaritma \(x\). Jika base tidak diisi, otomatis menggunakan bilangan basis alami \(e\) (\(\ln x\)).
	• Contoh: math.log(100, 10) \(\rightarrow \) 2.0
• math.log10(x) : Logaritma basis 10 (\(\log_{10} x\)).
• math.log2(x) : Logaritma basis 2 (\(\log_{2} x\)).
• math.exp(x) : Menghitung nilai eksponensial \(e^{x}\).

C. Trigonometri (Sudut dalam Radian)

Catatan: Fungsi trigonometri di Python menerima inputan sudut berupa Radian, bukan Derajat.
• math.sin(x) : Menghitung nilai Sinus.
• math.cos(x) : Menghitung nilai Cosinus.
• math.tan(x) : Menghitung nilai Tangen.
• math.radians(x) : Mengonversi nilai sudut dari Derajat ke Radian.
	• Contoh: math.sin(math.radians(90)) \(\rightarrow \) 1.0
• math.degrees(x) : Mengonversi nilai sudut dari Radian ke Derajat.
• Fungsi Kebalikan (Arcus): math.asin(), math.acos(), math.atan().

D. Konstanta Matematika (Nilai Tetap)

Modul math juga menyimpan variabel angka matematika yang sudah pakem:
• math.pi : Nilai \(\pi \) (\(\approx \) 3.141592653589793).
• math.e : Nilai bilangan Euler \(e\) (\(\approx \) 2.718281828459045).
• math.tau : Nilai \(\tau \) atau sama dengan \(2\pi\) (\(\approx \) 6.283185307179586).
• math.inf : Merepresentasikan nilai tak terhingga (Infinity).
• math.nan : Merepresentasikan Not a Number (Bukan Angka).
"""