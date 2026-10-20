"""
Fungsi pada Python adalah blok kode terorganisir yang dapat digunakan kembali 
untuk melakukan tugas tertentu dan hanya berjalan saat dipanggil.

ada fungsi yang tersedia di python dan fungsi juga bisa dibuat sendiri menggunakan kunci "def"
"""

# cth fungsi bawaan python
angka = -9
print(abs(angka)) # memforat angka ke bentuk positif
print(round(10.21))

# cth fungsi yang dibuat sendiri

# fungsi penjumlahan
def operasi_penjumlahan(angka1, angka2):
    hasil = angka1 + angka2
    print(hasil)

operasi_penjumlahan(10,23)
print("-" * 40)

# fungsi convert farenheit to celcius
def convert_to_celcius(farenheit):
    convert = (farenheit - 32) *5/9
    print(convert)

print("hasil convert untuk 80 adalah:")
convert_to_celcius(80)
print("-" * 40)

# fungsi convert farenheit to celcius upgrade
def convert_to_celcius(farenheit:float)->float:
    return (farenheit - 32) *5/9

print("hasil convert untuk 90 adalah: \n", convert_to_celcius(90))