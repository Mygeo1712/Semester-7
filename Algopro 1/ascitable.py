# Mencetak header tabel
print(f"{'Desimal':<10} | {'Karakter':<8}")
print("-" * 23)

# Loop untuk mencetak nilai ASCII dari 32 sampai 126
for i in range(32, 127):

    print(f"{i:<10} | {chr(i):<8}")
