# payment_risk.py
# Red flag detection for payment/settlement prompts

PAYMENT_RISK_KEYWORDS = [
    "upi id", "payment credentials", "full upi id", "credential reuse"
]

def check_payment_risk(prompt: str) -> dict:
    for keyword in PAYMENT_RISK_KEYWORDS:
        if keyword.lower() in prompt.lower():
            return {"is_red_flag": True, "reason": f"Contains sensitive payment field: {keyword}"}
    return {"is_red_flag": False, "reason": "No payment risk detected"}
