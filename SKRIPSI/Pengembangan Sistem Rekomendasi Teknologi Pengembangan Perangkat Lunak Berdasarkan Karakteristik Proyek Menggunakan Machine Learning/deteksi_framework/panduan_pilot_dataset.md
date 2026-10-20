Bisa. Saya buatkan versi **pilot yang benar-benar bisa dijalankan**, dengan alur:

```text
GitHub API
   ↓
Cari 10 repository
   ↓
Ambil metadata
   ↓
Ambil bahasa
   ↓
Ambil contributors
   ↓
Ambil file dependency
   ↓
Deteksi framework
   ↓
Deteksi database
   ↓
Deteksi jenis aplikasi
   ↓
Hitung aktivitas
   ↓
dataset.csv
```

GitHub memang menyediakan endpoint resmi untuk metadata repository, bahasa, contributor, serta isi file repository. Untuk file repository, API Contents dapat mengambil isi file secara langsung. ([GitHub Docs][1])

Untuk tahap awal, saya sengaja membuat **10 repository dari beberapa framework target**, bukan 10 repository acak. Ini lebih berguna untuk menguji apakah detector kita bekerja.

## 1. Instal library

Di terminal VS Code:

```bash
pip install requests pandas python-dotenv
```

Buat struktur:

```text
github_dataset/
│
├── collect_dataset.py
├── .env
└── dataset.csv        ← otomatis dibuat
```

---

## 2. Buat GitHub Personal Access Token

Token digunakan supaya akses API lebih stabil dan rate limit lebih tinggi. GitHub memang mendukung autentikasi API dan merekomendasikan penggunaan token untuk akses API. ([GitHub Docs][1])

Buat token di GitHub, kemudian `.env`:

```text
GITHUB_TOKEN=github_pat_XXXXXXXXXXXXXXXX
```

**Jangan masukkan token ke dalam kode atau upload `.env` ke GitHub.**

Tambahkan `.gitignore`:

```text
.env
__pycache__/
dataset.csv
```

---

# 3. Kode lengkap `collect_dataset.py`

```python
import os
import re
import time
import base64
from datetime import datetime, timedelta, timezone

import requests
import pandas as pd
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise RuntimeError(
        "GITHUB_TOKEN tidak ditemukan. "
        "Buat file .env dan isi GITHUB_TOKEN=token_kamu"
    )

API_URL = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2026-03-10",
    "User-Agent": "Software-Technology-Recommender-Research"
}


# ============================================================
# TARGET REPOSITORIES
# ============================================================
#
# Untuk tahap pilot kita gunakan repository nyata yang
# mewakili beberapa framework.
#
# Nantinya daftar ini dapat diganti menjadi proses pencarian
# otomatis menggunakan GitHub Search API.
# ============================================================

REPOSITORIES = [
    "django/django",
    "pallets/flask",
    "laravel/framework",
    "symfony/symfony",
    "spring-projects/spring-boot",
    "expressjs/express",
    "nestjs/nest",
    "vercel/next.js",
    "fastapi/fastapi",
    "rails/rails",
]


# ============================================================
# HELPER: API REQUEST
# ============================================================

def github_get(url, params=None):
    """
    Melakukan GET request ke GitHub API.
    """

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()

        print(
            f"[WARNING] HTTP {response.status_code}: {url}"
        )

        try:
            print(response.json())
        except Exception:
            pass

        return None

    except requests.RequestException as e:
        print(f"[ERROR] Request gagal: {e}")
        return None


# ============================================================
# GET REPOSITORY METADATA
# ============================================================

def get_repository(owner, repo):
    """
    Mengambil metadata utama repository.
    """

    url = f"{API_URL}/repos/{owner}/{repo}"

    return github_get(url)


# ============================================================
# GET LANGUAGES
# ============================================================

def get_languages(owner, repo):
    """
    Mengambil bahasa pemrograman repository.

    GitHub mengembalikan jumlah byte kode untuk setiap bahasa.
    Bahasa dengan jumlah byte terbesar digunakan sebagai
    primary language.
    """

    url = f"{API_URL}/repos/{owner}/{repo}/languages"

    data = github_get(url)

    if not data:
        return None, {}

    sorted_languages = sorted(
        data.items(),
        key=lambda item: item[1],
        reverse=True
    )

    primary_language = sorted_languages[0][0]

    return primary_language, data


# ============================================================
# GET CONTRIBUTORS
# ============================================================

def get_contributors_count(owner, repo):
    """
    Menghitung jumlah contributor menggunakan endpoint
    contributors.

    Per_page=100 digunakan untuk mengurangi jumlah request.
    """

    url = f"{API_URL}/repos/{owner}/{repo}/contributors"

    params = {
        "per_page": 100,
        "page": 1
    }

    data = github_get(url, params)

    if not data:
        return 0

    return len(data)


# ============================================================
# GET FILE CONTENT
# ============================================================

def get_file_content(owner, repo, path):
    """
    Mengambil isi file dari root repository.

    Digunakan untuk membaca:
    - package.json
    - requirements.txt
    - pyproject.toml
    - composer.json
    - pom.xml
    - build.gradle
    - README.md
    """

    url = f"{API_URL}/repos/{owner}/{repo}/contents/{path}"

    data = github_get(url)

    if not data:
        return None

    # Pastikan object yang dikembalikan memang file
    if data.get("type") != "file":
        return None

    content = data.get("content")

    if not content:
        return None

    try:
        decoded = base64.b64decode(content)
        return decoded.decode("utf-8", errors="ignore")

    except Exception:
        return None


# ============================================================
# DETECT FRAMEWORK
# ============================================================

def detect_framework(files):
    """
    Mendeteksi framework berdasarkan file dependency.

    files merupakan dictionary:
        {
            "package.json": "...",
            "requirements.txt": "...",
            ...
        }
    """

    # --------------------------------------------------------
    # Python
    # --------------------------------------------------------

    python_files = [
        files.get("requirements.txt", ""),
        files.get("pyproject.toml", ""),
        files.get("Pipfile", "")
    ]

    python_text = "\n".join(python_files).lower()

    if re.search(r"\bdjango\b", python_text):
        return "Django"

    if re.search(r"\bfastapi\b", python_text):
        return "FastAPI"

    if re.search(r"\bflask\b", python_text):
        return "Flask"

    # --------------------------------------------------------
    # PHP
    # --------------------------------------------------------

    composer = files.get("composer.json", "").lower()

    if "laravel/framework" in composer:
        return "Laravel"

    if '"symfony/' in composer:
        return "Symfony"

    # --------------------------------------------------------
    # Java
    # --------------------------------------------------------

    pom = files.get("pom.xml", "").lower()

    if "spring-boot" in pom:
        return "Spring Boot"

    gradle = (
        files.get("build.gradle", "")
        + "\n"
        + files.get("build.gradle.kts", "")
    ).lower()

    if "spring-boot" in gradle:
        return "Spring Boot"

    # --------------------------------------------------------
    # JavaScript / TypeScript
    # --------------------------------------------------------

    package_json = files.get("package.json", "").lower()

    if '"next"' in package_json:
        return "Next.js"

    if '"@nestjs/core"' in package_json:
        return "NestJS"

    if '"express"' in package_json:
        return "Express.js"

    # --------------------------------------------------------
    # Ruby
    # --------------------------------------------------------

    gemfile = files.get("Gemfile", "").lower()

    if "rails" in gemfile:
        return "Ruby on Rails"

    return "Unknown"


# ============================================================
# DETECT DATABASE
# ============================================================

def detect_database(files):
    """
    Mendeteksi database berdasarkan dependency/configuration.

    Hasilnya merupakan indikasi database, bukan jaminan mutlak.
    """

    combined_text = "\n".join(
        value for value in files.values() if value
    ).lower()

    # PostgreSQL
    postgres_patterns = [
        "postgresql",
        "psycopg",
        "psycopg2",
        "pg",
        "postgres"
    ]

    for pattern in postgres_patterns:
        if pattern in combined_text:
            return "PostgreSQL"

    # MySQL
    mysql_patterns = [
        "mysql",
        "mysqlclient",
        "pymysql"
    ]

    for pattern in mysql_patterns:
        if pattern in combined_text:
            return "MySQL"

    # MongoDB
    mongodb_patterns = [
        "mongodb",
        "mongoose",
        "pymongo"
    ]

    for pattern in mongodb_patterns:
        if pattern in combined_text:
            return "MongoDB"

    # SQLite
    sqlite_patterns = [
        "sqlite",
        "sqlite3"
    ]

    for pattern in sqlite_patterns:
        if pattern in combined_text:
            return "SQLite"

    # Redis
    redis_patterns = [
        "redis"
    ]

    for pattern in redis_patterns:
        if pattern in combined_text:
            return "Redis"

    return "Unknown"


# ============================================================
# COUNT DEPENDENCIES
# ============================================================

def count_dependencies(files):
    """
    Menghitung dependency secara sederhana berdasarkan file
    package manager.
    """

    total = 0

    # --------------------------------------------------------
    # package.json
    # --------------------------------------------------------

    package_json = files.get("package.json")

    if package_json:

        dependencies_section = re.search(
            r'"dependencies"\s*:\s*\{(.*?)\}',
            package_json,
            re.DOTALL
        )

        dev_dependencies_section = re.search(
            r'"devDependencies"\s*:\s*\{(.*?)\}',
            package_json,
            re.DOTALL
        )

        if dependencies_section:
            total += len(
                re.findall(
                    r'"[^"]+"\s*:',
                    dependencies_section.group(1)
                )
            )

        if dev_dependencies_section:
            total += len(
                re.findall(
                    r'"[^"]+"\s*:',
                    dev_dependencies_section.group(1)
                )
            )

    # --------------------------------------------------------
    # requirements.txt
    # --------------------------------------------------------

    requirements = files.get("requirements.txt")

    if requirements:

        lines = requirements.splitlines()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            if line.startswith("-"):
                continue

            total += 1

    # --------------------------------------------------------
    # composer.json
    # --------------------------------------------------------

    composer = files.get("composer.json")

    if composer:

        require_section = re.search(
            r'"require"\s*:\s*\{(.*?)\}',
            composer,
            re.DOTALL
        )

        if require_section:

            total += len(
                re.findall(
                    r'"[^"]+"\s*:',
                    require_section.group(1)
                )
            )

    # --------------------------------------------------------
    # Maven
    # --------------------------------------------------------

    pom = files.get("pom.xml")

    if pom:

        total += len(
            re.findall(
                r"<dependency>",
                pom,
                re.IGNORECASE
            )
        )

    # --------------------------------------------------------
    # Gradle
    # --------------------------------------------------------

    gradle = (
        files.get("build.gradle", "")
        + "\n"
        + files.get("build.gradle.kts", "")
    )

    if gradle:

        total += len(
            re.findall(
                r"(implementation|api|compileOnly|runtimeOnly)\s*[\(\"]",
                gradle
            )
        )

    return total


# ============================================================
# DETECT APPLICATION TYPE
# ============================================================

def detect_application_type(files, repository):
    """
    Klasifikasi sederhana berdasarkan:
    - description
    - topics
    - README
    - dependency/framework
    """

    description = repository.get("description") or ""

    topics = repository.get("topics") or []

    readme = files.get("README.md") or ""

    text = (
        description
        + " "
        + " ".join(topics)
        + " "
        + readme
    ).lower()

    # API
    if any(
        keyword in text
        for keyword in [
            "rest api",
            "restful api",
            "api server",
            "web api",
            "backend api"
        ]
    ):
        return "API"

    # E-commerce
    if any(
        keyword in text
        for keyword in [
            "e-commerce",
            "ecommerce",
            "online shop",
            "shopping"
        ]
    ):
        return "E-commerce"

    # Dashboard
    if any(
        keyword in text
        for keyword in [
            "dashboard",
            "admin panel",
            "analytics dashboard"
        ]
    ):
        return "Dashboard"

    # Web application
    if any(
        keyword in text
        for keyword in [
            "web application",
            "web app",
            "web framework",
            "website"
        ]
    ):
        return "Web Application"

    # CLI
    if any(
        keyword in text
        for keyword in [
            "command line",
            "cli tool",
            "command-line"
        ]
    ):
        return "CLI"

    # Library
    if any(
        keyword in text
        for keyword in [
            "library",
            "framework",
            "package"
        ]
    ):
        return "Library"

    return "Unknown"


# ============================================================
# CALCULATE ACTIVITY
# ============================================================

def get_commit_activity(owner, repo):
    """
    Mengambil aktivitas commit 52 minggu terakhir.

    GitHub menyediakan endpoint statistik commit activity.
    """

    url = (
        f"{API_URL}/repos/"
        f"{owner}/{repo}/stats/commit_activity"
    )

    data = github_get(url)

    if not data or not isinstance(data, list):
        return 0, 0

    cutoff = datetime.now(timezone.utc) - timedelta(days=365)

    total_commits = 0
    active_weeks = 0

    for week in data:

        commits = week.get("total", 0)

        total_commits += commits

        if commits > 0:
            active_weeks += 1

    return total_commits, active_weeks


# ============================================================
# GET REPOSITORY FILES
# ============================================================

def get_dependency_files(owner, repo):
    """
    Mencoba mengambil file dependency/configuration yang
    umum digunakan oleh berbagai ekosistem.
    """

    candidate_files = [
        "package.json",
        "requirements.txt",
        "pyproject.toml",
        "Pipfile",
        "composer.json",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "Gemfile",
        "README.md"
    ]

    files = {}

    for filename in candidate_files:

        content = get_file_content(
            owner,
            repo,
            filename
        )

        if content is not None:

            files[filename] = content

            print(
                f"      File ditemukan: {filename}"
            )

    return files


# ============================================================
# COLLECT ONE REPOSITORY
# ============================================================

def collect_repository(full_name):

    owner, repo = full_name.split("/")

    print()
    print("=" * 70)
    print(f"Menganalisis: {full_name}")
    print("=" * 70)

    # --------------------------------------------------------
    # Metadata
    # --------------------------------------------------------

    repository = get_repository(
        owner,
        repo
    )

    if not repository:

        print("Repository gagal diambil.")

        return None

    # --------------------------------------------------------
    # Languages
    # --------------------------------------------------------

    print("  [1/7] Mengambil bahasa...")

    primary_language, languages = get_languages(
        owner,
        repo
    )

    # --------------------------------------------------------
    # Contributors
    # --------------------------------------------------------

    print("  [2/7] Mengambil contributors...")

    contributors = get_contributors_count(
        owner,
        repo
    )

    # --------------------------------------------------------
    # Files
    # --------------------------------------------------------

    print("  [3/7] Membaca dependency/configuration files...")

    files = get_dependency_files(
        owner,
        repo
    )

    # --------------------------------------------------------
    # Framework
    # --------------------------------------------------------

    print("  [4/7] Mendeteksi framework...")

    framework = detect_framework(files)

    # --------------------------------------------------------
    # Database
    # --------------------------------------------------------

    print("  [5/7] Mendeteksi database...")

    database = detect_database(files)

    # --------------------------------------------------------
    # Dependencies
    # --------------------------------------------------------

    dependency_count = count_dependencies(files)

    # --------------------------------------------------------
    # Application Type
    # --------------------------------------------------------

    application_type = detect_application_type(
        files,
        repository
    )

    # --------------------------------------------------------
    # Activity
    # --------------------------------------------------------

    print("  [6/7] Mengambil aktivitas repository...")

    total_commits, active_weeks = get_commit_activity(
        owner,
        repo
    )

    # --------------------------------------------------------
    # Final row
    # --------------------------------------------------------

    print("  [7/7] Membentuk record dataset...")

    record = {

        # Identification
        "repository": repository.get(
            "full_name"
        ),

        "repository_url": repository.get(
            "html_url"
        ),

        # Basic characteristics
        "description": repository.get(
            "description"
        ),

        "primary_language": primary_language,

        "framework": framework,

        "database": database,

        "application_type": application_type,

        # Team / project size
        "contributors": contributors,

        "repository_size_kb": repository.get(
            "size"
        ),

        "dependency_count": dependency_count,

        # Popularity
        "stars": repository.get(
            "stargazers_count"
        ),

        "forks": repository.get(
            "forks_count"
        ),

        # Activity
        "commits_last_52_weeks": total_commits,

        "active_weeks_last_52_weeks": active_weeks,

        # GitHub metadata
        "created_at": repository.get(
            "created_at"
        ),

        "updated_at": repository.get(
            "updated_at"
        ),

        "pushed_at": repository.get(
            "pushed_at"
        ),

        "archived": repository.get(
            "archived"
        ),

        "is_fork": repository.get(
            "fork"
        ),

        "topics": ", ".join(
            repository.get("topics") or []
        )
    }

    return record


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("GITHUB SOFTWARE TECHNOLOGY DATASET COLLECTOR")
    print("=" * 70)

    records = []

    for repository in REPOSITORIES:

        try:

            result = collect_repository(
                repository
            )

            if result:

                records.append(result)

        except Exception as e:

            print(
                f"[ERROR] Gagal memproses "
                f"{repository}: {e}"
            )

        # Jangan melakukan request terlalu cepat
        time.sleep(1)

    # --------------------------------------------------------
    # DataFrame
    # --------------------------------------------------------

    if not records:

        print()
        print("Tidak ada data yang berhasil dikumpulkan.")
        return

    df = pd.DataFrame(records)

    # --------------------------------------------------------
    # Save CSV
    # --------------------------------------------------------

    output_file = "dataset.csv"

    df.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    print()
    print("=" * 70)
    print("SELESAI")
    print("=" * 70)

    print(
        f"Jumlah repository : {len(df)}"
    )

    print(
        f"Dataset           : {output_file}"
    )

    print()
    print("Preview:")
    print(
        df[
            [
                "repository",
                "primary_language",
                "framework",
                "database",
                "contributors",
                "dependency_count"
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
```

---

# 4. Jalankan

Di terminal:

```bash
python collect_dataset.py
```

Jika berhasil, kamu akan mendapatkan:

```text
github_dataset/
│
├── collect_dataset.py
├── .env
├── .gitignore
└── dataset.csv
```

Contoh output terminal:

```text
======================================================================
GITHUB SOFTWARE TECHNOLOGY DATASET COLLECTOR
======================================================================

======================================================================
Menganalisis: django/django
======================================================================
  [1/7] Mengambil bahasa...
  [2/7] Mengambil contributors...
  [3/7] Membaca dependency/configuration files...
      File ditemukan: pyproject.toml
      File ditemukan: README.md
  [4/7] Mendeteksi framework...
  [5/7] Mendeteksi database...
  [6/7] Mengambil aktivitas repository...
  [7/7] Membentuk record dataset...

...
```

Lalu:

```text
SELESAI

Jumlah repository : 10
Dataset           : dataset.csv
```

---

# 5. Isi `dataset.csv`

Kolom yang dihasilkan:

```text
repository
repository_url
description
primary_language
framework
database
application_type
contributors
repository_size_kb
dependency_count
stars
forks
commits_last_52_weeks
active_weeks_last_52_weeks
created_at
updated_at
pushed_at
archived
is_fork
topics
```

Jadi kurang lebih:

| repository                  | language   | framework   | database   | contributors | dependencies |
| --------------------------- | ---------- | ----------- | ---------- | -----------: | -----------: |
| django/django               | Python     | Django      | PostgreSQL |          ... |          ... |
| pallets/flask               | Python     | Flask       | ...        |          ... |          ... |
| laravel/framework           | PHP        | Laravel     | MySQL      |          ... |          ... |
| spring-projects/spring-boot | Java       | Spring Boot | ...        |          ... |          ... |
| expressjs/express           | JavaScript | Express.js  | ...        |          ... |          ... |

**Jangan kaget jika beberapa nilai `database` atau `application_type` menjadi `Unknown`.** Itu bukan berarti program gagal. Artinya informasi yang kita gunakan belum cukup untuk menyimpulkan database/jenis aplikasinya. Untuk penelitian, ini malah perlu ditangani sebagai bagian dari tahap *data cleaning* dan validasi.

---

# 6. Ada satu hal yang perlu saya luruskan dari rancangan sebelumnya

Kode di atas adalah **prototype data collector**, bukan dataset final untuk melatih model skripsi.

Ada alasan penting.

Misalnya:

```text
django/django
```

adalah repository framework Django itu sendiri.

Kalau kita memasukkannya ke dataset sebagai:

```text
framework = Django
application_type = Library
```

itu berbeda dengan:

```text
project = Sistem Informasi Rumah Sakit
framework = Django
```

Padahal model penelitianmu membutuhkan hubungan:

> **karakteristik proyek → teknologi yang digunakan**

Bukan:

> **karakteristik framework → framework itu sendiri**

Jadi setelah collector ini berhasil, tahap berikutnya **bukan langsung training ML**.

Kita perlu mengubah strategi dataset menjadi:

```text
GitHub Repository
        ↓
Repository proyek nyata
        ↓
Karakteristik proyek
        ↓
Framework yang digunakan
        ↓
Training Dataset
```

Contohnya:

```text
repository       : hospital-management-system
language         : Python
framework        : Django
database         : PostgreSQL
contributors     : 4
dependency_count : 18
application_type : Information System
activity         : High
size             : 3200 KB
```

Baris seperti inilah yang jauh lebih berguna untuk penelitianmu.

---

## 7. Kenapa saya tidak membuat pencarian 10 repository secara acak?

Karena untuk penelitian, **sampling harus dapat dipertanggungjawabkan**.

GitHub Search API memang dapat digunakan untuk mencari repository berdasarkan query, tetapi kalau kita langsung mengambil:

```text
"django"
"laravel"
"spring"
```

hasilnya akan sangat bias terhadap repository yang terkenal.

Untuk dataset penelitian nanti saya justru menyarankan desain:

```text
             GitHub
                ↓
       Search repositories
                ↓
     Filtering criteria
                ↓
       ┌────────┴────────┐
       ↓                 ↓
   Django             Laravel
   projects           projects
       ↓                 ↓
     ...               ...
       └────────┬────────┘
                ↓
          Balanced Dataset
                ↓
       Data Validation
                ↓
          ML Dataset
```

Misalnya akhirnya:

```text
Django       200
Laravel      200
Spring Boot  200
Express      200
FastAPI      200
Next.js      200
              ───
             1200
```

Itu jauh lebih masuk akal untuk penelitian.

Dokumentasi GitHub juga menyatakan bahwa endpoint Contents dapat mengambil file repository, sedangkan endpoint Languages memberikan jumlah byte kode berdasarkan bahasa. ([GitHub Docs][2])

### Dan saya sangat menyarankan satu perubahan lagi

Untuk **versi skripsi**, kita sebaiknya menambahkan:

```text
README analysis
        +
repository structure analysis
        +
dependency analysis
        +
configuration analysis
        ↓
Application Type
Complexity
Database
Deployment
```

Dengan demikian dataset akhirnya tidak hanya berisi metadata GitHub, tetapi benar-benar menggambarkan **karakteristik proyek perangkat lunak** yang menjadi input sistem rekomendasimu.

Kalau tahap pilot ini sudah jalan, langkah berikutnya yang paling penting adalah **membuat collector versi 2 yang otomatis mencari ±100 repository per framework, menyaring repository yang tidak layak, membaca file dependency, dan menghasilkan dataset penelitian yang jauh lebih bersih**.

[1]: https://docs.github.com/en/rest?utm_source=chatgpt.com "GitHub REST API documentation - GitHub Docs"
[2]: https://docs.github.com/en/rest/repos/contents?apiversion=2022-11-11-11-11-28&utm_source=chatgpt.com "REST API endpoints for repository contents - GitHub Docs"
