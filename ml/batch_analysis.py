import pandas as pd
import joblib


MODEL_PATH = "ml/recovery_model.pkl"
DATA_PATH = "data/revenue_recovery_dataset.csv"
OUTPUT_PATH = "data/recovery_analysis.csv"


FEATURES = [
    "amount",
    "payment_method",
    "failure_reason",
    "customer_lifetime_value",
    "successful_payments",
    "failed_payments",
    "previous_recovery_rate",
    "hour_of_day",
    "days_since_last_payment",
    "subscription_status",
    "checkout_abandoned",
    "retry_count"
]


def calculate_priority(expected_recovery):
    """
    Assign recovery priority based on expected recoverable revenue.
    """

    if expected_recovery >= 10000:
        return "HIGH"

    elif expected_recovery >= 5000:
        return "MEDIUM"

    else:
        return "LOW"


def analyze_dataset():

    print("Loading dataset...")

    data = pd.read_csv(DATA_PATH)

    print(f"Total transactions: {len(data)}")

    print("Loading trained ML model...")

    model = joblib.load(MODEL_PATH)

    # Prepare features
    X = data[FEATURES]

    print("Generating recovery probabilities...")

    # Probability of class 1 = recovered
    probabilities = model.predict_proba(X)[:, 1]

    # Add predictions to dataset
    data["recovery_probability"] = probabilities

    # Calculate expected recovery
    data["expected_recovery"] = (
        data["amount"] *
        data["recovery_probability"]
    )

    # Assign priority
    data["priority"] = data["expected_recovery"].apply(
        calculate_priority
    )

    # Sort by expected recovery
    data = data.sort_values(
        by="expected_recovery",
        ascending=False
    )

    # Save results
    data.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\n========== BATCH RECOVERY ANALYSIS ==========")

    print(
        f"Total transactions analyzed : {len(data)}"
    )

    print(
        f"Total revenue at risk       : "
        f"₹{data['amount'].sum():,.2f}"
    )

    print(
        f"Expected recoverable revenue: "
        f"₹{data['expected_recovery'].sum():,.2f}"
    )

    print("\nPriority Distribution:")

    print(
        data["priority"].value_counts()
    )

    print("\n========== TOP 10 RECOVERY OPPORTUNITIES ==========")

    top_transactions = data[
        [
            "transaction_id",
            "amount",
            "recovery_probability",
            "expected_recovery",
            "priority"
        ]
    ].head(10)

    print(top_transactions.to_string(index=False))

    print(
        f"\nAnalysis saved to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    analyze_dataset()