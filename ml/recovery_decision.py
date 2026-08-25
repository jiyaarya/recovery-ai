import pandas as pd
import joblib

from guardrails import check_guardrails


MODEL_PATH = "ml/recovery_model.pkl"
DATA_PATH = "data/revenue_recovery_dataset.csv"
OUTPUT_PATH = "data/final_recovery_decisions.csv"


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

    if retry_count >= 4:
        return (
            "ESCALATE",
            "Maximum retry threshold reached"
        )

    if recovery_probability < 0.30:
        return (
            "NO_ACTION",
            "Low probability of successful recovery"
        )

    if checkout_abandoned == 1:
        return (
            "SEND_PAYMENT_LINK",
            "Customer abandoned checkout"
        )

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

    if str(subscription_status).lower() == "active":

        if recovery_probability >= 0.60:
            return (
                "SEND_PAYMENT_LINK",
                "Active subscription with reasonable recovery probability"
            )

    if recovery_probability >= 0.75:
        return (
            "RETRY_PAYMENT",
            "High recovery probability"
        )

    if recovery_probability >= 0.50:
        return (
            "RETRY_LATER",
            "Moderate recovery probability"
        )

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

    print("Generating ML predictions...")

    # Generate probabilities for all transactions at once
    X = data[FEATURES]

    data["recovery_probability"] = (
        model.predict_proba(X)[:, 1]
    )

    print("Calculating expected recovery...")

    data["expected_recovery"] = (
        data["amount"] *
        data["recovery_probability"]
    )

    print("Calculating priorities...")

    data["priority"] = data[
        "expected_recovery"
    ].apply(
        calculate_priority
    )

    print("Generating strategy recommendations...")

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

    data["recommended_strategy"] = strategies.apply(
        lambda result: result[0]
    )

    data["strategy_reason"] = strategies.apply(
        lambda result: result[1]
    )

    print("Applying safety guardrails...")

    guardrail_results = data.apply(
        lambda row: check_guardrails(
            strategy=row["recommended_strategy"],
            recovery_probability=row["recovery_probability"],
            retry_count=row["retry_count"],
            recovered=row["recovered"],
            amount=row["amount"],
            customer_lifetime_value=row[
                "customer_lifetime_value"
            ]
        ),
        axis=1
    )

    data["action_allowed"] = guardrail_results.apply(
        lambda result: result["allowed"]
    )

    data["final_action"] = guardrail_results.apply(
        lambda result: result["final_action"]
    )

    data["risk_level"] = guardrail_results.apply(
        lambda result: result["risk_level"]
    )

    data["guardrail_reason"] = guardrail_results.apply(
        lambda result: result["reason"]
    )

    # Rank by expected recovery
    data = data.sort_values(
        by="expected_recovery",
        ascending=False
    )

    output_columns = [
        "transaction_id",
        "amount",
        "recovery_probability",
        "expected_recovery",
        "priority",
        "recommended_strategy",
        "strategy_reason",
        "action_allowed",
        "final_action",
        "risk_level",
        "guardrail_reason"
    ]

    results = data[output_columns]

    results.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        "\n========== FINAL RECOVERY DECISIONS =========="
    )

    print(
        f"Transactions analyzed: {len(results)}"
    )

    print("\nRecommended Strategy Distribution:")

    print(
        results[
            "recommended_strategy"
        ].value_counts()
    )

    print("\nFinal Action Distribution:")

    print(
        results[
            "final_action"
        ].value_counts()
    )

    print("\nRisk Distribution:")

    print(
        results[
            "risk_level"
        ].value_counts()
    )

    print("\nBlocked Actions:")

    blocked = (
        results["action_allowed"] == False
    ).sum()

    print(blocked)

    print(
        "\n========== TOP 10 FINAL DECISIONS =========="
    )

    print(
        results.head(10).to_string(
            index=False
        )
    )

    print(
        f"\nFinal decisions saved to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()