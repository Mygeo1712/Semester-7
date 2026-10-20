
huruf_pilihan = ['a', 'p', 'j', 'm'] # Tentukan huruf-huruf yang ingin Anda bandingkan

huruf_terurut = sorted(huruf_pilihan, key=ord, reverse=True)   # Urutkan berdasarkan nilai ASCII (Terbesar ke Terkecil)

# Cetak hasilnya dalam bentuk tabel perbandingan

print(f"{'Huruf':<8} | {'Nilai ASCII':<12}")
print("-" * 25)

for huruf in huruf_terurut:
    teks_huruf = f"'{huruf}'"
    print(f"{teks_huruf:<8} | {ord(huruf):<12}")