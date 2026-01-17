# ============================================
# Phase 7: Power BI Dataset Preparation
# Project: Credit Card Fraud Detection
# Author: Amar Jeet
#
# Purpose:
# - Prepare a Power BI Web–ready dataset
# - Pre-compute KPIs, risk buckets, and customer dimensions
# - Avoid DAX dependency (Power BI Web–only workflow)
# ============================================

import pandas as pd
import numpy as np
import joblib
import os

# ---------- PATHS ----------
DATA_PATH = "../data/processed/"
MODEL_PATH = "../models/"
OUTPUT_PATH = "../data/powerbi/"

os.makedirs(OUTPUT_PATH, exist_ok=True)

# ---------- LOAD DATA ----------
X_test = pd.read_csv(DATA_PATH + "X_test.csv")
y_test = pd.read_csv(DATA_PATH + "y_test.csv").values.ravel()

# ---------- LOAD MODEL ----------
model = joblib.load(MODEL_PATH + "fraud_model.pkl")

# ---------- PREDICT FRAUD PROBABILITY ----------
fraud_probability = model.predict_proba(X_test)[:, 1]

# ---------- CREATE BASE DATASET ----------
powerbi_df = X_test.copy()
powerbi_df["actual_class"] = y_test
powerbi_df["fraud_probability"] = fraud_probability

# Fraud flag based on business threshold
powerbi_df["fraud_flag"] = (powerbi_df["fraud_probability"] > 0.85).astype(int)

# Fraud label
powerbi_df["fraud_label"] = powerbi_df["fraud_flag"].map({
    0: "Legitimate",
    1: "Fraud"
})

# ---------- RISK BUCKETS (FOR CONDITIONAL FORMATTING) ----------
powerbi_df["risk_bucket"] = pd.cut(
    powerbi_df["fraud_probability"],
    bins=[0.0, 0.30, 0.60, 0.85, 1.00],
    labels=["Low", "Medium", "High", "Critical"],
    include_lowest=True
)

# ---------- TIME BUCKETS (FOR DRILL-DOWN) ----------
powerbi_df["time_bucket"] = pd.cut(
    powerbi_df["time"],
    bins=10,
    labels=[f"T{i}" for i in range(1, 11)]
)

# ---------- SIMULATED CUSTOMER DIMENSION ----------
np.random.seed(42)
powerbi_df["customer_id"] = np.random.randint(
    10000, 20000, size=len(powerbi_df)
)

# ---------- SIMULATED MERCHANT CATEGORY ----------
powerbi_df["merchant_category"] = np.random.choice(
    ["E-commerce", "POS", "ATM", "Travel", "Food"],
    size=len(powerbi_df)
)

# ---------- FINAL COLUMN ORDER (OPTIONAL) ----------
final_columns = [
    "customer_id",
    "merchant_category",
    "time",
    "time_bucket",
    "amount",
    "fraud_probability",
    "risk_bucket",
    "fraud_flag",
    "fraud_label",
    "actual_class"
]

# Add PCA features after main columns
pca_columns = [col for col in powerbi_df.columns if col.startswith("v")]
final_columns.extend(pca_columns)

powerbi_df = powerbi_df[final_columns]

# ---------- SAVE POWER BI DATASET ----------
output_file = OUTPUT_PATH + "fraud_powerbi_dataset.csv"
powerbi_df.to_csv(output_file, index=False)

print("✅ Power BI dataset created successfully")
print(f"📁 Saved at: {output_file}")
print(f"📊 Rows: {len(powerbi_df)} | Columns: {len(powerbi_df.columns)}")

