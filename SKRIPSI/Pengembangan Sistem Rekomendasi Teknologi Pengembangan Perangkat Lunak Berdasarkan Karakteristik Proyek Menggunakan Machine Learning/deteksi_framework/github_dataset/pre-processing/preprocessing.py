import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os

def preprocess_and_split():
    # Define paths
    input_file = '../dataset_clean_2.csv'
    output_dir = '.'
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return
        
    print(f"Loading dataset from {input_file}...")
    df = pd.read_csv(input_file)
    
    print(f"Original dataset shape: {df.shape}")
    
    # Target Mapping
    framework_mapping = {
        'Django': 1,
        'FastAPI': 2,
        'Ruby on Rails': 3,
        'Next.js': 4,
        'Flask': 5,
        'Spring Boot': 6,
        'Laravel': 7,
        'Symfony': 8,
        'Express.js': 9
    }
    
    # Feature X1: application_type
    app_type_mapping = {
        'Web Application': 1,
        'API': 2,
        'CMS': 3,
        'Dashboard': 4,
        'E-commerce': 5,
        'CLI': 6,
        'Unknown': 0 # Assign 0 or could impute
    }
    
    # Feature X2: primary_language
    lang_mapping = {
        'Python': 1,
        'PHP': 2,
        'Java': 3,
        'JavaScript': 4,
        'TypeScript': 5,
        'Ruby': 6,
        'Unknown': 0
    }
    
    # Feature X3: database
    db_mapping = {
        'PostgreSQL': 1,
        'MySQL': 2,
        'MongoDB': 3,
        'SQLite': 4,
        'Redis': 5,
        'Relational (ORM)': 6,
        'Unknown': 0
    }
    
    df_processed = pd.DataFrame()
    
    # Apply Mappings
    df_processed['X1_application_type'] = df['application_type'].map(app_type_mapping).fillna(0).astype(int)
    df_processed['X2_primary_language'] = df['primary_language'].map(lang_mapping).fillna(0).astype(int)
    df_processed['X3_database'] = df['database'].map(db_mapping).fillna(0).astype(int)
    
    # X4, X5, X6, X7 are already binary / numeric
    df_processed['X4_has_docker'] = df['has_docker'].astype(int)
    df_processed['X5_has_ci_cd'] = df['has_ci_cd'].astype(int)
    df_processed['X6_has_tests'] = df['has_tests'].astype(int)
    df_processed['X7_monorepo'] = df['monorepo'].astype(int)
    
    # X8: contributors
    # 1 orang (1), 2-3 orang (2), 4-10 orang (3), Lebih dari 10 orang (4)
    def map_contributors(c):
        if pd.isna(c) or c <= 1: return 1
        elif 2 <= c <= 3: return 2
        elif 4 <= c <= 10: return 3
        else: return 4
    df_processed['X8_contributors'] = df['contributors'].apply(map_contributors)
    
    # X9: pengguna (stars + forks + dependency_count proxy)
    # Kurang dari 100 (1), 100-1.000 (2), 1.001-10.000 (3), 10.001-100.000 (4), Lebih dari 100.000 (5)
    def map_users(row):
        total = row.get('stars', 0) + row.get('forks', 0)
        if total < 100: return 1
        elif 100 <= total <= 1000: return 2
        elif 1001 <= total <= 10000: return 3
        elif 10001 <= total <= 100000: return 4
        else: return 5
    df_processed['X9_pengguna'] = df.apply(map_users, axis=1)
    
    # X10: active weeks
    # Kurang dari 3 bulan (1), 3-6 bulan (2), 6-12 bulan (3), Lebih dari 1 tahun (4)
    # Approx: 3 months ~ 12 weeks, 6 months ~ 24 weeks, 12 months ~ 48 weeks
    def map_active_weeks(w):
        if pd.isna(w) or w < 12: return 1
        elif 12 <= w < 24: return 2
        elif 24 <= w <= 48: return 3
        else: return 4
    df_processed['X10_active_weeks'] = df['active_weeks_last_52_weeks'].apply(map_active_weeks)
    
    # Target
    df_processed['Y_framework'] = df['framework'].map(framework_mapping)
    
    # Filter out rows with unmapped frameworks if any
    df_processed = df_processed.dropna(subset=['Y_framework'])
    df_processed['Y_framework'] = df_processed['Y_framework'].astype(int)
    
    # Include original repository name for traceability (optional, but good for validation)
    df_processed['repository'] = df['repository']
    
    # Feature columns
    features = [f"X{i}_{name}" for i, name in zip(range(1, 11), 
               ['application_type', 'primary_language', 'database', 'has_docker', 'has_ci_cd', 
                'has_tests', 'monorepo', 'contributors', 'pengguna', 'active_weeks'])]
    
    X = df_processed[features]
    y = df_processed['Y_framework']
    
    print("\nClass distribution before split:")
    print(y.value_counts().sort_index())
    
    # 80:20 Split with Stratified Sampling
    print("\nSplitting data into 80% Training and 20% Testing with Stratified Sampling...")
    X_train, X_test, y_train, y_test, repo_train, repo_test = train_test_split(
        X, y, df_processed['repository'], test_size=0.20, random_state=42, stratify=y
    )
    
    # Combine back for saving
    train_data = X_train.copy()
    train_data['Y_framework'] = y_train
    train_data['repository'] = repo_train
    
    test_data = X_test.copy()
    test_data['Y_framework'] = y_test
    test_data['repository'] = repo_test
    
    print(f"\nTraining set shape: {train_data.shape}")
    print(f"Testing set shape: {test_data.shape}")
    
    print("\nClass distribution in Training set:")
    print(y_train.value_counts().sort_index() / len(y_train))
    
    print("\nClass distribution in Testing set:")
    print(y_test.value_counts().sort_index() / len(y_test))
    
    # Save to CSV
    processed_file = os.path.join(output_dir, 'dataset_preprocessed.csv')
    train_file = os.path.join(output_dir, 'dataset_train.csv')
    test_file = os.path.join(output_dir, 'dataset_test.csv')
    
    df_processed.to_csv(processed_file, index=False)
    train_data.to_csv(train_file, index=False)
    test_data.to_csv(test_file, index=False)
    
    print(f"\nSaved preprocessed full dataset to: {processed_file}")
    print(f"Saved training dataset to: {train_file}")
    print(f"Saved testing dataset to: {test_file}")
    print("Preprocessing completed successfully.")

if __name__ == '__main__':
    preprocess_and_split()
