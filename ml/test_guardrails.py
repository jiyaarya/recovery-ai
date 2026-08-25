from guardrails import check_guardrails


def run_test(name, **kwargs):

    result = check_guardrails(**kwargs)

    print(f"\n========== {name} ==========")

    print(
        f"Allowed       : {result['allowed']}"
    )

    print(
        f"Final Action  : {result['final_action']}"
    )

    print(
        f"Risk Level    : {result['risk_level']}"
    )

    print(
        f"Reason        : {result['reason']}"
    )


# Test 1: Safe retry
run_test(
    "SAFE RETRY",
    strategy="RETRY_PAYMENT",
    recovery_probability=0.85,
    retry_count=0,
    recovered=0,
    amount=20000,
    customer_lifetime_value=50000
)


# Test 2: Too many retries
run_test(
    "TOO MANY RETRIES",
    strategy="RETRY_PAYMENT",
    recovery_probability=0.90,
    retry_count=4,
    recovered=0,
    amount=20000,
    customer_lifetime_value=50000
)


# Test 3: Already recovered
run_test(
    "ALREADY RECOVERED",
    strategy="RETRY_PAYMENT",
    recovery_probability=0.90,
    retry_count=0,
    recovered=1,
    amount=20000,
    customer_lifetime_value=50000
)


# Test 4: Low probability
run_test(
    "LOW PROBABILITY",
    strategy="RETRY_PAYMENT",
    recovery_probability=0.20,
    retry_count=0,
    recovered=0,
    amount=20000,
    customer_lifetime_value=50000
)


# Test 5: Payment link
run_test(
    "PAYMENT LINK",
    strategy="SEND_PAYMENT_LINK",
    recovery_probability=0.75,
    retry_count=0,
    recovered=0,
    amount=15000,
    customer_lifetime_value=70000
)