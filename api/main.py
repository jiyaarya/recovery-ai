from fastapi import FastAPI
import pandas as pd
import joblib
import sys
import os

# Allow Python to access files inside the ml folder
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from ml.guardrails import check_guardrails


app = FastAPI(
    title="RecoverAI API",
    description="AI-powered payment recovery intelligence system",
    version="1.0.0"
)


# --------------------------------------------------
# LOAD ML MODEL
# --------------------------------------------------

MODEL_PATH = "ml/recovery_model.pkl"

model = joblib.load(MODEL_PATH)


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


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "RecoverAI API is running",
        "status": "healthy"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model_loaded": True
    }


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

@app.post("/predict")
def predict(transaction: dict):

    # Convert incoming transaction to DataFrame
    data = pd.DataFrame(
        [transaction]
    )

    # Make sure all required features exist
    missing_features = [
        feature
        for feature in FEATURES
        if feature not in data.columns
    ]

    if missing_features:

        return {
            "error": "Missing required features",
            "missing_features": missing_features
        }

    # Keep only model features
    X = data[FEATURES]

    # ML prediction
    recovery_probability = float(
        model.predict_proba(X)[0][1]
    )

    amount = float(
        transaction["amount"]
    )

    # Expected recovery
    expected_recovery = (
        amount *
        recovery_probability
    )

    # Priority
    if expected_recovery >= 10000:

        priority = "HIGH"

    elif expected_recovery >= 5000:

        priority = "MEDIUM"

    else:

        priority = "LOW"

    # --------------------------------------------------
    # STRATEGY
    # --------------------------------------------------

    recovery_probability_value = (
        recovery_probability
    )

    retry_count = int(
        transaction["retry_count"]
    )

    failure_reason = str(
        transaction["failure_reason"]
    ).lower().strip()

    checkout_abandoned = int(
        transaction["checkout_abandoned"]
    )

    subscription_status = str(
        transaction["subscription_status"]
    )

    # Maximum retries
    if retry_count >= 4:

        strategy = "ESCALATE"

        strategy_reason = (
            "Maximum retry threshold reached"
        )

    elif recovery_probability_value < 0.30:

        strategy = "NO_ACTION"

        strategy_reason = (
            "Low probability of successful recovery"
        )

    elif checkout_abandoned == 1:

        strategy = "SEND_PAYMENT_LINK"

        strategy_reason = (
            "Customer abandoned checkout"
        )

    elif failure_reason in [
        "network_error",
        "temporary_failure",
        "timeout",
        "technical_error"
    ]:

        if recovery_probability_value >= 0.70:

            strategy = "RETRY_PAYMENT"

            strategy_reason = (
                "High recovery probability with retryable failure"
            )

        else:

            strategy = "RETRY_LATER"

            strategy_reason = (
                "Retryable failure with moderate recovery probability"
            )

    elif (
        subscription_status.lower() == "active"
        and recovery_probability_value >= 0.60
    ):

        strategy = "SEND_PAYMENT_LINK"

        strategy_reason = (
            "Active subscription with reasonable recovery probability"
        )

    elif recovery_probability_value >= 0.75:

        strategy = "RETRY_PAYMENT"

        strategy_reason = (
            "High recovery probability"
        )

    elif recovery_probability_value >= 0.50:

        strategy = "RETRY_LATER"

        strategy_reason = (
            "Moderate recovery probability"
        )

    else:

        strategy = "ESCALATE"

        strategy_reason = (
            "Transaction requires manual review"
        )

    # --------------------------------------------------
    # GUARDRAILS
    # --------------------------------------------------

    guardrail = check_guardrails(
        strategy=strategy,
        recovery_probability=recovery_probability,
        retry_count=retry_count,
        recovered=int(
            transaction.get(
                "recovered",
                0
            )
        ),
        amount=amount,
        customer_lifetime_value=float(
            transaction[
                "customer_lifetime_value"
            ]
        )
    )

    # --------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------

    return {

        "transaction_id": transaction.get(
            "transaction_id",
            "UNKNOWN"
        ),

        "amount": amount,

        "recovery_probability": round(
            recovery_probability * 100,
            2
        ),

        "expected_recovery": round(
            expected_recovery,
            2
        ),

        "priority": priority,

        "recommended_strategy": strategy,

        "strategy_reason": strategy_reason,

        "action_allowed": guardrail[
            "allowed"
        ],

        "final_action": guardrail[
            "final_action"
        ],

        "risk_level": guardrail[
            "risk_level"
        ],

        "guardrail_reason": guardrail[
            "reason"
        ]
    }