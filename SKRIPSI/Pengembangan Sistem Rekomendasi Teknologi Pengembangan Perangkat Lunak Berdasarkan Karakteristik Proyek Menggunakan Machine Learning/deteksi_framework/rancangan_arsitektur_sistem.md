Bisa. Topik ini justru menarik kalau **jangan dibuat sebagai “website yang memilih framework”**, tetapi sebagai **sistem rekomendasi keputusan teknologi** yang memiliki data, model, pembobotan, evaluasi, dan alasan rekomendasi.

Saya sarankan arsitekturnya dibuat seperti ini.

## 1. Gambaran besar sistem

Alur utama:

```text
                 ┌─────────────────────┐
                 │      USER           │
                 │ Karakteristik       │
                 │ proyek              │
                 └──────────┬──────────┘
                            ↓
                 ┌─────────────────────┐
                 │ Preprocessing       │
                 │ - validasi          │
                 │ - encoding          │
                 │ - normalisasi       │
                 └──────────┬──────────┘
                            ↓
                 ┌─────────────────────┐
                 │ Feature Engineering │
                 │ Profil kebutuhan    │
                 │ proyek              │
                 └──────────┬──────────┘
                            ↓
                 ┌─────────────────────┐
                 │ Recommendation      │
                 │ Model               │
                 │ ML + Similarity     │
                 └──────────┬──────────┘
                            ↓
          ┌─────────────────┴─────────────────┐
          ↓                                   ↓
 ┌──────────────────┐                ┌──────────────────┐
 │ Ranking teknologi│                │ Explanation      │
 │ Django   91%     │                │ Mengapa Django?  │
 │ Laravel  82%     │                │                  │
 │ Express  77%     │                │ Python → cocok   │
 └─────────┬────────┘                └─────────┬────────┘
           └────────────────┬─────────────────┘
                            ↓
                 ┌─────────────────────┐
                 │ Hasil rekomendasi   │
                 │ + alasan            │
                 │ + skor              │
                 │ + alternatif        │
                 └─────────────────────┘
```

---

# 2. Tentukan dulu: apa sebenarnya yang direkomendasikan?

Ini penting untuk penelitian.

Jangan langsung membuat:

> "AI memilih teknologi pemrograman."

Tentukan **objek rekomendasi**.

Untuk versi pertama, saya menyarankan:

### Target rekomendasi

**Web application framework**

Misalnya:

| Teknologi   | Bahasa                |
| ----------- | --------------------- |
| Laravel     | PHP                   |
| Django      | Python                |
| Spring Boot | Java                  |
| Express.js  | JavaScript            |
| Next.js     | JavaScript/TypeScript |

Dengan begitu penelitianmu menjadi lebih terukur.

Nanti kalau sistem sudah berhasil, bisa dikembangkan menjadi:

> framework + database + deployment platform

Tetapi **jangan langsung terlalu luas**. Untuk skripsi, framework saja sudah cukup.

---

# 3. Tentukan karakteristik proyek

Ini menjadi bagian paling penting karena inilah yang membedakan sistemmu dari rekomendasi berdasarkan popularitas.

Saya sarankan input dibagi menjadi beberapa kelompok.

### A. Karakteristik aplikasi

```text
Jenis aplikasi
- Sistem informasi
- E-commerce
- API
- SaaS
- Dashboard
- Real-time application
```

### B. Skala

```text
Jumlah pengguna
- <100
- 100–1.000
- 1.000–10.000
- >10.000

Kompleksitas
- Rendah
- Sedang
- Tinggi
```

### C. Tim

```text
Jumlah developer
- 1
- 2–5
- 6–10
- >10

Pengalaman tim
- PHP
- Python
- Java
- JavaScript
- TypeScript
```

### D. Infrastruktur

```text
Deployment
- Shared hosting
- VPS
- Cloud
- Container

Database
- MySQL
- PostgreSQL
- MongoDB
```

### E. Kebutuhan sistem

```text
Real-time
Authentication
REST API
High scalability
Rapid development
Security
Maintainability
```

### F. Constraint

```text
Budget
- Rendah
- Sedang
- Tinggi

Time to market
- Cepat
- Sedang
- Tidak terlalu penting
```

---

# 4. Contoh data input

Misalnya user memasukkan:

```text
Jenis aplikasi       : Sistem Informasi
Pengguna             : 5.000
Kompleksitas         : Sedang

Developer            : 2
Pengalaman           : Python

Database             : PostgreSQL
Deployment           : Cloud

Real-time             : Tidak
REST API              : Ya

Budget               : Rendah
Time to market       : Cepat
```

Data tersebut kemudian diubah menjadi fitur numerik.

Contohnya:

```text
Python experience = 1
PHP experience    = 0
Java experience   = 0
JS experience     = 0

Complexity        = 0.6
Users             = 0.7
Budget            = 0.2
Cloud             = 1
API requirement   = 1
```

Data inilah yang masuk ke sistem rekomendasi.

---

# 5. Dari mana dataset-nya?

**Ini adalah tantangan terbesar penelitianmu.**

Karena kamu tidak bisa sekadar mengambil dataset:

> project → framework

sebanyak 100.000 baris secara langsung.

Maka saya menyarankan membuat **dataset proyek-teknologi** yang memiliki dua komponen:

### Dataset karakteristik proyek

Contoh:

| Project | Users | Complexity | Team | Experience | DB         | Cloud | API | Framework |
| ------- | ----: | ---------- | ---: | ---------- | ---------- | ----- | --- | --------- |
| P001    |   500 | Low        |    2 | Python     | PostgreSQL | Yes   | Yes | Django    |
| P002    |  5000 | Medium     |    3 | PHP        | MySQL      | Yes   | Yes | Laravel   |
| P003    | 10000 | High       |    8 | Java       | PostgreSQL | Yes   | Yes | Spring    |
| P004    |   300 | Low        |    1 | JavaScript | MongoDB    | No    | Yes | Express   |

Namun **jangan mengarang data seolah-olah merupakan data proyek nyata**.

Ada beberapa pendekatan yang lebih akademis.

### Pilihan A — Dataset dari proyek open source

Ambil repository open source dari GitHub.

Kemudian ekstrak:

* bahasa pemrograman
* framework
* jumlah contributor
* ukuran repository
* dependencies
* database
* jenis aplikasi
* aktivitas repository

Lalu karakteristik proyek dibentuk dari metadata tersebut.

**Ini paling kuat secara akademis.**

### Pilihan B — Dataset survei

Kamu membuat kuesioner kepada developer.

Contohnya:

> "Untuk proyek dengan karakteristik berikut, teknologi apa yang digunakan/dipilih?"

Target misalnya:

**50–100 responden.**

### Pilihan C — Hybrid

Menurut saya **ini yang paling bagus untuk skripsimu**:

```text
Open-source project
        +
Survey developer
        ↓
Dataset
        ↓
Training recommendation model
```

Dengan begitu kamu tidak hanya mengandalkan opini pribadi.

---

# 6. Metode Machine Learning yang saya sarankan

Jangan langsung menggunakan deep learning.

Untuk penelitianmu, saya lebih menyarankan:

## Content-Based Recommendation + Similarity

Konsepnya:

```text
Profil proyek user
        ↓
Bandingkan dengan
profil teknologi
        ↓
Hitung similarity
        ↓
Ranking
```

Misalnya proyek user:

```text
Python = tinggi
PostgreSQL = tinggi
Cloud = tinggi
Scalability = sedang
Team = kecil
```

Kemudian sistem memiliki profil:

```text
Django:
Python        = 1.0
PostgreSQL    = 0.9
Cloud         = 0.8
Scalability   = 0.8
Small Team    = 0.9

Laravel:
Python        = 0
PostgreSQL    = 0.8
Cloud         = 0.8
Scalability   = 0.8
Small Team    = 0.9
```

Similarity dihitung.

Misalnya:

```text
Django      0.91
Laravel     0.82
Express     0.77
Spring Boot 0.63
```

---

# 7. Tetapi di sinilah novelty bisa diperkuat

Kalau hanya:

> TF-IDF + cosine similarity

novelty-nya menurut saya **belum cukup kuat** untuk skripsi.

Saya akan membuat sistem menjadi:

### Hybrid Recommendation

```text
                    Project Profile
                          │
              ┌───────────┴───────────┐
              ↓                       ↓
       Content Similarity       Compatibility Score
              │                       │
              │                 Python → Django
              │                 PostgreSQL → Django
              │                 Cloud → Django
              ↓                       ↓
              └───────────┬───────────┘
                          ↓
                    Hybrid Score
                          ↓
                       Ranking
```

Misalnya:

[
Score = 0.6(Similarity) + 0.4(Compatibility)
]

atau bobot tersebut ditentukan berdasarkan eksperimen.

---

# 8. Compatibility Score

Ini bagian yang menurut saya bisa menjadi **identitas penelitianmu**.

Misalnya:

### Django

```text
Python experience       +30
PostgreSQL              +20
Cloud deployment        +15
Small team              +10
Rapid development       +10
API requirement         +10
-----------------------------
Total                   95
```

### Laravel

```text
PHP experience          +0
PostgreSQL              +20
Cloud deployment        +15
Small team              +10
Rapid development       +10
API requirement         +10
-----------------------------
Total                   65
```

Kemudian digabungkan dengan similarity.

Jadi sistem bukan hanya mengatakan:

> "Django populer."

Tetapi:

> "Django memiliki tingkat kecocokan paling tinggi terhadap karakteristik proyek yang diberikan."

---

# 9. Tambahkan Explainable Recommendation

Ini menurut saya **wajib**.

Jangan hanya menghasilkan:

```text
Django
91%
```

Tetapi:

> **Django — 91%**
>
> Django memperoleh skor tertinggi karena proyek membutuhkan pengembangan cepat, tim memiliki pengalaman Python, menggunakan PostgreSQL, dan target deployment berada pada lingkungan cloud.
>
> **Kelebihan untuk proyek ini:**
>
> * sesuai dengan pengalaman tim Python
> * mendukung PostgreSQL
> * cocok untuk pengembangan aplikasi web
> * memiliki ekosistem yang matang
>
> **Pertimbangan:**
>
> * membutuhkan pemahaman struktur Django
> * fleksibilitas tertentu dapat membutuhkan konfigurasi tambahan

Ini membuat sistemmu lebih **decision-support system**, bukan sekadar classifier.

---

# 10. Arsitektur aplikasi

Saya menyarankan:

```text
Frontend
   │
   │ HTTP
   ↓
Streamlit / Web UI
   │
   ↓
Recommendation API
   │
   ├── Preprocessing
   │
   ├── ML Model
   │
   ├── Similarity Engine
   │
   ├── Compatibility Engine
   │
   └── Explanation Engine
   │
   ↓
Database
```

Kalau kamu ingin pengerjaan lebih sederhana:

```text
Streamlit
   │
   ├── Input Form
   ├── Recommendation Engine
   ├── Explanation
   └── Result
```

Karena kamu sudah pernah menggunakan **Python dan Streamlit**, saya justru menyarankan Streamlit untuk prototype penelitian.

---

# 11. Struktur program

Misalnya:

```text
software_recommender/
│
├── app.py
│
├── data/
│   ├── projects.csv
│   ├── technologies.csv
│   └── compatibility_rules.csv
│
├── models/
│   └── recommendation_model.pkl
│
├── src/
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── similarity.py
│   ├── recommendation.py
│   ├── compatibility.py
│   └── explanation.py
│
├── evaluation/
│   ├── evaluation.py
│   └── results.csv
│
└── requirements.txt
```

---

# 12. Flow pengerjaan dari awal sampai selesai

Saya akan membaginya menjadi **10 tahap**.

### Tahap 1 — Studi literatur

Cari penelitian mengenai:

* software technology recommendation
* recommender system
* technology selection
* framework recommendation
* content-based recommendation
* hybrid recommendation
* explainable recommendation
* software engineering decision support

Tujuannya bukan hanya mencari referensi, tetapi menemukan:

> **apa yang belum dilakukan penelitian sebelumnya.**

---

### Tahap 2 — Menentukan ruang lingkup

Batasi:

```text
Objek:
Web application framework

Teknologi:
Django
Laravel
Spring Boot
Express.js
Next.js

Input:
Karakteristik proyek

Output:
Ranking framework
+
explanation
```

Dengan batasan ini penelitian menjadi realistis.

---

### Tahap 3 — Menentukan fitur

Buat tabel:

```text
Feature
│
├── Project Type
├── User Scale
├── Complexity
├── Team Size
├── Developer Experience
├── Database
├── Deployment
├── API Requirement
├── Real-time Requirement
├── Scalability
├── Budget
└── Time-to-Market
```

Kemudian tentukan bagaimana setiap fitur direpresentasikan.

---

### Tahap 4 — Membuat dataset

```text
Collect Data
     ↓
Cleaning
     ↓
Labeling
     ↓
Feature Engineering
     ↓
Dataset Final
```

Targetkan dataset yang cukup untuk eksperimen.

Misalnya:

**500–2.000 project records**

kalau memungkinkan.

Kalau dataset jauh lebih kecil, metode dan klaim penelitian harus disesuaikan.

---

### Tahap 5 — Preprocessing

Contohnya:

```text
Categorical data
       ↓
One Hot Encoding

Numerical data
       ↓
Normalization

Missing value
       ↓
Imputation

Text data
       ↓
TF-IDF
```

Hasil akhirnya:

```text
Project → vector
Technology → vector
```

---

### Tahap 6 — Membuat baseline

Ini penting untuk skripsi.

Jangan hanya membuat satu model.

Bandingkan:

```text
Baseline 1
Popularitas teknologi

vs

Baseline 2
Content-Based Recommendation

vs

Model penelitian
Hybrid Recommendation
```

Dengan demikian kamu bisa menunjukkan:

> apakah metode yang kamu usulkan memang lebih baik?

---

# 13. Tahap 7 — Training/modeling

Eksperimen dapat dibuat seperti:

```text
Model A
Cosine Similarity

Model B
KNN Recommendation

Model C
Random Forest

Model D
Hybrid Recommendation
```

Kemudian bandingkan performanya.

Tetapi saya **tidak menyarankan memasukkan terlalu banyak algoritma hanya supaya terlihat AI**.

Lebih baik:

> **1 baseline + 1 metode utama + 1 metode pembanding.**

Misalnya:

```text
Baseline:
Popularity

Pembanding:
KNN

Metode utama:
Hybrid Content-Based Recommendation
```

---

# 14. Tahap 8 — Evaluasi

Karena ini recommendation system, metriknya sebaiknya bukan hanya:

> Accuracy

Gunakan:

### Precision@K

Contoh:

```text
Precision@3
```

Apakah rekomendasi yang benar masuk ke tiga hasil teratas?

### Recall@K

Apakah teknologi yang relevan berhasil ditemukan?

### NDCG@K

Mengukur kualitas ranking.

Misalnya:

```text
Django       relevant
Laravel      relevant
Express      kurang relevant
Spring       tidak relevant
```

Ranking menjadi penting.

---

# 15. Evaluasi tambahan yang sangat bagus

Lakukan **user evaluation**.

Misalnya berikan 10 skenario proyek kepada developer/mahasiswa.

Kemudian:

```text
User memilih framework
        ↓
Sistem memberikan rekomendasi
        ↓
Bandingkan
        ↓
Apakah rekomendasi sesuai?
```

Bisa menggunakan:

```text
Relevance
1–5

Usefulness
1–5

Explanation clarity
1–5
```

Ini akan memperkuat penelitianmu.

---

# 16. Tahap 9 — Bangun aplikasi

UI sederhananya:

```text
========================================
 SOFTWARE TECHNOLOGY RECOMMENDER
========================================

Project Type
[ Sistem Informasi       ▼ ]

Expected Users
[ 5.000                  ]

Team Size
[ 2                      ]

Team Experience
[ Python                 ▼ ]

Database
[ PostgreSQL             ▼ ]

Deployment
[ Cloud                  ▼ ]

Complexity
[ Medium                 ▼ ]

API Required
[ ✓ ]

Real-time
[ ]

             [ RECOMMEND ]
========================================
```

Kemudian hasil:

```text
RECOMMENDATION

🥇 Django
Compatibility: 91%

🥈 Laravel
Compatibility: 82%

🥉 Express.js
Compatibility: 77%


WHY DJANGO?

✓ Team has Python experience
✓ PostgreSQL is supported
✓ Suitable for web applications
✓ Suitable for rapid development

CONSIDERATIONS

• Django has a relatively opinionated structure
• Python ecosystem knowledge is required
```

---

# 17. Tahap 10 — Pengujian

Pengujian dibagi menjadi:

### Pengujian sistem

```text
Functional Testing
Usability Testing
Black-box Testing
```

### Pengujian model

```text
Precision@K
Recall@K
NDCG@K
```

### Pengujian pengguna

```text
Recommendation relevance
Explanation usefulness
User satisfaction
```

---

# 18. Flow penelitian keseluruhan

Kalau dimasukkan ke proposal skripsi, alurnya bisa dibuat:

```text
Identifikasi Masalah
        ↓
Studi Literatur
        ↓
Analisis Penelitian Terdahulu
        ↓
Identifikasi Research Gap
        ↓
Penentuan Karakteristik Proyek
        ↓
Pengumpulan Dataset
        ↓
Data Preprocessing
        ↓
Feature Engineering
        ↓
Pembangunan Baseline
        ↓
Pengembangan Recommendation Model
        ↓
Hybrid Scoring
        ↓
Explanation Engine
        ↓
Implementasi Aplikasi
        ↓
Pengujian Model
        ↓
Pengujian Pengguna
        ↓
Analisis Hasil
        ↓
Kesimpulan
```

---

# 19. Di mana letak novelty-nya?

Ini bagian yang **jangan sampai salah** ketika nanti kamu presentasi ke dosen.

Novelty jangan diklaim:

> "Saya membuat sistem rekomendasi framework."

Itu terlalu umum.

Lebih kuat jika:

> **Penelitian mengembangkan sistem rekomendasi teknologi pengembangan perangkat lunak yang menggabungkan kesesuaian karakteristik proyek, kompetensi tim pengembang, kebutuhan teknis, dan kondisi deployment untuk menghasilkan ranking teknologi beserta penjelasan alasan rekomendasinya.**

Jadi kontribusinya kira-kira:

```text
Project Characteristics
          +
Developer Competency
          +
Technical Requirements
          +
Infrastructure
          ↓
Hybrid Recommendation
          ↓
Ranking
          +
Explainable Recommendation
```

**Ini yang harus kamu pertahankan sebagai inti penelitian.**

---

# 20. Teknologi yang saya sarankan

Karena kamu sudah familiar dengan Python:

| Bagian              | Teknologi             |
| ------------------- | --------------------- |
| Programming         | Python                |
| Data processing     | Pandas                |
| ML                  | Scikit-learn          |
| Similarity          | Cosine Similarity     |
| Model               | KNN / Hybrid          |
| Visualization       | Matplotlib            |
| Database            | PostgreSQL            |
| Interface           | Streamlit             |
| API jika diperlukan | FastAPI               |
| Deployment          | Streamlit Cloud / VPS |

Tidak perlu menggunakan TensorFlow atau neural network.

Untuk penelitian ini, **model sederhana yang dapat dijelaskan justru lebih cocok**.

---

# 21. Urutan pengerjaan yang paling aman

Kalau kamu benar-benar akan menjadikan ini tugas akhir, saya sarankan **jangan mulai coding dulu**.

Urutannya:

```text
MINGGU 1
↓
Cari 15–25 paper
↓
MINGGU 2
↓
Mapping penelitian terdahulu
↓
MINGGU 3
↓
Tentukan research gap + novelty
↓
MINGGU 4
↓
Tentukan fitur
↓
MINGGU 5–6
↓
Bangun dataset
↓
MINGGU 7
↓
Preprocessing
↓
MINGGU 8
↓
Baseline
↓
MINGGU 9–10
↓
Hybrid recommendation
↓
MINGGU 11
↓
Evaluation
↓
MINGGU 12
↓
Streamlit application
↓
MINGGU 13
↓
User testing
↓
MINGGU 14
↓
Analisis + dokumentasi
```

### Hal paling penting

Menurut saya, **jangan mengunci metode ML sebelum dataset dan penelitian terdahulu dianalisis**. Justru kita perlu melihat dulu karakteristik dataset yang realistis, bagaimana penelitian 2024–2026 melakukan technology recommendation, dan apa gap yang benar-benar masih kosong.

Kalau kita ingin menjadikan ini topik tugas akhir yang **benar-benar kuat dan tidak mudah dianggap sekadar CRUD + AI**, langkah berikutnya sebaiknya adalah membuat **matriks 15–20 penelitian terdahulu → metode → dataset → objek rekomendasi → variabel → hasil → kekurangan → research gap → novelty penelitianmu**. Dari sana baru kita kunci judul, dataset, algoritma, dan arsitektur final.
