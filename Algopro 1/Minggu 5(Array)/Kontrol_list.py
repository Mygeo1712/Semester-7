# Nomor  pasien yang datang ke klinik day 1 - 14

Pasien_Number = [5,4,7,3,2,3,2,6,4,2,1,7,1,3]

print(len(Pasien_Number)) #banyak data adalah : 14

# akses list berdasar index
print(Pasien_Number[0]) #5
print(Pasien_Number[1]) #4


def sorted_pasien(data, descending=False):
	return sorted(data, reverse=descending)


print("Ascending:", sorted_pasien(Pasien_Number))
print("Descending:", sorted_pasien(Pasien_Number, descending=True))