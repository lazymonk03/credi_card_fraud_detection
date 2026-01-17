# ============================================
# Phase 4: Exploratory Data Analysis (EDA)
# Project: Credit Card Fraud Detection
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ---------- PATHS ----------
DATA_PATH = "../data/processed/"
REPORT_PATH = "../reports/eda_plots/"
os.makedirs(REPORT_PATH, exist_ok=True)

# ---------- LOAD DATA ----------
X_train = pd.read_csv(DATA_PATH + "X_train.csv")
y_train = pd.read_csv(DATA_PATH + "y_train.csv")

df = X_train.copy()
df["class"] = y_train

print("EDA Data Shape:", df.shape)

# ---------- 1. FRAUD DISTRIBUTION ----------
fraud_counts = df["class"].value_counts()

plt.figure()
fraud_counts.plot(kind="bar")
plt.title("Fraud vs Non-Fraud Transactions")
plt.xlabel("Class (0 = Legit, 1 = Fraud)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(REPORT_PATH + "fraud_distribution.png")
plt.close()

# ---------- 2. AMOUNT DISTRIBUTION ----------
plt.figure()
sns.histplot(
    df[df["class"] == 0]["amount"],
    bins=50,
    kde=True,
    label="Non-Fraud",
    stat="density"
)
sns.histplot(
    df[df["class"] == 1]["amount"],
    bins=50,
    kde=True,
    label="Fraud",
    stat="density"
)
plt.legend()
plt.title("Transaction Amount Distribution")
plt.xlabel("Amount (Scaled)")
plt.ylabel("Density")
plt.tight_layout()
plt.savefig(REPORT_PATH + "amount_distribution.png")
plt.close()

# ---------- 3. TIME VS FRAUD ----------
plt.figure()
sns.histplot(
    df[df["class"] == 1]["time"],
    bins=50,
    kde=True,
    color="red"
)
plt.title("Fraud Transactions Over Time")
plt.xlabel("Time")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(REPORT_PATH + "fraud_time_distribution.png")
plt.close()

# ---------- 4. CORRELATION WITH FRAUD ----------
corr = df.corr()["class"].sort_values(ascending=False)

corr_df = corr.reset_index()
corr_df.columns = ["Feature", "Correlation"]

corr_df.to_csv(REPORT_PATH + "feature_fraud_correlation.csv", index=False)

print("EDA completed. Plots saved.")

