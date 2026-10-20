# List_Nilai = [90.56, 75, 85,100, 95]


# for i in List_Nilai:
#     print(f"nilai mahasiswa adalah:  {i}")


# #Rataam
# nilai_rata = sum(List_Nilai)/len(List_Nilai)
# print(f"nilai rata-ratanya adalah : {nilai_rata}")

# # test looping + nilai rata
# for j in List_Nilai:
#     print(f"jumlah nilai ditambah rataan: {j + nilai_rata} ")


#Gambar segitiga
Tinggi  = 7

for i in range(Tinggi):
    Spasi = " " * (Tinggi-i)
    tulisan = "*" * (2*i-1)
    print(Spasi + tulisan)      