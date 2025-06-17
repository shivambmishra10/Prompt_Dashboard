# fraud_risk.py
# Red flag detection for risk & fraud analytics prompts

FRAUD_RISK_KEYWORDS = [
    "ip_address", "device_id", "raw logs", "location", "personal device", "real-time access"
]

def check_fraud_risk(prompt: str) -> dict:
    for keyword in FRAUD_RISK_KEYWORDS:
        if keyword.lower() in prompt.lower():
            return {"is_red_flag": True, "reason": f"Contains sensitive fraud/risk field: {keyword}"}
    return {"is_red_flag": False, "reason": "No fraud/risk detected"}
