"""
Export Random Forest model to JSON for browser-based inference.
Run this script once to generate rf_model.json which is used by index.html.
"""
import joblib
import json
import numpy as np
import os

def export_rf_to_json():
    model_path = '../github_dataset/model_training/rf_model.joblib'
    features_path = '../github_dataset/model_training/model_features.joblib'
    output_path = 'rf_model.json'

    print("Loading model...")
    rf = joblib.load(model_path)
    features = joblib.load(features_path)

    print(f"Model has {rf.n_estimators} trees")
    print(f"Classes: {rf.classes_.tolist()}")
    print(f"Features: {features}")

    def export_tree(tree):
        t = tree.tree_
        nodes = []
        for i in range(t.node_count):
            if t.children_left[i] == -1:  # leaf
                # Get class probabilities
                value = t.value[i][0]
                total = sum(value)
                proba = [v / total for v in value] if total > 0 else [0] * len(value)
                nodes.append({
                    'is_leaf': True,
                    'proba': proba
                })
            else:
                nodes.append({
                    'is_leaf': False,
                    'feature': int(t.feature[i]),
                    'threshold': float(t.threshold[i]),
                    'left': int(t.children_left[i]),
                    'right': int(t.children_right[i])
                })
        return nodes

    print("Exporting trees to JSON...")
    trees = []
    for i, estimator in enumerate(rf.estimators_):
        if i % 10 == 0:
            print(f"  Processing tree {i+1}/{rf.n_estimators}...")
        trees.append(export_tree(estimator))

    model_json = {
        'n_classes': int(rf.n_classes_),
        'classes': rf.classes_.tolist(),
        'features': features,
        'n_features': len(features),
        'n_estimators': rf.n_estimators,
        'trees': trees
    }

    print(f"Writing to {output_path}...")
    with open(output_path, 'w') as f:
        json.dump(model_json, f, separators=(',', ':'))

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\n[SUCCESS] Model exported to {output_path} ({size_mb:.2f} MB)")
    print("Now open index.html in your browser!")

if __name__ == '__main__':
    export_rf_to_json()
