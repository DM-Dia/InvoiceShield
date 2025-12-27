def calculate_fraud_score(is_anomaly: bool, rule_flags: dict) -> int:
    score = 0

    if is_anomaly:
        score += 40

    score += sum(10 for v in rule_flags.values() if v)

    return min(score, 100)
