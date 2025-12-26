def rule_flags(data):
    issues = []

    if data["tax_percent"] > 30:
        issues.append("High tax percentage")

    if len(data["invoice_number"]) < 3:
        issues.append("Suspicious invoice number")

    return ", ".join(issues) if issues else "No Issues"