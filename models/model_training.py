# ============================================
# Phase 5: Machine Learning Model Training
# Project: Credit Card Fraud Detection
# ============================================

import pandas as pd
import numpy as np
import joblib
import os

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    precision_recall_fscore_support
)

# ---------- PATHS ----------
DATA_PATH = "../data/processed/"
MODEL_PATH = "../models/"
os.makedirs(MODEL_PATH, exist_ok=True)

# ---------- LOAD DATA ----------
X_train = pd.read_csv(DATA_PATH + "X_train.csv")
X_test = pd.read_csv(DATA_PATH + "X_test.csv")
y_train = pd.read_csv(DATA_PATH + "y_train.csv").values.ravel()
y_test = pd.read_csv(DATA_PATH + "y_test.csv").values.ravel()

print("Training data:", X_train.shape)
print("Test data:", X_test.shape)

# ---------- HELPER FUNCTION ----------
def evaluate_model(name, model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, y_pred, average="binary"
    )
    roc_auc = roc_auc_score(y_test, y_prob)

    print(f"\n{name} Results")
    print("-" * 40)
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1-score  : {f1:.4f}")
    print(f"ROC-AUC   : {roc_auc:.4f}")

    return {
        "model": name,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc
    }

results = []

# ---------- 1. LOGISTIC REGRESSION (BASELINE) ----------
log_reg = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    n_jobs=-1
)
log_reg.fit(X_train, y_train)

results.append(
    evaluate_model("Logistic Regression", log_reg, X_test, y_test)
)

# ---------- 2. RANDOM FOREST ----------
rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)
rf.fit(X_train, y_train)

results.append(
    evaluate_model("Random Forest", rf, X_test, y_test)
)

# ---------- 3. XGBOOST ----------
try:
    from xgboost import XGBClassifier

    xgb = XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum(),
        eval_metric="logloss",
        random_state=42
    )
    xgb.fit(X_train, y_train)

    results.append(
        evaluate_model("XGBoost", xgb, X_test, y_test)
    )

    best_model = xgb

except ImportError:
    print("XGBoost not installed. Skipping.")
    best_model = rf

# ---------- SAVE RESULTS ----------
results_df = pd.DataFrame(results)
results_df.to_csv(MODEL_PATH + "model_comparison.csv", index=False)

# ---------- SAVE BEST MODEL ----------
joblib.dump(best_model, MODEL_PATH + "fraud_model.pkl")

print("\nModel training complete.")
print("Best model saved to /models/")

