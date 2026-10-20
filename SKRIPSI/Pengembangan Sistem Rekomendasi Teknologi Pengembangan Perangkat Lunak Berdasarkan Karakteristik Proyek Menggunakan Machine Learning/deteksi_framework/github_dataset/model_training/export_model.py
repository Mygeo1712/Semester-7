import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def export_model():
    # File path dataset
    train_file = '../pre-processing/dataset_train.csv'
    
    if not os.path.exists(train_file):
        print(f"Error: Dataset {train_file} tidak ditemukan.")
        return
        
    print("1. Memuat dataset training...")
    df_train = pd.read_csv(train_file)
    
    # Memisahkan fitur (X) dan target (y)
    X_train = df_train.drop(columns=['Y_framework', 'repository'])
    y_train = df_train['Y_framework']
    
    print("2. Melatih model Random Forest...")
    # Menggunakan parameter terbaik yang telah terbukti menghasilkan akurasi 87.22%
    rf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    rf.fit(X_train, y_train)
    
    print("3. Mengekspor (menyimpan) model ke dalam file...")
    # Menyimpan model
    model_filename = 'rf_model.joblib'
    joblib.dump(rf, model_filename)
    
    # Menyimpan nama-nama fitur (berguna saat validasi input pengguna di web app)
    features_filename = 'model_features.joblib'
    joblib.dump(list(X_train.columns), features_filename)
    
    print(f"\n[SUKSES] Model berhasil diterbitkan!")
    print(f"- File Model  : {os.path.abspath(model_filename)}")
    print(f"- File Fitur  : {os.path.abspath(features_filename)}")
    print("\nFile-file ini siap diintegrasikan ke dalam backend Flask Anda.")

if __name__ == '__main__':
    export_model()
