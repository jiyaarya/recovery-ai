import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("data/revenue_recovery_dataset.csv")

print("Dataset loaded successfully.")
print(f"Total rows: {len(df)}")


# ============================================================
# 2. REMOVE IDENTIFIERS
# ============================================================

df = df.drop(columns=[
    "transaction_id",
    "customer_id"
])


# ============================================================
# 3. SEPARATE FEATURES AND TARGET
# ============================================================

X = df.drop(columns=["recovered"])
y = df["recovered"]


# ============================================================
# 4. DEFINE COLUMN TYPES
# ============================================================

categorical_features = [
    "payment_method",
    "failure_reason",
    "subscription_status"
]

numerical_features = [
    "amount",
    "customer_lifetime_value",
    "successful_payments",
    "failed_payments",
    "previous_recovery_rate",
    "hour_of_day",
    "days_since_last_payment",
    "checkout_abandoned",
    "retry_count"
]


# ============================================================
# 5. PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)


# ============================================================
# 6. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nData split:")
print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")


# ============================================================
# 7. CREATE ML MODEL
# ============================================================

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    random_state=42,
    class_weight="balanced"
)


# ============================================================
# 8. CREATE COMPLETE PIPELINE
# ============================================================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# ============================================================
# 9. TRAIN
# ============================================================

print("\nTraining model...")

pipeline.fit(X_train, y_train)

print("Training completed!")


# ============================================================
# 10. MAKE PREDICTIONS
# ============================================================

y_pred = pipeline.predict(X_test)

y_probability = pipeline.predict_proba(X_test)[:, 1]


# ============================================================
# 11. EVALUATE MODEL
# ============================================================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(y_test, y_pred)

recall = recall_score(y_test, y_pred)

f1 = f1_score(y_test, y_pred)

roc_auc = roc_auc_score(y_test, y_probability)


print("\n================ MODEL RESULTS ================")

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC-AUC   : {roc_auc:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# ============================================================
# 12. SAVE MODEL
# ============================================================

model_file = "ml/recovery_model.pkl"

joblib.dump(pipeline, model_file)

print("\nModel saved successfully!")
print(f"Model location: {model_file}")