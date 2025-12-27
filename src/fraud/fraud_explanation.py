def explain_fraud_score(
    is_anomaly: bool,
    rule_flags: dict,
    fraud_score: int
) -> dict:
    reasons = []

    if is_anomaly:
        reasons.append("Invoice flagged as anomalous based on historical patterns")

    for rule, triggered in rule_flags.items():
        if triggered:
            reasons.append(f"Rule triggered: {rule}")

    if not reasons:
        reasons.append("No significant risk indicators detected")

    return {
        "fraud_score": fraud_score,
        "risk_level": (
            "High" if fraud_score >= 70
            else "Medium" if fraud_score >= 40
            else "Low"
        ),
        "reasons": reasons
    }