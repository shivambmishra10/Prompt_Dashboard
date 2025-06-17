# account_risk.py
# Red flag detection for account & user data prompts

ACCOUNT_RISK_KEYWORDS = [
    "aadhaar", "pan", "mobile", "email", "account_id", "balance", "unmasked"
]

def check_account_risk(prompt: str) -> dict:
    for keyword in ACCOUNT_RISK_KEYWORDS:
        if keyword.lower() in prompt.lower():
            return {"is_red_flag": True, "reason": f"Contains sensitive account/user field: {keyword}"}
    return {"is_red_flag": False, "reason": "No account/user risk detected"}
