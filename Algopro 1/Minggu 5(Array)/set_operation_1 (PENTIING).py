ten = set(range(10))
lows = {0,1,2,3,4}
odds = {1,3,5,7,9}
print(f"ten: {ten}")
# menambahkan elemen 9 ke akhir list
lows.add(9)
print("lows: ",lows)

# mencari nilai yang berbeda antara odds dan lows
lows.difference(odds)
print("difference: ",lows.difference(odds))

# mencari nilai yang sama antara odds dan lows
lows.intersection(odds)
print("intersection: ",lows.intersection(odds))

# True / false jika lows adalah subset dari 10, artinya semua elemen lows ada di 10
lows.issubset(ten)
print("issubset: ",lows.issubset(ten))

# True / false jika lows adalah subset dari odds, artinya semua elemen lows ada di odds
lows.issubset(odds)
print("issubset: ",lows.issubset(odds))

# True / false jika lows adalah superset dari odds, artinya semua elemen odds ada di 10
lows.issuperset(odds)
print("issuperset: ",lows.issuperset(odds))

# hilangkan nilai 0 di dalam  set lows
lows.remove(0)
print("remove: ",lows)

# mencari nilai yang berbeda antara lows dan odds, lalu gabungkan dengan nilai yang berbeda antara odds dan lows
lows.symmetric_difference(odds)
print("symmetric_difference: ",lows.symmetric_difference(odds))

# menambahkan semua nilai odds ke dalam set lows 
lows.union(odds)
print("union: ",lows.union(odds))

lows.clear()
print("clear: ",lows)

print("lows: ",lows)