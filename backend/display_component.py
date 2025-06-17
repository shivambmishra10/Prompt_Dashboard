"""
Streamlit component for displaying a prompt and model output with customizable styling, expander, and copy-to-clipboard functionality.
"""
import streamlit as st
import streamlit.components.v1 as components
import html

def display_prompt_and_output(prompt_text, model_output, prompt_style=None, output_style=None, expander_label="Model Output"):
    """
    Display a prompt and model output in a visually appealing, styled Streamlit component.

    Parameters:
        prompt_text (str): The prompt text to display (markdown supported).
        model_output (str): The model output to display (shown in a code block).
        prompt_style (dict, optional): CSS-like style dict for the prompt area.
        output_style (dict, optional): CSS-like style dict for the output area.
        expander_label (str, optional): Label for the expander wrapping the output area.

    Returns:
        None
    """
    # Default styles
    default_prompt_style = {
        "background-color": "#f6f6f6",
        "color": "#222",
        "font-size": "16px",
        "border-radius": "8px",
        "padding": "1em",
        "margin-bottom": "1em",
        "border": "1px solid #e0e0e0"
    }
    default_output_style = {
        "background-color": "#fff",
        "color": "#1a237e",
        "font-size": "15px",
        "border-radius": "8px",
        "padding": "1em",
        "border": "1px solid #e0e0e0"
    }
    # Merge styles
    prompt_style = {**default_prompt_style, **(prompt_style or {})}
    output_style = {**default_output_style, **(output_style or {})}
    # Convert style dicts to inline CSS
    def style_dict_to_str(style_dict):
        return "; ".join(f"{k}: {v}" for k, v in style_dict.items())
    prompt_style_str = style_dict_to_str(prompt_style)
    output_style_str = style_dict_to_str(output_style)
    # Render prompt area (markdown, safe)
    st.markdown(f"""
        <div style='{prompt_style_str}'>
            {prompt_text}
        </div>
    """, unsafe_allow_html=True)
    # Expander for output
    with st.expander(expander_label, expanded=False):
        st.markdown(f"<div style='{output_style_str}'>", unsafe_allow_html=True)
        st.code(model_output, language=None)
        st.markdown("</div>", unsafe_allow_html=True)
        # Copy to clipboard button
        components.html(f'''
            <button id="copy-btn" style="margin-top:10px;padding:7px 18px;border-radius:6px;background:#1a237e;color:#fff;border:none;cursor:pointer;font-size:1em;">Copy to Clipboard</button>
            <script>
            const btn = document.getElementById('copy-btn');
            btn.onclick = function() {{
                const text = `{html.escape(model_output).replace('`', '\`')}`;
                navigator.clipboard.writeText(text).then(function() {{
                    btn.innerText = 'Copied!';
                    setTimeout(()=>{{btn.innerText='Copy to Clipboard'}}, 1200);
                }}, function() {{
                    btn.innerText = 'Error!';
                    setTimeout(()=>{{btn.innerText='Copy to Clipboard'}}, 1200);
                }});
            }};
            </script>
        ''', height=50)
        # Feedback message is handled by button text change

# Example usage
if __name__ == "__main__":
    prompt_text = """
**Task:** Write a Python function to calculate the factorial of a number.

*   The function should be named `factorial`.
*   It should take one argument: `n` (an integer).
*   It should return the factorial of `n`.
*   Handle the case where `n` is negative by raising a ValueError.
"""
    model_output = """
def factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
"""
    st.title("Prompt & Model Output Display Demo")
    display_prompt_and_output(
        prompt_text,
        model_output,
        prompt_style={"background-color": "#f0f4f8", "color": "#222", "font-size": "17px"},
        output_style={"background-color": "#f9f9ff", "color": "#1a237e", "font-size": "15px"},
        expander_label="See Model Output"
    )
