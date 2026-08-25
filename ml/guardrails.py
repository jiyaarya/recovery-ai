def check_guardrails(
    strategy,
    recovery_probability,
    retry_count,
    recovered,
    amount,
    customer_lifetime_value
):
    """
    Safety layer that determines whether a recovery strategy
    should be allowed, modified, or sent for manual review.
    """

    # --------------------------------------------------
    # RULE 1: Already recovered
    # --------------------------------------------------

    if recovered == 1:
        return {
            "allowed": False,
            "final_action": "NO_ACTION",
            "risk_level": "SAFE",
            "reason": "Transaction has already been recovered"
        }

    # --------------------------------------------------
    # RULE 2: Too many retries
    # --------------------------------------------------

    if retry_count >= 4:
        return {
            "allowed": False,
            "final_action": "ESCALATE",
            "risk_level": "HIGH",
            "reason": "Maximum retry threshold reached"
        }

    # --------------------------------------------------
    # RULE 3: Very low recovery probability
    # --------------------------------------------------

    if recovery_probability < 0.30:
        return {
            "allowed": False,
            "final_action": "NO_ACTION",
            "risk_level": "LOW",
            "reason": "Recovery probability is too low"
        }

    # --------------------------------------------------
    # RULE 4: High-value transaction protection
    # --------------------------------------------------

    if amount >= 40000 and recovery_probability < 0.60:
        return {
            "allowed": False,
            "final_action": "ESCALATE",
            "risk_level": "HIGH",
            "reason": "High-value transaction requires additional review"
        }

    # --------------------------------------------------
    # RULE 5: Very high-value customer
    # --------------------------------------------------

    if customer_lifetime_value >= 150000:

        if recovery_probability < 0.50:
            return {
                "allowed": False,
                "final_action": "ESCALATE",
                "risk_level": "MEDIUM",
                "reason": "High-value customer with uncertain recovery"
            }

    # --------------------------------------------------
    # RULE 6: Retry protection
    # --------------------------------------------------

    if strategy == "RETRY_PAYMENT":

        if retry_count >= 2:
            return {
                "allowed": False,
                "final_action": "RETRY_LATER",
                "risk_level": "MEDIUM",
                "reason": "Multiple retries already attempted"
            }

    # --------------------------------------------------
    # RULE 7: Safe recovery strategy
    # --------------------------------------------------

    if strategy == "SEND_PAYMENT_LINK":

        return {
            "allowed": True,
            "final_action": "SEND_PAYMENT_LINK",
            "risk_level": "LOW",
            "reason": "Payment link recovery is considered low risk"
        }

    # --------------------------------------------------
    # RULE 8: Safe retry
    # --------------------------------------------------

    if strategy == "RETRY_PAYMENT":

        if recovery_probability >= 0.70 and retry_count < 2:

            return {
                "allowed": True,
                "final_action": "RETRY_PAYMENT",
                "risk_level": "MEDIUM",
                "reason": "High recovery probability and retry limit not exceeded"
            }

    # --------------------------------------------------
    # RULE 9: Retry later
    # --------------------------------------------------

    if strategy == "RETRY_LATER":

        return {
            "allowed": True,
            "final_action": "RETRY_LATER",
            "risk_level": "LOW",
            "reason": "Moderate recovery probability; defer retry"
        }

    # --------------------------------------------------
    # RULE 10: Manual escalation
    # --------------------------------------------------

    if strategy == "ESCALATE":

        return {
            "allowed": False,
            "final_action": "ESCALATE",
            "risk_level": "MEDIUM",
            "reason": "Transaction requires manual review"
        }

    # --------------------------------------------------
    # DEFAULT SAFETY
    # --------------------------------------------------

    return {
        "allowed": False,
        "final_action": "NO_ACTION",
        "risk_level": "MEDIUM",
        "reason": "No safe recovery action identified"
    }