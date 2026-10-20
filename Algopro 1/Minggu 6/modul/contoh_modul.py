# def get_weekday(hari_ini, prediksi_hari):
#     return (hari_ini + prediksi_hari-1) % 7+1

# print(get_weekday(1,10))

# angka hari_ini adalah 1 - 365 dalam setahun
# tracking jika ulangtahun dalam tahun yang sama
print("Hari Ulangtahun di tahun ini")
def get_hari_ulangtahun(hari_ini_dalam_tahun, hari_ini_dalam_minggu, hari_ulangtahun_next):
    sisa_hari = hari_ulangtahun_next - hari_ini_dalam_tahun
    hari_apa = (hari_ini_dalam_minggu + sisa_hari) % 7 
    
    match hari_apa :
        case 1:
            print("minggu")
        case 2:
            print("senin")
        case 3:
            print("selasa")
        case 4:
            print("rabu")
        case 5:
            print("kamis")
        case 6:
            print("jumat")
        case 7:
            print("sabtu")

    return(hari_apa)

print(get_hari_ulangtahun(279,3,351))                


print("-"* 40)
# tracking jika ulangtahun itu tahun depan
print("Hari Ulangtahun di Tahun Depan")
def get_hari_ulangtahun_tahundepan(hari_ini_dalam_tahun, hari_ini_dalam_minggu, hari_ulangtahun_next):

    if hari_ulangtahun_next < hari_ini_dalam_tahun:
        sisa_hari = (365 - hari_ini_dalam_tahun) + hari_ulangtahun_next
    else:
        sisa_hari = hari_ulangtahun_next - hari_ini_dalam_tahun

    hari_apa = (hari_ini_dalam_minggu + sisa_hari + 365) % 7 
    
    match hari_apa :
        case 1:
            print("minggu")
        case 2:
            print("senin")
        case 3:
            print("selasa")
        case 4:
            print("rabu")
        case 5:
            print("kamis")
        case 6:
            print("jumat")
        case 7:
            print("sabtu")

    return(hari_apa)

print(get_hari_ulangtahun(279,3,20))     