# prompt_templates.py

def enhance_prompt(prompt):
    """Enhance a prompt to be more descriptive for LLMs, with context and examples."""
    return (
        "You are an expert prompt engineer. Improve the following prompt by making it more detailed, clear, and actionable for an LLM agent. "
        "Add relevant context if missing, and provide 1-2 short example completions if possible.\n\n"
        f"Prompt: {prompt}\n\nImproved Prompt:"
    )
