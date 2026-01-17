# ============================================
# Phase 6: Explainable AI with SHAP
# Project: Credit Card Fraud Detection
# ============================================

import os
import joblib
import shap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------- PATHS ----------
DATA_PATH = "../data/processed/"
MODEL_PATH = "../models/"
REPORT_PATH = "../reports/shap/"
os.makedirs(REPORT_PATH, exist_ok=True)

# ---------- LOAD DATA ----------
X_train = pd.read_csv(DATA_PATH + "X_train.csv")
X_test  = pd.read_csv(DATA_PATH + "X_test.csv")
y_test  = pd.read_csv(DATA_PATH + "y_test.csv").values.ravel()

# ---------- LOAD MODEL ----------
model = joblib.load(MODEL_PATH + "fraud_model.pkl")
print("Loaded model:", type(model))

# ---------- CHOOSE EXPLAINER ----------
# TreeExplainer for tree models; KernelExplainer fallback
try:
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    print("Using TreeExplainer")
except Exception as e:
    print("TreeExplainer failed, using KernelExplainer:", e)
    background = shap.sample(X_train, 100)
    explainer = shap.KernelExplainer(model.predict_proba, background)
    shap_values = explainer.shap_values(X_test, nsamples=100)

# ---------- HANDLE BINARY CLASS SHAP ----------
# For many tree models, shap_values is a list [class0, class1]
if isinstance(shap_values, list):
    shap_vals_fraud = shap_values[1]
else:
    shap_vals_fraud = shap_values

# ---------- 1. GLOBAL SUMMARY PLOT ----------
plt.figure()
shap.summary_plot(
    shap_vals_fraud,
    X_test,
    show=False
)
plt.tight_layout()
plt.savefig(REPORT_PATH + "shap_summary.png", dpi=200)
plt.close()

# ---------- 2. TOP FEATURES (CSV) ----------
mean_abs_shap = np.abs(shap_vals_fraud).mean(axis=0)
feature_importance = pd.DataFrame({
    "feature": X_test.columns,
    "mean_abs_shap": mean_abs_shap
}).sort_values(by="mean_abs_shap", ascending=False)

feature_importance.to_csv(
    REPORT_PATH + "shap_feature_importance.csv",
    index=False
)

# ---------- 3. LOCAL EXPLANATION (ONE TRANSACTION) ----------
# Pick a high-risk transaction (highest predicted prob)
try:
    probs = model.predict_proba(X_test)[:, 1]
    idx = np.argmax(probs)
except Exception:
    idx = 0

plt.figure()
shap.force_plot(
    explainer.expected_value[1] if isinstance(explainer.expected_value, (list, np.ndarray)) else explainer.expected_value,
    shap_vals_fraud[idx],
    X_test.iloc[idx],
    matplotlib=True,
    show=False
)
plt.tight_layout()
plt.savefig(REPORT_PATH + "shap_local_example.png", dpi=200)
plt.close()

print("SHAP analysis complete. Files saved to reports/shap/")

