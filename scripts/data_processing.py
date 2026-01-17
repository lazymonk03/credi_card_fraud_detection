# ============================================
# Phase 3: Data Processing
# Project: Credit Card Fraud Detection
# ============================================

import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

# ---------- DB CONNECTION ----------
DB_USER = "lazymonk"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "credit_fraud_db"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ---------- LOAD DATA ----------
query = "SELECT * FROM credit_card_transactions;"
df = pd.read_sql(query, engine)

print("Data Loaded:", df.shape)

# ---------- FEATURE / TARGET ----------
X = df.drop("class", axis=1)
y = df["class"]

# ---------- TRAIN TEST SPLIT ----------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ---------- SCALING ----------
scaler = StandardScaler()
X_train[["time", "amount"]] = scaler.fit_transform(
    X_train[["time", "amount"]]
)
X_test[["time", "amount"]] = scaler.transform(
    X_test[["time", "amount"]]
)

# ---------- SAVE OUTPUT ----------
os.makedirs("../data/processed", exist_ok=True)

X_train.to_csv("../data/processed/X_train.csv", index=False)
X_test.to_csv("../data/processed/X_test.csv", index=False)
y_train.to_csv("../data/processed/y_train.csv", index=False)
y_test.to_csv("../data/processed/y_test.csv", index=False)

print("Processed data saved successfully.")

