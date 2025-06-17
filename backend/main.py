# main.py
"""
Entry point for the Gemini Prompt Generator application.
"""

import argparse
from backend.config import API_KEY, MODEL_URL
from backend.prompt_templates import enhance_prompt
from backend.gemini import generate_gemini_content


def main():
    parser = argparse.ArgumentParser(description="Gemini Prompt Generator")
    parser.add_argument('--prompt', type=str, help='Prompt to send to Gemini API')
    parser.add_argument('--enhance', action='store_true', help='Enhance the prompt before sending')
    args = parser.parse_args()

    if args.prompt:
        prompt = args.prompt
    else:
        prompt = input("Enter your prompt: ")
    if args.enhance:
        prompt = enhance_prompt(prompt)
    result = generate_gemini_content(prompt, API_KEY, MODEL_URL)
    # Extract and print only the LLM response text
    try:
        llm_text = result['candidates'][0]['content']['parts'][0]['text']
        print(llm_text.strip())
    except (KeyError, IndexError, TypeError):
        print("Error: Unexpected response format.")

if __name__ == "__main__":
    main()
