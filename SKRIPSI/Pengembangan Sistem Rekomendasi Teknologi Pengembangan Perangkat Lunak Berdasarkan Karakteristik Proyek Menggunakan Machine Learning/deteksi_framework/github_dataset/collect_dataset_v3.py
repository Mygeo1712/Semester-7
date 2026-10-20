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
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "Software-Technology-Recommender-Research"
}

# ============================================================
# TARGET REPOSITORIES (V3)
# ============================================================
REPOSITORIES = [
    # Django Applications
    "getsentry/sentry",
    "saleor/saleor",
    
    # Laravel Applications
    "pterodactyl/panel",
    "koel/koel",
    
    # Spring Boot Applications
    "macrozheng/mall",
    "thingsboard/thingsboard",
    
    # Express / Node Applications
    "Requarks/wiki",
    "payloadcms/payload",
    
    # Ruby on Rails Applications
    "discourse/discourse",
    "mastodon/mastodon",
    
    # Next.js Applications
    "calcom/cal.com",
    "dubinc/dub"
]

# ============================================================
# HELPER: API REQUEST
# ============================================================

def github_get(url, params=None):
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
            
        print(f"[WARNING] HTTP {response.status_code}: {url}")
        return None
    except requests.RequestException as e:
        print(f"[ERROR] Request gagal: {e}")
        return None

# ============================================================
# GITHUB DATA GATHERING
# ============================================================

def get_repository(owner, repo):
    url = f"{API_URL}/repos/{owner}/{repo}"
    return github_get(url)

def get_languages(owner, repo):
    url = f"{API_URL}/repos/{owner}/{repo}/languages"
    data = github_get(url)
    if not data:
        return None, {}
    sorted_languages = sorted(data.items(), key=lambda item: item[1], reverse=True)
    if not sorted_languages:
        return None, {}
    return sorted_languages[0][0], data

def get_contributors_count(owner, repo):
    url = f"{API_URL}/repos/{owner}/{repo}/contributors"
    params = {"per_page": 100, "page": 1}
    data = github_get(url, params)
    return len(data) if data else 0

def get_commit_activity(owner, repo):
    url = f"{API_URL}/repos/{owner}/{repo}/stats/commit_activity"
    data = github_get(url)
    if not data or not isinstance(data, list):
        return 0, 0
    total_commits = 0
    active_weeks = 0
    for week in data:
        commits = week.get("total", 0)
        total_commits += commits
        if commits > 0:
            active_weeks += 1
    return total_commits, active_weeks

# ============================================================
# RECURSIVE FILE TREE ANALYSIS (V3)
# ============================================================

def get_repository_tree(owner, repo, branch):
    url = f"{API_URL}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    data = github_get(url)
    if data and "tree" in data:
        if data.get("truncated"):
            print("      [!] Peringatan: File tree terlalu besar (truncated)")
        return data["tree"]
    return []

def get_blob_content(url):
    data = github_get(url)
    if data and data.get("content"):
        try:
            return base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
        except:
            return None
    return None

def get_dependency_files_v3(owner, repo, branch):
    tree = get_repository_tree(owner, repo, branch)
    if not tree:
        print("      [!] Gagal mengambil file tree.")
        return {}
        
    candidate_names = [
        "package.json", "requirements.txt", "pyproject.toml",
        "Pipfile", "composer.json", "pom.xml", "build.gradle",
        "build.gradle.kts", "Gemfile", "README.md"
    ]
    
    files_content = {name: [] for name in candidate_names}
    
    for name in candidate_names:
        matching_nodes = [node for node in tree if node.get("type") == "blob" and node.get("path", "").endswith(name)]
        matching_nodes.sort(key=lambda x: x.get("path", "").count("/"))
        
        for node in matching_nodes[:3]:
            content = get_blob_content(node["url"])
            if content:
                files_content[name].append(content)
                print(f"      File ditemukan: {node['path']}")
                
    combined_files = {}
    for name, contents in files_content.items():
        if contents:
            combined_files[name] = "\n\n--- FILE BREAK ---\n\n".join(contents)
            
    return combined_files

# ============================================================
# STRICT DETECTORS (V3)
# ============================================================

def detect_framework(files, primary_language):
    """
    Mendeteksi framework dengan validasi ketat berdasarkan primary_language.
    Ini mencegah repository Ruby (seperti Mastodon) dideteksi sebagai Express.js
    hanya karena ada package.json di folder tertentu.
    """
    lang = primary_language.lower() if primary_language else ""
    
    python_files = [files.get("requirements.txt", ""), files.get("pyproject.toml", ""), files.get("Pipfile", "")]
    python_text = "\n".join(python_files).lower()
    
    composer = files.get("composer.json", "").lower()
    pom = files.get("pom.xml", "").lower()
    gradle = (files.get("build.gradle", "") + "\n" + files.get("build.gradle.kts", "")).lower()
    package_json = files.get("package.json", "").lower()
    gemfile = files.get("Gemfile", "").lower()

    # 1. Cek Framework Berdasarkan Bahasa Utama (Primary Language)
    if "ruby" in lang:
        if "rails" in gemfile: return "Ruby on Rails"
        
    elif "python" in lang:
        if re.search(r"\bdjango\b", python_text): return "Django"
        if re.search(r"\bfastapi\b", python_text): return "FastAPI"
        if re.search(r"\bflask\b", python_text): return "Flask"

    elif "php" in lang:
        if "laravel/framework" in composer: return "Laravel"
        if '"symfony/' in composer: return "Symfony"

    elif "java" in lang:
        if "spring-boot" in pom or "spring-boot" in gradle: return "Spring Boot"

    elif "typescript" in lang or "javascript" in lang:
        if '"next"' in package_json: return "Next.js"
        if '"@nestjs/core"' in package_json: return "NestJS"
        if '"express"' in package_json: return "Express.js"

    # 2. Fallback (Jika framework di bahasa utama tidak ditemukan,
    # tapi kita sangat yakin berdasarkan file dependency)
    # Ini berguna jika misal backend (Python) tapi primary repo jadi JS karena frontend sangat besar
    if "rails" in gemfile: return "Ruby on Rails"
    if "laravel/framework" in composer: return "Laravel"
    if re.search(r"\bdjango\b", python_text): return "Django"
    if "spring-boot" in pom or "spring-boot" in gradle: return "Spring Boot"
    if '"next"' in package_json: return "Next.js"
    if '"express"' in package_json: return "Express.js"

    return "Unknown"

def detect_database(files):
    combined_text = "\n".join(value for value in files.values() if value).lower()
    if any(p in combined_text for p in ["postgresql", "psycopg", "psycopg2", "pg", "postgres"]): return "PostgreSQL"
    if any(p in combined_text for p in ["mysql", "mysqlclient", "pymysql"]): return "MySQL"
    if any(p in combined_text for p in ["mongodb", "mongoose", "pymongo"]): return "MongoDB"
    if any(p in combined_text for p in ["sqlite", "sqlite3"]): return "SQLite"
    if "redis" in combined_text: return "Redis"
    return "Unknown"

def detect_application_type(files, repository):
    description = repository.get("description") or ""
    topics = repository.get("topics") or []
    readme = files.get("README.md") or ""
    text = (description + " " + " ".join(topics) + " " + readme).lower()

    if any(k in text for k in ["rest api", "restful api", "api server", "web api", "backend api"]): return "API"
    if any(k in text for k in ["e-commerce", "ecommerce", "online shop", "shopping"]): return "E-commerce"
    if any(k in text for k in ["dashboard", "admin panel", "analytics dashboard"]): return "Dashboard"
    if any(k in text for k in ["web application", "web app", "web framework", "website", "platform", "cms"]): return "Web Application"
    if any(k in text for k in ["command line", "cli tool", "command-line"]): return "CLI"
    if any(k in text for k in ["library", "framework", "package"]): return "Library"
    
    return "Unknown"

def count_dependencies(files):
    total = 0
    package_json = files.get("package.json")
    if package_json:
        deps = re.findall(r'"dependencies"\s*:\s*\{(.*?)\}', package_json, re.DOTALL)
        dev_deps = re.findall(r'"devDependencies"\s*:\s*\{(.*?)\}', package_json, re.DOTALL)
        for d in deps + dev_deps: total += len(re.findall(r'"[^"]+"\s*:', d))
            
    reqs = files.get("requirements.txt")
    if reqs:
        for line in reqs.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("-"): total += 1
                
    composer = files.get("composer.json")
    if composer:
        reqs = re.findall(r'"require"\s*:\s*\{(.*?)\}', composer, re.DOTALL)
        for r in reqs: total += len(re.findall(r'"[^"]+"\s*:', r))
            
    pom = files.get("pom.xml")
    if pom: total += len(re.findall(r"<dependency>", pom, re.IGNORECASE))
        
    gradle = files.get("build.gradle", "") + "\n" + files.get("build.gradle.kts", "")
    if gradle: total += len(re.findall(r"(implementation|api|compileOnly|runtimeOnly)\s*[\(\"]", gradle))
        
    return total

# ============================================================
# PROCESS REPOSITORY
# ============================================================

def collect_repository(full_name):
    owner, repo = full_name.split("/")
    print(f"\n{'='*70}\nMenganalisis: {full_name}\n{'='*70}")

    repository = get_repository(owner, repo)
    if not repository:
        print("Repository gagal diambil.")
        return None

    default_branch = repository.get("default_branch", "main")
    
    print("  [1/7] Mengambil bahasa...")
    primary_language, languages = get_languages(owner, repo)

    print("  [2/7] Mengambil contributors...")
    contributors = get_contributors_count(owner, repo)

    print(f"  [3/7] Membaca file dependency secara recursive (branch: {default_branch})...")
    files = get_dependency_files_v3(owner, repo, default_branch)

    print("  [4/7] Mendeteksi framework...")
    # PASSING PRIMARY LANGUAGE UNTUK VALIDASI KETAT
    framework = detect_framework(files, primary_language)

    print("  [5/7] Mendeteksi database...")
    database = detect_database(files)

    dependency_count = count_dependencies(files)

    application_type = detect_application_type(files, repository)

    print("  [6/7] Mengambil aktivitas repository...")
    total_commits, active_weeks = get_commit_activity(owner, repo)

    print("  [7/7] Membentuk record dataset...")
    record = {
        "repository": repository.get("full_name"),
        "repository_url": repository.get("html_url"),
        "description": repository.get("description"),
        "primary_language": primary_language,
        "framework": framework,
        "database": database,
        "application_type": application_type,
        "contributors": contributors,
        "repository_size_kb": repository.get("size"),
        "dependency_count": dependency_count,
        "stars": repository.get("stargazers_count"),
        "forks": repository.get("forks_count"),
        "commits_last_52_weeks": total_commits,
        "active_weeks_last_52_weeks": active_weeks,
        "created_at": repository.get("created_at"),
        "updated_at": repository.get("updated_at"),
        "topics": ", ".join(repository.get("topics") or [])
    }
    return record

# ============================================================
# MAIN
# ============================================================

def main():
    print(f"\n{'='*70}\nGITHUB SOFTWARE TECHNOLOGY DATASET COLLECTOR V3\n{'='*70}")
    records = []

    for repository in REPOSITORIES:
        try:
            result = collect_repository(repository)
            if result:
                records.append(result)
        except Exception as e:
            print(f"[ERROR] Gagal memproses {repository}: {e}")
        time.sleep(1)

    if not records:
        print("\nTidak ada data yang berhasil dikumpulkan.")
        return

    df = pd.DataFrame(records)
    output_file = "dataset_v3.csv"
    df.to_csv(output_file, index=False, encoding="utf-8-sig")

    print(f"\n{'='*70}\nSELESAI\n{'='*70}")
    print(f"Jumlah repository : {len(df)}")
    print(f"Dataset           : {output_file}\n")
    print("Preview (Fokus pada primary_language dan framework):")
    print(df[["repository", "primary_language", "framework", "database"]].to_string(index=False))

if __name__ == "__main__":
    main()
