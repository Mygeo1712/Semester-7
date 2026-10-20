day_number = 6

match day_number:
    case 1:
        print("Senin")
    case 2:
        print("Selasa")
    case 3:
        print("Rabu")
    case 4:
        print("Kamis")
    case 5:
        print("Jumat")
    case 6 | 7:
        print("Libur")

buah = ["nanas", "apel", "jeruk"]
for makanan in buah:
  print (f"Saya suka makan {makanan}")