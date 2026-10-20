# List 1
Buah = ["apel", "pisang", "jeruk", "mangga", "sirsak", "nanas"]

print(Buah[0]) #apel
print(Buah[1]) #pisang  
print(Buah[2]) #jeruk
print(Buah[3]) #mangga  

print(f"banyak data adalah : {len(Buah)}") #4
print(f"jumlah data adalah : {sum(len(buah) for buah in Buah)}") #21

print(Buah[1:3]) # cetak index 1 sampai sebelum index 3 = index 2
print(Buah[:3]) # cetak index 0 sampai sebelum index 3 = index 2
print(Buah[3:]) # cetak index 3 sampai akhir list
print(Buah[-1]) #mangga
print(Buah[-2]) #jeruk
print(Buah[-3]) #pisang
print(Buah[-4]) #apel
# print(Buah[5]) -> error karena index 5 tidak ada di list Buah


# List2 = campuran tipe data
campuran = ["apel", 1, 2.5, True]

print(campuran[0]) #apel
print(campuran[1]) #1
print(campuran[2]) #2.5
print(campuran[3]) #True

print(max(Buah)) # melihat berdasarkan ASCITABLE huruf depan terbesar terbesar (p untuk pisang, m untuk mangga, j untuk jeruk, a untuk apel) 
print(Buah[1::2]) # cetak index 1 sampai akhir list dengan step 2 = index 1,3,5


# cari data dan cek apakah ada di list Buah
print("jeruk" in Buah) #True

