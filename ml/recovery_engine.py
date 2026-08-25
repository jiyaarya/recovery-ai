import pandas as pd
import joblib


MODEL_PATH = "ml/recovery_model.pkl"
DATA_PATH = "data/revenue_recovery_dataset.csv"


def calculate_expected_recovery(amount, recovery_probability):
    """
    Calculate the expected amount of revenue that can potentially
    be recovered.
    """
    return amount * recovery_probability


def calculate_priority(expected_recovery):
    """
    Assign priority based on expected recoverable revenue.
    """

    if expected_recovery >= 10000:
        return "HIGH"

    elif expected_recovery >= 5000:
        return "MEDIUM"

    else:
        return "LOW"


def prepare_transaction(transaction):
    """
    Prepare a transaction in the same format used during model training.
    """

    features = [
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

    return transaction[features]


def analyze_transaction(transaction):
    """
    Use the trained ML model to calculate recovery intelligence.
    """

    model = joblib.load(MODEL_PATH)

    transaction_features = prepare_transaction(transaction)

    # Convert to DataFrame because the model expects tabular data
    transaction_features = pd.DataFrame(
        [transaction_features]
    )

    # Get probability of class 1 = recovered
    recovery_probability = model.predict_proba(
        transaction_features
    )[0][1]

    amount = transaction["amount"]

    expected_recovery = calculate_expected_recovery(
        amount,
        recovery_probability
    )

    priority = calculate_priority(
        expected_recovery
    )

    return {
        "amount": amount,
        "recovery_probability": recovery_probability,
        "expected_recovery": expected_recovery,
        "priority": priority
    }


if __name__ == "__main__":

    # Load dataset
    data = pd.read_csv(DATA_PATH)

    # Select one transaction for testing
    transaction = data.iloc[0]

    result = analyze_transaction(transaction)

    print("\n========== REAL ML RECOVERY INTELLIGENCE ==========")

    print(
        f"Transaction Amount     : "
        f"₹{result['amount']:,.2f}"
    )

    print(
        f"Recovery Probability   : "
        f"{result['recovery_probability'] * 100:.2f}%"
    )

    print(
        f"Expected Recovery      : "
        f"₹{result['expected_recovery']:,.2f}"
    )

    print(
        f"Priority               : "
        f"{result['priority']}"
    )