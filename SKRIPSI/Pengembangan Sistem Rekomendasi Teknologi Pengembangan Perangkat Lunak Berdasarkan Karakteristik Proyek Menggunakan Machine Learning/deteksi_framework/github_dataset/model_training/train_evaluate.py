import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

def train_and_evaluate():
    # Paths
    train_file = '../pre-processing/dataset_train.csv'
    test_file = '../pre-processing/dataset_test.csv'
    output_dir = '.'
    
    print("Loading data...")
    df_train = pd.read_csv(train_file)
    df_test = pd.read_csv(test_file)
    
    # Separate features and target
    X_train = df_train.drop(columns=['Y_framework', 'repository'])
    y_train = df_train['Y_framework']
    
    X_test = df_test.drop(columns=['Y_framework', 'repository'])
    y_test = df_test['Y_framework']
    
    # Framework mapping for labels
    framework_mapping = {
        1: 'Django',
        2: 'FastAPI',
        3: 'Ruby on Rails',
        4: 'Next.js',
        5: 'Flask',
        6: 'Spring Boot',
        7: 'Laravel',
        8: 'Symfony',
        9: 'Express.js'
    }
    labels = [framework_mapping[i] for i in range(1, 10)]
    
    # Initialize model
    print("Training Random Forest Classifier...")
    # Using random_state for reproducibility
    rf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    rf.fit(X_train, y_train)
    
    # Predictions
    print("Evaluating model...")
    y_pred = rf.predict(X_test)
    
    # Metrics calculation
    accuracy = accuracy_score(y_test, y_pred)
    macro_precision = precision_score(y_test, y_pred, average='macro')
    macro_recall = recall_score(y_test, y_pred, average='macro')
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    
    print("\n" + "="*50)
    print("MODEL EVALUATION METRICS")
    print("="*50)
    print(f"Accuracy        : {accuracy:.4f}")
    print(f"Macro Precision : {macro_precision:.4f}")
    print(f"Macro Recall    : {macro_recall:.4f}")
    print(f"Macro F1-Score  : {macro_f1:.4f}")
    print("="*50)
    
    print("\nCLASSIFICATION REPORT")
    print(classification_report(y_test, y_pred, target_names=labels))
    
    # Plotting 1: Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Framework')
    plt.ylabel('Actual Framework')
    plt.xticks(rotation=45)
    plt.tight_layout()
    cm_path = os.path.join(output_dir, 'confusion_matrix.png')
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"Saved Confusion Matrix plot to {cm_path}")
    
    # Plotting 2: Feature Importance
    importances = rf.feature_importances_
    features = X_train.columns
    
    # Clean feature names for plot
    clean_features = [f.split('_', 1)[1] if '_' in f else f for f in features]
    
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(12, 6))
    plt.title('Feature Importances in Random Forest')
    plt.bar(range(X_train.shape[1]), importances[indices], align='center')
    plt.xticks(range(X_train.shape[1]), [clean_features[i] for i in indices], rotation=45, ha='right')
    plt.xlim([-1, X_train.shape[1]])
    plt.tight_layout()
    feat_imp_path = os.path.join(output_dir, 'feature_importance.png')
    plt.savefig(feat_imp_path, dpi=300)
    plt.close()
    print(f"Saved Feature Importance plot to {feat_imp_path}")
    
    # Plotting 3: Metrics Summary Bar Chart
    metrics_names = ['Accuracy', 'Macro Precision', 'Macro Recall', 'Macro F1-Score']
    metrics_values = [accuracy, macro_precision, macro_recall, macro_f1]
    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(metrics_names, metrics_values, color=['#4C72B0', '#55A868', '#C44E52', '#8172B2'])
    plt.ylim(0, 1.1)
    plt.title('Overall Model Performance Metrics')
    plt.ylabel('Score')
    
    # Add values on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.4f}', va='bottom', ha='center', fontweight='bold')
        
    plt.tight_layout()
    metrics_path = os.path.join(output_dir, 'metrics_summary.png')
    plt.savefig(metrics_path, dpi=300)
    plt.close()
    print(f"Saved Metrics Summary plot to {metrics_path}")
    
    print("\nModel evaluation completed. Graphs have been saved successfully.")

if __name__ == '__main__':
    train_and_evaluate()
