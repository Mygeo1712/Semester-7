# List 1
color = ["red", "orange", "green", "mangga"]


print(max(color)) 
print(min(color)) 



# Pertanyaan 1 : APA yang terjadi jika kita melakukan sorted() pada list color di atas lalu hasilnya diterapkan .sort()?
hasil_sorted = sorted(color)
hasil_sorted.sort()
print(hasil_sorted)



"""
1. hasil_sorted = sorted(color)
	• Fungsi sorted() membuat list baru yang berisi elemen dari color yang sudah terurut secara alfabetis (Ascending/A-Z).
	• Isi dari variabel hasil_sorted setelah baris ini adalah: ['green', 'mangga', 'orange', 'red'].
2. hasil_sorted.sort()
	• Method .sort() digunakan untuk mengurutkan list secara langsung di tempat (in-place).
	• Karena list hasil_sorted sudah dalam keadaan terurut rapi (A-Z) dari proses sebelumnya, memanggil .sort() kembali pada list tersebut tidak mengubah posisi elemen mana pun. Karakter 'g' tetap paling depan, diikuti 'm', 'o', dan 'r'.
3. print(hasil_sorted)
	• Mencetak list yang sudah melalui dua kali proses pengurutan yang sama, sehingga hasilnya tetap ['green', 'mangga', 'orange', 'red'].

"""