import os
import re
import time
import base64
import json
from datetime import datetime
import traceback

import requests
import pandas as pd
from dotenv import load_dotenv

# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN tidak ditemukan di .env")

API_URL = "https://api.github.com"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "Software-Technology-Recommender-Research"
}

# Target pengumpulan final (>= 100 clean repositori per framework)
TARGET_PER_FRAMEWORK = 115 
MAX_API_RETRIES = 3
OUTPUT_CSV = "dataset_v4.csv"
PROCESSED_LOG = "processed_repos_v4.json"

TARGET_FRAMEWORKS = [
    {"name": "Flask", "query": "topic:flask language:python is:public archived:false stars:>15"},
    {"name": "Laravel", "query": "topic:laravel language:php is:public archived:false stars:>15"},
    {"name": "Symfony", "query": "topic:symfony language:php is:public archived:false stars:>15"},
    {"name": "Spring Boot", "query": "topic:spring-boot language:java is:public archived:false stars:>15"},
    {"name": "Express.js", "query": "topic:express language:javascript is:public archived:false stars:>15"},
    {"name": "Express.js", "query": "topic:express language:typescript is:public archived:false stars:>15"},
    {"name": "Express.js", "query": "topic:expressjs language:javascript is:public archived:false stars:>15"},
    {"name": "Next.js", "query": "topic:nextjs language:typescript is:public archived:false stars:>20"},
    {"name": "Next.js", "query": "topic:nextjs language:javascript is:public archived:false stars:>20"},
    {"name": "FastAPI", "query": "topic:fastapi language:python is:public archived:false stars:>20"},
    {"name": "Ruby on Rails", "query": "topic:rails language:ruby is:public archived:false stars:>20"},
    {"name": "Django", "query": "topic:django language:python is:public archived:false stars:>20"}
]

# Struktur log yang dipisah: accepted, rejected, failed
if os.path.exists(PROCESSED_LOG):
    with open(PROCESSED_LOG, "r") as f:
        log_data = json.load(f)
        if isinstance(log_data, list):
            # Menangani format file JSON lama yang berbentuk list
            processed_logs = {
                "accepted": set(log_data),
                "rejected": set(),
                "failed": set()
            }
        else:
            processed_logs = {
                "accepted": set(log_data.get("accepted", [])),
                "rejected": set(log_data.get("rejected", [])),
                "failed": set(log_data.get("failed", []))
            }
else:
    processed_logs = {"accepted": set(), "rejected": set(), "failed": set()}

def is_already_processed(repo_name):
    return (repo_name in processed_logs["accepted"] or 
            repo_name in processed_logs["rejected"] or 
            repo_name in processed_logs["failed"])

def save_processed_log(repo_name, status):
    processed_logs[status].add(repo_name)
    with open(PROCESSED_LOG, "w") as f:
        json.dump({
            "accepted": list(processed_logs["accepted"]),
            "rejected": list(processed_logs["rejected"]),
            "failed": list(processed_logs["failed"])
        }, f, indent=4)

# ============================================================
# API HELPERS WITH RATE LIMIT HANDLING
# ============================================================

def handle_rate_limit(response):
    if response.status_code == 403 or response.status_code == 429:
        if "rate limit" in response.text.lower():
            reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
            if reset_time > 0:
                sleep_duration = max(reset_time - time.time(), 0) + 5
                print(f"      [RATE LIMIT] API Terkena limit. Menunggu {int(sleep_duration)} detik...")
                time.sleep(sleep_duration)
                return True
    return False

def github_get(url, params=None):
    retries = 0
    while retries < MAX_API_RETRIES:
        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            elif response.status_code in [403, 429]:
                if handle_rate_limit(response):
                    continue
            
            print(f"      [WARNING] HTTP {response.status_code}: {url}")
            return None
        except requests.RequestException as e:
            print(f"      [ERROR] Request gagal: {e}")
            time.sleep(5)
            retries += 1
    return None

def search_repositories(query, limit):
    print(f"\nMencari repository: {query}")
    items = []
    page = 1
    per_page = 100 if limit >= 100 else limit

    while len(items) < limit:
        params = {"q": query, "per_page": per_page, "page": page, "sort": "stars", "order": "desc"}
        url = f"{API_URL}/search/repositories"
        data = github_get(url, params)
        if not data or "items" not in data:
            break
        
        batch = data["items"]
        if not batch:
            break
            
        items.extend(batch)
        page += 1
        
        if len(items) >= 1000 or len(batch) < per_page:
            break
            
        time.sleep(2)
    return items[:limit]

# ============================================================
# FILE SCANNING
# ============================================================

def get_repository_tree(owner, repo, branch):
    url = f"{API_URL}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    data = github_get(url)
    if data and "tree" in data:
        return data["tree"]
    return []

def get_blob_content(url):
    data = github_get(url)
    if data and data.get("content"):
        try:
            return base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
        except:
            pass
    return None

def get_dependency_and_project_files(owner, repo, branch):
    tree = get_repository_tree(owner, repo, branch)
    if not tree:
        return {}, tree
        
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
                files_content[name].append((node["path"], content))
                
    combined_files = {}
    for name, contents in files_content.items():
        if contents:
            combined_files[name] = "\n\n".join([f"### {p} ###\n{c}" for p, c in contents])
            
    return combined_files, tree

# ============================================================
# PROJECT CHARACTERISTICS
# ============================================================

def extract_project_characteristics(tree, files):
    paths = [node["path"].lower() for node in tree]
    
    has_docker = any(p.endswith("dockerfile") or p.endswith("docker-compose.yml") or p.endswith("docker-compose.yaml") for p in paths)
    has_ci_cd = any(".github/workflows/" in p or ".gitlab-ci.yml" in p or ".travis.yml" in p or "bitbucket-pipelines.yml" in p or "jenkinsfile" in p for p in paths)
    has_tests = any("tests/" in p or "__tests__/" in p or "spec/" in p or "pytest.ini" in p or "jest.config" in p or "phpunit.xml" in p for p in paths)
    
    has_documentation = any("docs/" in p or "wiki/" in p or "mkdocs.yml" in p for p in paths)
    if not has_documentation and "README.md" in files:
        has_documentation = len(files["README.md"]) > 2000
        
    monorepo = any(p in ["lerna.json", "pnpm-workspace.yaml", "nx.json", "workspace.json"] for p in paths)
    if not monorepo:
        apps_pkgs = len([p for p in paths if ("apps/" in p or "packages/" in p) and (p.endswith("package.json") or p.endswith("pom.xml"))])
        monorepo = apps_pkgs >= 2

    return int(has_docker), int(has_ci_cd), int(has_tests), int(has_documentation), int(monorepo)

def detect_repository_type(full_name, description, topics):
    full_name = full_name.lower()
    description = (description or "").lower()
    topics_text = " ".join(topics).lower()
    
    # 1. Framework repo detection
    framework_repos = [
        "django/django", "pallets/flask", "fastapi/fastapi", 
        "laravel/framework", "spring-projects/spring-boot", 
        "expressjs/express", "vercel/next.js", "rails/rails"
    ]
    is_framework = int(full_name in framework_repos)
    
    # 2. Tutorial repo detection
    tutorial_keywords = ["tutorial", "learning", "30-days", "course", "demo", "example", "learn", "study"]
    is_tutorial = int(any(k in full_name or k in description or k in topics_text for k in tutorial_keywords))
    
    # 3. Library repo detection
    library_keywords = ["library", "package", "sdk", "wrapper"]
    is_library = int(any(k in full_name or k in topics_text for k in library_keywords))
    
    return is_framework, is_tutorial, is_library

# ============================================================
# DETECTORS (WITH EVIDENCE & CONFIDENCE)
# ============================================================

def detect_framework(files, primary_language):
    lang = primary_language.lower() if primary_language else ""
    
    python_files = [files.get("requirements.txt", ""), files.get("pyproject.toml", ""), files.get("Pipfile", "")]
    python_text = "\n".join(python_files).lower()
    
    composer = files.get("composer.json", "").lower()
    pom = files.get("pom.xml", "").lower()
    gradle = (files.get("build.gradle", "") + "\n" + files.get("build.gradle.kts", "")).lower()
    package_json = files.get("package.json", "").lower()
    gemfile = files.get("Gemfile", "").lower()

    # 1. Dependency-based direct detection (Confidence High: 0.95)
    if "ruby" in lang or "rails" in gemfile:
        if "rails" in gemfile: return ("Ruby on Rails", 0.95, "Gemfile: rails")
        
    if "python" in lang or re.search(r"\b(django|fastapi|flask)\b", python_text):
        if re.search(r"\bdjango\b", python_text): return ("Django", 0.95, "Python deps: django")
        if re.search(r"\bfastapi\b", python_text): return ("FastAPI", 0.95, "Python deps: fastapi")
        if re.search(r"\bflask\b", python_text): return ("Flask", 0.95, "Python deps: flask")

    if "php" in lang or "laravel/framework" in composer or '"symfony/' in composer:
        if "laravel/framework" in composer: return ("Laravel", 0.95, "composer.json: laravel/framework")
        if '"symfony/' in composer: return ("Symfony", 0.95, "composer.json: symfony")

    if "java" in lang or "spring-boot" in pom or "spring-boot" in gradle:
        if "spring-boot" in pom or "spring-boot" in gradle: return ("Spring Boot", 0.95, "pom/gradle: spring-boot")

    if '"next"' in package_json: return ("Next.js", 0.95, "package.json: next")
    if '"@nestjs/core"' in package_json: return ("NestJS", 0.95, "package.json: @nestjs/core")
    if '"express"' in package_json: return ("Express.js", 0.95, "package.json: express")

    # Fallback (Confidence lower)
    if "rails" in gemfile: return ("Ruby on Rails", 0.70, "Gemfile: rails (fallback)")
    if "laravel/framework" in composer: return ("Laravel", 0.70, "composer.json: laravel/framework (fallback)")
    if re.search(r"\bdjango\b", python_text): return ("Django", 0.70, "Python deps: django (fallback)")
    if "spring-boot" in pom or "spring-boot" in gradle: return ("Spring Boot", 0.70, "pom/gradle: spring-boot (fallback)")

    return ("Unknown", 0.0, "")

def detect_database(files):
    combined = []
    for k, v in files.items():
        if k != "README.md":
            combined.append(f"{k}:::{v}")
    text = "\n".join(combined).lower()
    
    postgres_indicators = ["postgresql", "postgres", "psycopg", "psycopg2", "asyncpg", "pg8000", "pgvector", "pgx", "pq"]
    mysql_indicators = ["mysql", "mysqlclient", "pymysql", "mysql2", "mysqldb"]
    mongodb_indicators = ["mongodb", "mongoose", "pymongo", "motor"]
    redis_indicators = ["redis", "redis-py", "ioredis"]
    sqlite_indicators = ["sqlite", "sqlite3", "aiosqlite"]
    
    if any(re.search(rf"\b{ind}\b", text) for ind in postgres_indicators):
        return ("PostgreSQL", "dependencies mention postgresql/psycopg/dll")
    if any(re.search(rf"\b{ind}\b", text) for ind in mysql_indicators):
        return ("MySQL", "dependencies mention mysql/mysqlclient/dll")
    if any(re.search(rf"\b{ind}\b", text) for ind in mongodb_indicators):
        return ("MongoDB", "dependencies mention mongodb/mongoose/dll")
    if any(re.search(rf"\b{ind}\b", text) for ind in sqlite_indicators):
        return ("SQLite", "dependencies mention sqlite")
    if any(re.search(rf"\b{ind}\b", text) for ind in redis_indicators):
        return ("Redis", "dependencies mention redis")
        
    # Jika menggunakan ORM yang database-agnostic (seperti Prisma/TypeORM/Sequelize/SQLAlchemy)
    if any(re.search(rf"\b{orm}\b", text) for orm in ["prisma", "typeorm", "sequelize", "sqlalchemy", "hibernate"]):
        return ("Relational (ORM)", "dependencies mention orm (prisma/sqlalchemy/etc)")

    return ("Unknown", "")

def detect_application_type(files, repository):
    description = (repository.get("description") or "").lower()
    topics = repository.get("topics") or []
    topics_text = " ".join(topics).lower()
    
    # 1. Cek secara spesifik pada topics (paling akurat karena di-tag oleh developer)
    if any(k in topics_text for k in ["api", "rest-api", "backend"]): return "API"
    if any(k in topics_text for k in ["ecommerce", "e-commerce", "shop"]): return "E-commerce"
    if any(k in topics_text for k in ["dashboard", "admin-panel"]): return "Dashboard"
    if any(k in topics_text for k in ["cms", "blog", "content-management"]): return "CMS"
    if any(k in topics_text for k in ["cli", "command-line"]): return "CLI"
    
    # 2. Cek pada description (kalimat penjelasan)
    if "api " in description or "backend " in description or "restful" in description: return "API"
    if "ecommerce" in description or "e-commerce" in description: return "E-commerce"
    if "dashboard" in description or "admin panel" in description: return "Dashboard"
    if "cms " in description or "blog " in description: return "CMS"
    
    # 3. Fallback pencarian di README (dibatasi 1000 karakter pertama agar tidak bias)
    readme = (files.get("README.md") or "").lower()[:1000]
    if "ecommerce" in readme or "e-commerce" in readme: return "E-commerce"
    if "admin dashboard" in readme or "admin panel" in readme: return "Dashboard"
    if "restful api" in readme: return "API"
    
    # Jika tidak terdeteksi spesifik, asumsikan ini Web Application secara umum
    # (karena kita sudah membuang library, tutorial, dan framework repo di tahap filter)
    return "Web Application"

# [Fungsi API lainnya sama...]
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
            if line and not line.startswith("#") and not line.startswith("-") and not line.startswith("###"): total += 1
                
    composer = files.get("composer.json")
    if composer:
        reqs = re.findall(r'"require"\s*:\s*\{(.*?)\}', composer, re.DOTALL)
        for r in reqs: total += len(re.findall(r'"[^"]+"\s*:', r))
            
    pom = files.get("pom.xml")
    if pom: total += len(re.findall(r"<dependency>", pom, re.IGNORECASE))
        
    gradle = files.get("build.gradle", "") + "\n" + files.get("build.gradle.kts", "")
    if gradle: total += len(re.findall(r"(implementation|api|compileOnly|runtimeOnly)\s*[\(\"]", gradle))
        
    return total

def get_contributors_count(owner, repo):
    url = f"{API_URL}/repos/{owner}/{repo}/contributors"
    params = {"per_page": 1, "anon": 1}
    response = requests.get(url, headers=HEADERS, params=params, timeout=30)
    if response.status_code == 200:
        if "Link" in response.headers:
            links = response.headers["Link"]
            last_page = re.search(r'page=(\d+)>; rel="last"', links)
            if last_page:
                return int(last_page.group(1))
        return len(response.json())
    return 1

def get_commit_activity(owner, repo):
    url = f"{API_URL}/repos/{owner}/{repo}/stats/commit_activity"
    data = github_get(url)
    if not data or not isinstance(data, list):
        return 0, 0
    total_commits = sum(w.get("total", 0) for w in data)
    active_weeks = sum(1 for w in data if w.get("total", 0) > 0)
    return total_commits, active_weeks

# ============================================================
# PROCESS REPOSITORY
# ============================================================

def collect_repository(repository):
    full_name = repository.get("full_name")
    owner, repo = full_name.split("/")
    
    print(f"  > Mengambil data: {full_name}")

    default_branch = repository.get("default_branch", "main")
    files, tree = get_dependency_and_project_files(owner, repo, default_branch)
    if not tree:
        save_processed_log(full_name, "failed")
        return None

    primary_language = repository.get("language")

    # Framework & DB Detection
    framework, f_conf, f_ev = detect_framework(files, primary_language)
    if framework == "Unknown":
        print(f"      [REJECT] Framework tidak dikenali.")
        save_processed_log(full_name, "rejected")
        return None

    database, db_ev = detect_database(files)

    # Repository Types (Framework repo, Tutorial, Library)
    is_fw, is_tut, is_lib = detect_repository_type(full_name, repository.get("description"), repository.get("topics", []))

    # Project Characteristics
    has_docker, has_ci_cd, has_tests, has_docs, monorepo = extract_project_characteristics(tree, files)
    
    dependency_count = count_dependencies(files)
    application_type = detect_application_type(files, repository)

    total_commits, active_weeks = get_commit_activity(owner, repo)
    contributors = get_contributors_count(owner, repo)

    return {
        "repository": full_name,
        "repository_url": repository.get("html_url"),
        "primary_language": primary_language,
        "database": database,
        "application_type": application_type,
        "has_docker": has_docker,
        "has_ci_cd": has_ci_cd,
        "has_tests": has_tests,
        "has_documentation": has_docs,
        "monorepo": monorepo,
        "contributors": contributors,
        "repository_size_kb": repository.get("size"),
        "dependency_count": dependency_count,
        "stars": repository.get("stargazers_count"),
        "forks": repository.get("forks_count"),
        "commits_last_52_weeks": total_commits,
        "active_weeks_last_52_weeks": active_weeks,
        "framework": framework,
        "framework_confidence": f_conf,
        "framework_evidence": f_ev,
        "database_evidence": db_ev,
        "is_framework_repository": is_fw,
        "is_tutorial_repository": is_tut,
        "is_library_repository": is_lib
    }

# ============================================================
# MAIN
# ============================================================

def save_to_csv(record):
    df_new = pd.DataFrame([record])
    if not os.path.isfile(OUTPUT_CSV):
        df_new.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    else:
        df_new.to_csv(OUTPUT_CSV, mode="a", index=False, header=False, encoding="utf-8-sig")

def main():
    print(f"\n{'='*70}\nGITHUB DATASET COLLECTOR V4 (REFINED PILOT)\n{'='*70}")
    
    total_collected = 0
    
    # Target per framework dictionary untuk memastikan max 3 per framework,
    # meskipun Express.js dan Next.js memiliki 2 query masing-masing.
    collected_count_by_framework = {
        "Django": 0, "Flask": 0, "FastAPI": 0, "Laravel": 0, "Symfony": 0,
        "Spring Boot": 0, "Express.js": 0, "Next.js": 0, "Ruby on Rails": 0
    }
    if os.path.exists(OUTPUT_CSV):
        try:
            df_existing = pd.read_csv(OUTPUT_CSV)
            if 'framework' in df_existing.columns:
                counts = df_existing['framework'].value_counts().to_dict()
                for k in collected_count_by_framework:
                    collected_count_by_framework[k] = counts.get(k, 0)
                print("Jumlah terkumpul saat ini per framework di CSV:")
                for k, v in collected_count_by_framework.items():
                    print(f"  - {k}: {v}/{TARGET_PER_FRAMEWORK}")
        except Exception as e:
            print(f"Gagal membaca CSV existing: {e}")
    
    for fw_query in TARGET_FRAMEWORKS:
        fw_name = fw_query["name"]
        
        # Cek jika framework ini sudah memenuhi kuota (dari query sebelumnya)
        if collected_count_by_framework[fw_name] >= TARGET_PER_FRAMEWORK:
            continue
            
        print(f"\n[{fw_name}] Mengeksekusi Query: {fw_query['query']}")
        repos = search_repositories(fw_query['query'], TARGET_PER_FRAMEWORK * 3) # Cari kandidat
        
        for repo_info in repos:
            repo_name = repo_info["full_name"]
            
            if is_already_processed(repo_name):
                print(f"  > [SKIP] {repo_name} sudah ada di log.")
                continue
                
            if collected_count_by_framework[fw_name] >= TARGET_PER_FRAMEWORK:
                break
                
            try:
                record = collect_repository(repo_info)
                if record:
                    save_to_csv(record)
                    save_processed_log(repo_name, "accepted")
                    collected_count_by_framework[fw_name] += 1
                    total_collected += 1
                    print(f"      [OK] Disimpan ({collected_count_by_framework[fw_name]}/{TARGET_PER_FRAMEWORK} untuk {fw_name})")
                
            except Exception as e:
                print(f"      [ERROR] Gagal memproses {repo_name}: {e}")
                save_processed_log(repo_name, "failed")
                
            time.sleep(1) # Delay antar repo
            
    print(f"\n{'='*70}\nSELESAI\n{'='*70}")
    print(f"Total repository berhasil dikumpulkan di sesi ini: {total_collected}")
    print(f"Dataset disimpan di: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
