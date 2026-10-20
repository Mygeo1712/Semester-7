#1. Perulangan for (For Loop)

# Mengulang angka dari 1 sampai 5
for i in range(1, 6):
    print(f"Perulangan ke-{i}")

#mengulangi list  
buah = ["Apel", "Jeruk", "Mangga"]
for b in buah:
    print(f"Saya suka buah {b}")

#2. Perulangan while (While Loop)
hitung = 1
while hitung <= 3:
    print(f"Hitungan ke-{hitung}")
    hitung += 1  # Menambah nilai hitung sebesar 1 setiap perulangan


# 3. Kontrol Perulangan: break dan continue
print("--- Contoh Continue ---")
for x in range(1, 6):
    if x == 3:
        continue  # Angka 3 akan dilewati
    print(x)

print("--- Contoh Break ---")
for x in range(1, 6):
    if x == 4:
        break  # Perulangan berhenti total saat x mencapai 4
    print(x)
