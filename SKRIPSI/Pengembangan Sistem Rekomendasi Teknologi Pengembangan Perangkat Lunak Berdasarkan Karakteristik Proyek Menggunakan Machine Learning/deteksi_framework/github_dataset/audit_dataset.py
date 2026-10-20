import pandas as pd

df = pd.read_csv("dataset_v3.csv")

print("=" * 70)
print("AUDIT DATASET V3")
print("=" * 70)

print("\nJumlah baris :", len(df))
print("Jumlah kolom:", len(df.columns))

print("\nKOLOM:")
for col in df.columns:
    print("-", col)

print("\n" + "=" * 70)
print("DATA KOSONG")
print("=" * 70)

missing = df.isnull().sum()

for col, count in missing.items():
    if count > 0:
        print(f"{col}: {count}")

print("\n" + "=" * 70)
print("DISTRIBUSI FRAMEWORK")
print("=" * 70)

print(df["framework"].value_counts(dropna=False))

print("\n" + "=" * 70)
print("DISTRIBUSI DATABASE")
print("=" * 70)

print(df["database"].value_counts(dropna=False))

print("\n" + "=" * 70)
print("DISTRIBUSI BAHASA")
print("=" * 70)

print(df["primary_language"].value_counts(dropna=False))

print("\n" + "=" * 70)
print("REPOSITORY")
print("=" * 70)

print(df[[
    "repository",
    "primary_language",
    "framework",
    "database"
]].to_string(index=False))
