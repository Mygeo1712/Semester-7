def ulangtahun(hari_ini, hari_nanti):
   sisa_hari = (hari_nanti - hari_ini)%7
   match sisa_hari:
    case 1:
      print("senin")
    case 2:
      print("selasa")
    case 3:
      print("rabu")
    case 4:
      print("kamis")
    case 5:
      print("jumat")
    case 6:
      print("sabtu")
    case 0:
      print("minggu")
   return sisa_hari

