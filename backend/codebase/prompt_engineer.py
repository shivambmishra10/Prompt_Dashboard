# codebase/prompt_engineer.py
"""
Prompt engineering logic for codebase-specific tasks.
"""

from backend.config import API_KEY, MODEL_URL
from backend.general.gemini import generate_gemini_content
from backend.codebase.clarity_training import CLARITY_EXAMPLES
from backend.codebase.context_training import CONTEXT_EXAMPLES
from backend.codebase.execution_training import EXECUTION_EXAMPLES
from backend.codebase.hallucination_training import ROBUSTNESS_EXAMPLES
from backend.codebase.scope_training import SCOPE_EXAMPLES
from backend.codebase.realism_training import REALISM_EXAMPLES

def improve_code_prompt(user_task: str) -> str:
    """
    Transform a vague code-related task into a high-quality, LLM-ready prompt using Gemini API and all codebase training examples.
    """
    # Build few-shot prompt using all training examples
    def format_examples(examples, label_from, label_to):
        return "\n".join([
            f"{label_from}: {ex['vague']}\n{label_to}: {ex[list(ex.keys())[1]]}" for ex in examples[:2]
        ])
    clarity = format_examples(CLARITY_EXAMPLES, "Vague", "Clarified")
    context = format_examples(CONTEXT_EXAMPLES, "Vague", "Contextual")
    execution = format_examples(EXECUTION_EXAMPLES, "Vague", "Execution")
    hallucination = format_examples(ROBUSTNESS_EXAMPLES, "Vague", "Robust")
    scope = format_examples(SCOPE_EXAMPLES, "Vague", "Scoped")
    realism = format_examples(REALISM_EXAMPLES, "Vague", "Realistic")
    few_shot_examples = f"""
# Clarity\n{clarity}\n\n# Context & Continuity\n{context}\n\n# Execution Awareness\n{execution}\n\n# Hallucination/Robustness\n{hallucination}\n\n# Scope Control\n{scope}\n\n# Realism\n{realism}\n"""
    instruction = (
        "You are an expert code generation assistant. Rewrite the following vague coding task into a complete, specific, and robust prompt for an LLM to generate production-quality code. Ensure the following:\n\n"
        "1. **Clarity of Requirements**: Specify exact functionality, use case, and features.\n"
        "2. **Execution Awareness**: Mention actual libraries, API names, data formats, and error scenarios.\n"
        "3. **Context & Continuity**: Include any previous code context if available, or request for modular integration.\n"
        "4. **Robustness**: Ask for edge case handling, error management, and testing.\n"
        "5. **Scope Control**: Clearly define what to include/exclude to avoid overengineering.\n"
        "6. **Realism**: Avoid hallucinated tools; specify real-world APIs, libraries, or platforms.\n\n"
        "---\n\nHere are some examples for each principle:\n" + few_shot_examples +
        "---\n\n### Input:\nA user provides a vague coding task:  \n**\"" + user_task + "\"**\n\n---\n\n### Output:\nRewrite this as a high-quality, LLM-ready prompt that satisfies all the principles above."
    )
    result = generate_gemini_content(instruction, API_KEY, MODEL_URL)
    try:
        llm_text = result['candidates'][0]['content']['parts'][0]['text'].strip()
        return llm_text
    except (KeyError, IndexError, TypeError):
        return "Error: Unexpected response format from LLM."
