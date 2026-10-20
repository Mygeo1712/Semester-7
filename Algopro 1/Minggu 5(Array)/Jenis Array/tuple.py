# ==========================================
# 4. TANDA KURUNG BIASA () — TUPLE
# ==========================================

# --- MUDAH (Easy) ---
# Membuat tuple (bersifat immutable / tidak bisa diubah setelah dibuat)
koordinat = (10, 20, 30)
print(koordinat[0])  # Output: 10

# --- MEDIUM (Medium) ---
# Tuple Unpacking: Membongkar nilai tuple ke dalam variabel terpisah
x, y, z = koordinat
print(f"X: {x}, Y: {y}, Z: {z}")

# --- HARD (Hard) ---
# Menggunakan tuple sebagai key pada dictionary (karena list tidak bisa jadi key)
# Contoh: Menyimpan data lokasi GPS sebagai key dan nama tempat sebagai value
rute_peta = {
    (-6.2088, 106.8456): "Jakarta",
    (-7.2575, 112.7521): "Surabaya"
}
lokasi_dicari = (-6.2088, 106.8456)
print(f"Koordinat {lokasi_dicari} adalah kota {rute_peta[lokasi_dicari]}")

"""
• count(x): Menghitung berapa kali elemen x muncul di dalam tuple.
• index(x): Mencari posisi indeks pertama dari elemen x.
"""