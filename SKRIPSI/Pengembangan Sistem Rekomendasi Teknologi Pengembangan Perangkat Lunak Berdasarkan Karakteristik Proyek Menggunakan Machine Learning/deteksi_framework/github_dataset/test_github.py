import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

if not token:
    print("❌ GITHUB_TOKEN tidak ditemukan.")
    print("Pastikan file .env berisi:")
    print("GITHUB_TOKEN=github_pat_xxxxxxxxx")
    sys.exit(1)

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "GitHub-Dataset-Collector"
}

try:
    response = requests.get(
        "https://api.github.com/user",
        headers=headers,
        timeout=15
    )

    print("HTTP Status:", response.status_code)

    if response.status_code == 200:
        data = response.json()

        print("✅ Token berhasil!")
        print("GitHub username:", data.get("login"))

    elif response.status_code == 401:
        print("❌ Token tidak valid atau sudah kedaluwarsa.")

    else:
        print("⚠️ Terjadi masalah:")
        print(response.text)

except requests.RequestException as e:
    print("❌ Gagal terhubung ke GitHub API:")
    print(e)
