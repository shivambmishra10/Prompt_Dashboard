# loan_risk.py
# Red flag detection for loan processing prompts

LOAN_RISK_KEYWORDS = [
    "credit_score", "pii", "applicant data", "loan_id", "income", "pan", "aadhaar"
]

def check_loan_risk(prompt: str) -> dict:
    for keyword in LOAN_RISK_KEYWORDS:
        if keyword.lower() in prompt.lower():
            return {"is_red_flag": True, "reason": f"Contains sensitive loan field: {keyword}"}
    return {"is_red_flag": False, "reason": "No loan risk detected"}
