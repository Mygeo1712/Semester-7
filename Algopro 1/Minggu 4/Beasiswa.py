try:

    #SMA
    nilai = float(input("masukkan nilai: "))

    if nilai <= 100:
        if nilai >= 80:
            if nilai >= 90:
                print("Beasiswa anda 100%")
            else:
                print("Beasiswa anda 50%")

        else:
            print("Beasiswa anda 0%")
    else:
        print("input tidak terlalu tinggi")
        

    #S1
    ipk_s1 = float(input("\nmasukkan ipk S1 (0.0 - 4.0): "))

    if ipk_s1 <= 4.0:
            if ipk_s1 >= 3.25:
                if ipk_s1 >= 3.75:
                    print("Beasiswa anda 100%")
                else:
                    print("Beasiswa anda 75%")

            else:
                print("Beasiswa anda 30%")
    else:
        print("input tidak terlalu tinggi")
        
    #S2
    ipk_s2 = float(input("\nmasukkan ipk S2 (0.0 - 4.0): "))

    if ipk_s1 <= 4.0:
        if ipk_s2 >= 3.5:
            if ipk_s2 >= 3.8:
                print("Beasiswa anda 100%")
            else:
                print("Beasiswa anda 75%")

        else:
            print("Beasiswa anda 30%")
    else:
        print("input tidak terlalu tinggi")
        
except ValueError:
    print("input tidak sesuai")