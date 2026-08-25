import pandas as pd
import joblib


MODEL_PATH = "ml/recovery_model.pkl"
DATA_PATH = "data/revenue_recovery_dataset.csv"
OUTPUT_PATH = "data/strategy_analysis.csv"


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


def determine_strategy(
    recovery_probability,
    retry_count,
    failure_reason,
    checkout_abandoned,
    subscription_status
):
    """
    Determine the most appropriate recovery strategy.
    """

    # Safety rule: prevent excessive retries
    if retry_count >= 4:
        return (
            "ESCALATE",
            "Maximum retry threshold reached"
        )

    # Very low recovery probability
    if recovery_probability < 0.30:
        return (
            "NO_ACTION",
            "Low probability of successful recovery"
        )

    # Customer abandoned checkout
    if checkout_abandoned == 1:
        return (
            "SEND_PAYMENT_LINK",
            "Customer abandoned checkout"
        )

    # Failures that may be safely retried
    retryable_failures = [
        "network_error",
        "temporary_failure",
        "timeout",
        "technical_error"
    ]

    failure_reason_clean = str(
        failure_reason
    ).lower().strip()

    if failure_reason_clean in retryable_failures:

        if recovery_probability >= 0.70:
            return (
                "RETRY_PAYMENT",
                "High recovery probability with retryable failure"
            )

        else:
            return (
                "RETRY_LATER",
                "Retryable failure with moderate recovery probability"
            )

    # Active subscription recovery
    if str(subscription_status).lower() == "active":

        if recovery_probability >= 0.60:
            return (
                "SEND_PAYMENT_LINK",
                "Active subscription with reasonable recovery probability"
            )

    # High probability fallback
    if recovery_probability >= 0.75:
        return (
            "RETRY_PAYMENT",
            "High recovery probability"
        )

    # Medium probability fallback
    if recovery_probability >= 0.50:
        return (
            "RETRY_LATER",
            "Moderate recovery probability"
        )

    # Remaining cases
    return (
        "ESCALATE",
        "Transaction requires manual review"
    )


def main():

    print("Loading dataset...")

    data = pd.read_csv(DATA_PATH)

    print(
        f"Total transactions: {len(data)}"
    )

    print("Loading trained model...")

    model = joblib.load(MODEL_PATH)

    # --------------------------------------------------
    # STEP 1: Generate predictions for ALL transactions
    # --------------------------------------------------

    print("Generating ML predictions...")

    X = data[FEATURES]

    data["recovery_probability"] = (
        model.predict_proba(X)[:, 1]
    )

    # --------------------------------------------------
    # STEP 2: Calculate expected recovery
    # --------------------------------------------------

    print("Calculating expected recovery...")

    data["expected_recovery"] = (
        data["amount"] *
        data["recovery_probability"]
    )

    # --------------------------------------------------
    # STEP 3: Calculate priority
    # --------------------------------------------------

    print("Calculating priorities...")

    data["priority"] = data[
        "expected_recovery"
    ].apply(
        calculate_priority
    )

    # --------------------------------------------------
    # STEP 4: Determine recovery strategy
    # --------------------------------------------------

    print("Determining recovery strategies...")

    strategies = data.apply(
        lambda row: determine_strategy(
            row["recovery_probability"],
            row["retry_count"],
            row["failure_reason"],
            row["checkout_abandoned"],
            row["subscription_status"]
        ),
        axis=1
    )

    # Extract strategy name
    data["strategy"] = strategies.apply(
        lambda result: result[0]
    )

    # Extract explanation
    data["reason"] = strategies.apply(
        lambda result: result[1]
    )

    # --------------------------------------------------
    # STEP 5: Rank transactions
    # --------------------------------------------------

    data = data.sort_values(
        by="expected_recovery",
        ascending=False
    )

    # --------------------------------------------------
    # STEP 6: Select output columns
    # --------------------------------------------------

    output_columns = [
        "transaction_id",
        "amount",
        "recovery_probability",
        "expected_recovery",
        "priority",
        "strategy",
        "reason"
    ]

    results = data[output_columns]

    # --------------------------------------------------
    # STEP 7: Save analysis
    # --------------------------------------------------

    results.to_csv(
        OUTPUT_PATH,
        index=False
    )

    # --------------------------------------------------
    # STEP 8: Display results
    # --------------------------------------------------

    print(
        "\n========== RECOVERY STRATEGY ANALYSIS =========="
    )

    print(
        f"Total transactions analyzed: "
        f"{len(results)}"
    )

    print("\nStrategy Distribution:")

    print(
        results["strategy"].value_counts()
    )

    print("\nPriority Distribution:")

    print(
        results["priority"].value_counts()
    )

    print(
        "\n========== TOP 10 RECOVERY OPPORTUNITIES =========="
    )

    print(
        results.head(10).to_string(
            index=False
        )
    )

    print(
        f"\nAnalysis saved to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()