program_studi = {
    41: "Informatika",
    50: "psikologi",
    10: "kedokteran",
    11: "profesi dokter",
    14: "keperawatan",
    15: "keperawatan d3",
    17: "optometri",
    "02": "magister kecerdasan buatan", # Key berupa string
    21: "teknik elektro",
    22: "teknik industri",
    23: "program profesi insinyur",
    24: "teknik sipil",
    42: "sistem informasi",
    31: "manajemen",
    32: "akuntansi",
    61: "magister manajemen",
}

print(program_studi[10])
print(program_studi.get(41))
print(program_studi.keys())
print(program_studi.values())
print(list(program_studi.items()))
kunci = program_studi.keys()
nilai = program_studi.values()

print(list(zip(kunci, nilai)))
println([item for item in program_studi.items()])