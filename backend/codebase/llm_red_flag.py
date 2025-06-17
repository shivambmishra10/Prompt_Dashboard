# llm_red_flag.py
# LLM-based red flag detection for banking and sensitive data
from backend.config import API_KEY, MODEL_URL
from backend.general.gemini import generate_gemini_content

def check_red_flag_llm(prompt: str) -> dict:
    """
    Use LLM to detect if a prompt contains or requests sensitive banking/PII/production data.
    Returns: {is_red_flag: bool, reason: str}
    """
    system_prompt = (
        "You are a security and compliance assistant for banking software. "
        "Analyze the following prompt and determine if it requests, exposes, or manipulates sensitive or regulated data. "
        "Sensitive examples include: customer_id (e.g., CUST98342, real customer mapping), account_number (e.g., 5087 6543 2198 7654, Indian account format), "
        "email (e.g., amit.sinha@finbank.com, real user/employee), upi_id (e.g., amit.sinha@upi, Indian payment identifier), prod_backup.csv (filename suggests live data dump), "
        "or any PII, production, or unmasked customer information. "
        "If so, output 'RED FLAG' and a short reason. If not, output 'SAFE'."
    )
    full_prompt = f"{system_prompt}\n\nPrompt: {prompt}\n\nOutput:"
    result = generate_gemini_content(full_prompt, API_KEY, MODEL_URL)
    try:
        answer = result['candidates'][0]['content']['parts'][0]['text'].strip().lower()
        if answer.startswith('red flag'):
            reason = answer.split('red flag',1)[-1].strip(': .-\n')
            return {"is_red_flag": True, "reason": reason or "Sensitive data detected by LLM"}
        else:
            return {"is_red_flag": False, "reason": "No red flag detected by LLM"}
    except Exception as e:
        return {"is_red_flag": False, "reason": f"LLM check error: {e}"}
