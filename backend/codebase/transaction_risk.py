# transaction_risk.py
# Red flag detection for transaction-related prompts

import re

TRANSACTION_RISK_KEYWORDS = [
    "card_number", "cvv", "pin", "account_number", "failed card transactions", "main db",
    "customer_id", "customer id", "transaction_id", "transaction id", "payment_id", "payment id"
]

TRANSACTION_RISK_PATTERNS = [
    r"\b\d{12,19}\b",  # possible card numbers
    r"\b\d{3,4}\b",   # possible CVV or PIN (contextual)
    r"account\s*number", r"card\s*number", r"cvv", r"pin"
]

def check_transaction_risk(prompt: str) -> dict:
    # Keyword check
    for keyword in TRANSACTION_RISK_KEYWORDS:
        if keyword.lower() in prompt.lower():
            return {"is_red_flag": True, "reason": f"Contains sensitive transaction field: {keyword}"}
    # Pattern check
    for pattern in TRANSACTION_RISK_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return {"is_red_flag": True, "reason": f"Contains sensitive transaction pattern: {pattern}"}
    # Contextual check for unmasked data
    if re.search(r"unmasked|raw|full|export all", prompt, re.IGNORECASE):
        return {"is_red_flag": True, "reason": "Prompt suggests unmasked or raw sensitive data export"}
    return {"is_red_flag": False, "reason": "No transaction risk detected"}
