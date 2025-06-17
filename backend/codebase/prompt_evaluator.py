# prompt_evaluator.py
"""
Evaluate prompts for code generation quality parameters using LLM.
"""

from backend.config import API_KEY, MODEL_URL
from backend.general.gemini import generate_gemini_content
import re
import random

PARAMETERS = [
    "Clarity of Requirements",
    "Execution Awareness",
    "Context & Continuity",
    "Robustness",
    "Scope Control",
    "Realism"
]

EVAL_QUESTIONS = {
    "Clarity of Requirements": "Does this prompt clearly specify the exact functionality, use case, and features required? Answer Yes or No and explain.",
    "Execution Awareness": "Does this prompt mention actual libraries, API names, data formats, and error scenarios? Answer Yes or No and explain.",
    "Context & Continuity": "Does this prompt include previous code context or request modular integration? Answer Yes or No and explain.",
    "Robustness": "Does this prompt ask for edge case handling, error management, and testing? Answer Yes or No and explain.",
    "Scope Control": "Does this prompt clearly define what to include/exclude to avoid overengineering? Answer Yes or No and explain.",
    "Realism": "Does this prompt avoid hallucinated tools and specify real-world APIs, libraries, or platforms? Answer Yes or No and explain."
}

def evaluate_prompt(prompt: str) -> dict:
    """
    For each parameter, ask the LLM the evaluation question and return a probability (0-1) and explanation.
    Probability is estimated from the LLM's answer using keyword and confidence heuristics.
    """
    results = {}
    for param in PARAMETERS:
        # Use LLM self-scoring: ask for a 0-100 score and a one-line remark
        question = (
            f"Prompt: {prompt}\n\nOn a scale from 0 (not at all) to 100 (perfectly), how well does this prompt satisfy the requirement: {param}? Output only a number.\n"
            f"In one short sentence, what is the main issue or strength of this prompt for this parameter?"
        )
        result = generate_gemini_content(question, API_KEY, MODEL_URL)
        try:
            # Defensive: check for candidates and content structure
            candidates = result.get('candidates')
            if not candidates or not isinstance(candidates, list):
                raise ValueError("No candidates in LLM response")
            content = candidates[0].get('content')
            if not content or 'parts' not in content or not isinstance(content['parts'], list):
                raise ValueError("No content parts in LLM response")
            answer = content['parts'][0].get('text', '').strip()
            # Extract the first number in the answer
            match = re.search(r'(\d{1,3})', answer)
            if match:
                score = int(match.group(1))
                prob = 1 - (score / 100)
            else:
                prob = 0.5  # fallback if no number found
            # Extract the first non-numeric line as the remark
            lines = [line.strip() for line in answer.split('\n') if line.strip()]
            remark = ""
            for line in lines:
                if not re.match(r'^\d{1,3}$', line):
                    remark = line
                    break
            results[param] = {"probability": prob, "remark": remark or "No remark"}
        except Exception as e:
            results[param] = {"probability": 0.5, "remark": f"Error: {e}"}
    return results
