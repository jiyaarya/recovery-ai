import pandas as pd
import numpy as np
import random

# Make results reproducible
np.random.seed(42)
random.seed(42)

# Number of transactions
N = 10000

# Possible values
payment_methods = ["UPI", "Card", "NetBanking", "Wallet"]

failure_reasons = [
    "insufficient_funds",
    "card_expired",
    "bank_declined",
    "network_error",
    "authentication_failed",
    "customer_abandoned"
]

subscription_statuses = [
    "active",
    "inactive",
    "not_applicable"
]

data = []

for i in range(N):

    # Customer information
    customer_id = f"CUST_{random.randint(1000, 3000)}"

    amount = round(np.random.uniform(100, 50000), 2)

    payment_method = random.choice(payment_methods)

    failure_reason = random.choice(failure_reasons)

    customer_lifetime_value = round(
        np.random.uniform(1000, 200000), 2
    )

    successful_payments = random.randint(0, 30)

    failed_payments = random.randint(0, 8)

    previous_recovery_rate = round(
        np.random.uniform(0, 1), 2
    )

    hour_of_day = random.randint(0, 23)

    days_since_last_payment = random.randint(0, 90)

    subscription_status = random.choice(
        subscription_statuses
    )

    checkout_abandoned = random.choice([0, 1])

    retry_count = random.randint(0, 4)

    # ------------------------------------------------
    # Generate a realistic recovery probability
    # ------------------------------------------------

    probability = 0.45

    # Strong customer history
    if successful_payments >= 10:
        probability += 0.15

    # Good historical recovery
    if previous_recovery_rate >= 0.7:
        probability += 0.15

    # Too many failures reduce probability
    if failed_payments >= 5:
        probability -= 0.15

    # Too many retries reduce probability
    if retry_count >= 3:
        probability -= 0.20

    # Failure reason influence
    if failure_reason == "network_error":
        probability += 0.15

    elif failure_reason == "insufficient_funds":
        probability += 0.05

    elif failure_reason == "card_expired":
        probability -= 0.05

    elif failure_reason == "authentication_failed":
        probability -= 0.10

    elif failure_reason == "customer_abandoned":
        probability -= 0.05

    # Active subscriptions are easier to recover
    if subscription_status == "active":
        probability += 0.10

    # Clamp probability between 0 and 1
    probability = max(0.05, min(0.95, probability))

    # Add randomness
    recovered = np.random.binomial(1, probability)

    data.append([
        f"TXN_{i+1}",
        customer_id,
        amount,
        payment_method,
        failure_reason,
        customer_lifetime_value,
        successful_payments,
        failed_payments,
        previous_recovery_rate,
        hour_of_day,
        days_since_last_payment,
        subscription_status,
        checkout_abandoned,
        retry_count,
        recovered
    ])


# Create DataFrame
columns = [
    "transaction_id",
    "customer_id",
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
    "retry_count",
    "recovered"
]

df = pd.DataFrame(data, columns=columns)

# Save dataset
output_file = "data/revenue_recovery_dataset.csv"

df.to_csv(output_file, index=False)

print("Dataset created successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to: {output_file}")

print("\nFirst 5 rows:")
print(df.head())

print("\nRecovery distribution:")
print(df["recovered"].value_counts())