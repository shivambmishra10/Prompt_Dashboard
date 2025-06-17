# red_flag.py
# Combined red flag detection for all risk types

from backend.codebase.transaction_risk import check_transaction_risk
from backend.codebase.payment_risk import check_payment_risk
from backend.codebase.account_risk import check_account_risk
from backend.codebase.loan_risk import check_loan_risk
from backend.codebase.fraud_risk import check_fraud_risk

def check_red_flag(prompt: str) -> dict:
    """
    Check all risk modules and return a formatted red flag if any are triggered.
    """
    checks = [
        check_transaction_risk(prompt),
        check_payment_risk(prompt),
        check_account_risk(prompt),
        check_loan_risk(prompt),
        check_fraud_risk(prompt)
    ]
    for check in checks:
        if check["is_red_flag"]:
            return {
                "is_red_flag": True,
                "reason": f"🚩 <b>Red Flag:</b> Sensitive data detected. <span style='color:#ff5555'>Not good to proceed.</span><br><i>{check['reason']}</i>"
            }
    return {"is_red_flag": False, "reason": "No red flags detected."}
