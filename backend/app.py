import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from backend.config import API_KEY, MODEL_URL
from backend.general.gemini import generate_gemini_content
from backend.general.prompt_templates import enhance_prompt
from backend.codebase.prompt_engineer import improve_code_prompt
from backend.codebase.prompt_evaluator import evaluate_prompt, PARAMETERS
from backend.codebase.red_flag import check_red_flag
from backend.codebase.llm_red_flag import check_red_flag_llm
import pandas as pd

st.title("Prompt Engineering Dashboard [Experimental]")

# Remove theme toggle and use static colors
prompt_bg = '#23272f'
prompt_color = '#f3f3f3'
prompt_border = '#353a45'
prompt_title = '#7ed6df'
code_bg = '#1a1d23'
code_color = '#f3f3f3'

mode = st.radio("Choose Mode:", ["General Purpose", "Techno Functional"], horizontal=True)

prompt = st.text_area("Enter your prompt:")
enhance = st.checkbox("Enhance prompt before sending", value=True)

if st.button("Generate"): 
    if mode == "General Purpose":
        if enhance:
            prompt_to_send = enhance_prompt(prompt)
        else:
            prompt_to_send = prompt
        with st.spinner("Contacting General Purpose..."):
            result = generate_gemini_content(prompt_to_send, API_KEY, MODEL_URL)
            if "error" in result:
                st.error(f"Gemini API Error: {result['error']}")
            else:
                try:
                    llm_text = result['candidates'][0]['content']['parts'][0]['text'].strip()
                    # Try to extract an example if present (simple heuristic)
                    example = None
                    if "Example:" in llm_text:
                        parts = llm_text.split("Example:", 1)
                        enhanced = parts[0].strip()
                        example = parts[1].strip()
                    else:
                        enhanced = llm_text
                    # --- Improved Display ---
                    style_block = f"""
                        <style>
                        .enhanced-prompt-box {{
                            background: linear-gradient(135deg, {prompt_bg} 60%, {code_bg} 100%);
                            border-radius: 14px;
                            padding: 2em 2em 1.5em 2em;
                            margin-bottom: 1.5em;
                            box-shadow: 0 4px 24px rgba(44,62,80,0.13);
                            border: 1.5px solid {prompt_border};
                            font-size: 1.13em;
                            color: {prompt_color};
                            position: relative;
                        }}
                        .enhanced-prompt-title {{
                            font-size: 1.25em;
                            font-weight: 700;
                            margin-bottom: 0.7em;
                            color: {prompt_title};
                        }}
                        .copy-btn-ep {{
                            position: absolute;
                            top: 1.5em;
                            right: 2em;
                            background: {prompt_border};
                            color: {prompt_title};
                            border: none;
                            border-radius: 6px;
                            padding: 0.3em 1.1em;
                            font-size: 1em;
                            cursor: pointer;
                            transition: background 0.2s;
                        }}
                        .copy-btn-ep:hover {{
                            background: {prompt_title};
                            color: {prompt_bg};
                        }}
                        </style>
                    """
                    st.markdown(style_block, unsafe_allow_html=True)
                    prompt_box = (
                        f"<div class='enhanced-prompt-box'>"
                        f"<div class='enhanced-prompt-title'>✨ Enhanced Prompt (Ready to Copy)</div>"
                        f"<pre id='enhancedPromptText' style='white-space:pre-wrap; word-break:break-word; background:transparent; color:{prompt_color}; border:none; font-size:1.08em; margin-bottom:0.7em;'>"
                        f"{enhanced.replace('<','&lt;').replace('>','&gt;')}"
                        f"</pre>"
                        f"<button class='copy-btn-ep' onclick=\"navigator.clipboard.writeText(document.getElementById('enhancedPromptText').innerText);var btn=this;btn.innerText='Copied!';setTimeout(()=>{{btn.innerText='Copy'}},1200);\">Copy</button>"
                        f"</div>"
                    )
                    st.markdown(prompt_box, unsafe_allow_html=True)
                    # Example Output and Tips
                    if example:
                        st.markdown("<div class='example-section'><b>Example Output:</b></div>", unsafe_allow_html=True)
                        st.code(example, language=None)
                    st.markdown("<div class='tips-section'><b>Tips:</b><ul><li>The enhanced prompt is concise and ready for LLMs.</li><li>Use the copy button in the top right of the box.</li><li>If you want more examples, try making your original prompt more specific.</li><li>Use the 'Enhance' toggle to compare raw vs. enhanced prompts.</li></ul></div>", unsafe_allow_html=True)
                except (KeyError, IndexError, TypeError):
                    st.error("Error: Unexpected response format.")
    else:
        # Codebase mode: modern pipeline visualization and logic
        pipeline_labels = [
            "Red Flag Check",
            "Prompt Enhancement",
            "Quality Comparison"
        ]
        pipeline_status = [None, None, None]  # None=not started, 'running', 'done', 'fail'
        current_step = 0
        # Step 1: Red Flag Check
        pipeline_status[0] = 'running'
        st.markdown("""
            <style>
            .pipeline-container {display: flex; align-items: center; margin-bottom: 2em;}
            .pipeline-item {display: flex; flex-direction: column; align-items: center; margin: 0 1.5em;}
            .pipeline-icon {font-size: 2.1em; margin-bottom: 0.2em;}
            .pipeline-label {font-size: 1.08em; font-weight: 500; margin-top: 0.2em;}
            .pipeline-connector {height: 4px; width: 2.5em; background: #888; border-radius: 2px; margin: 0 0.2em;}
            .pipeline-icon-done {color: #27ae60;}
            .pipeline-icon-fail {color: #e74c3c;}
            .pipeline-icon-running {animation: spin 1.2s linear infinite; color: #f1c40f;}
            @keyframes spin {100% {transform: rotate(360deg);}}
            .pipeline-icon-wait {color: #888;}
            </style>
        """, unsafe_allow_html=True)
        pipeline_placeholder = st.empty()
        def render_pipeline(status):
            icons = {
                'done': "<span class='pipeline-icon pipeline-icon-done'>✅</span>",
                'fail': "<span class='pipeline-icon pipeline-icon-fail'>❌</span>",
                'running': "<span class='pipeline-icon pipeline-icon-running'>⏳</span>",
                None: "<span class='pipeline-icon pipeline-icon-wait'>-</span>"
            }
            html = "<div class='pipeline-container'>"
            for i, label in enumerate(pipeline_labels):
                html += f"<div class='pipeline-item'>{icons[status[i]]}<span class='pipeline-label'>{label}</span></div>"
                if i < len(pipeline_labels)-1:
                    html += "<div class='pipeline-connector'></div>"
            html += "</div>"
            pipeline_placeholder.markdown(html, unsafe_allow_html=True)
        render_pipeline(pipeline_status)
        with st.spinner("Checking for sensitive data and compliance flags..."):
            red_flag = check_red_flag_llm(prompt)
        if red_flag["is_red_flag"]:
            pipeline_status[0] = 'fail'
            render_pipeline(pipeline_status)
            st.markdown("""
                <style>
                .red-flag-box {
                    background: #e74c3c;
                    color: #fff;
                    border-radius: 16px;
                    padding: 2em 2.5em 1.5em 4em;
                    margin: 2em 0 1.5em 0;
                    font-size: 1.25em;
                    font-weight: 600;
                    box-shadow: 0 4px 24px rgba(231,76,60,0.15);
                    border-left: 12px solid #b30000;
                    position: relative;
                    min-height: 90px;
                    display: flex;
                    align-items: center;
                }
                .red-flag-icon {
                    position: absolute;
                    left: 1.2em;
                    top: 1.2em;
                    font-size: 2.2em;
                    color: #fff;
                    filter: drop-shadow(0 2px 4px #b30000);
                }
                .red-flag-reason {
                    font-size: 1.05em;
                    font-weight: 400;
                    margin-top: 0.5em;
                    color: #fffbe6;
                    font-style: italic;
                }
                </style>
            """, unsafe_allow_html=True)
            st.markdown(f"""
                <div class='red-flag-box'>
                    <span class='red-flag-icon'>🚩</span>
                    <div>
                        Red Flag: Sensitive data detected.<br>
                        <span class='red-flag-reason'>{red_flag['reason']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            pipeline_status[0] = 'done'
            pipeline_status[1] = 'running'
            render_pipeline(pipeline_status)
            with st.spinner("Enhancing prompt for best LLM results..."):
                improved_prompt = improve_code_prompt(prompt)
            pipeline_status[1] = 'done'
            pipeline_status[2] = 'running'
            render_pipeline(pipeline_status)
            # --- Improved Display ---
            style_block = f"""
                <style>
                .enhanced-prompt-box {{
                    background: linear-gradient(135deg, {prompt_bg} 60%, {code_bg} 100%);
                    border-radius: 14px;
                    padding: 2em 2em 1.5em 2em;
                    margin-bottom: 1.5em;
                    box-shadow: 0 4px 24px rgba(44,62,80,0.13);
                    border: 1.5px solid {prompt_border};
                    font-size: 1.13em;
                    color: {prompt_color};
                    position: relative;
                }}
                .enhanced-prompt-title {{
                    font-size: 1.25em;
                    font-weight: 700;
                    margin-bottom: 0.7em;
                    color: {prompt_title};
                }}
                .copy-btn-ep {{
                    position: absolute;
                    top: 1.5em;
                    right: 2em;
                    background: {prompt_border};
                    color: {prompt_title};
                    border: none;
                    border-radius: 6px;
                    padding: 0.3em 1.1em;
                    font-size: 1em;
                    cursor: pointer;
                    transition: background 0.2s;
                }}
                .copy-btn-ep:hover {{
                    background: {prompt_title};
                    color: {prompt_bg};
                }}
                </style>
            """
            st.markdown(style_block, unsafe_allow_html=True)
            prompt_box = (
                f"<div class='enhanced-prompt-box'>"
                f"<div class='enhanced-prompt-title'>✨ Enhanced Prompt (Ready to Copy)</div>"
                f"<pre id='enhancedPromptText' style='white-space:pre-wrap; word-break:break-word; background:transparent; color:{prompt_color}; border:none; font-size:1.08em; margin-bottom:0.7em;'>"
                f"{improved_prompt.replace('<','&lt;').replace('>','&gt;')}"
                f"</pre>"
                f"<button class='copy-btn-ep' onclick=\"navigator.clipboard.writeText(document.getElementById('enhancedPromptText').innerText);var btn=this;btn.innerText='Copied!';setTimeout(()=>{{btn.innerText='Copy'}},1200);\">Copy</button>"
                f"</div>"
            )
            st.markdown(prompt_box, unsafe_allow_html=True)
            with st.spinner("Final quality comparison and scoring..."):
                old_eval = evaluate_prompt(prompt)
                new_eval = evaluate_prompt(improved_prompt)
            pipeline_status[2] = 'done'
            render_pipeline(pipeline_status)
            df = pd.DataFrame({
                "Parameter": PARAMETERS,
                "Old Prompt Feature Probability": [1 - x["probability"] for x in old_eval.values()],
                "Enhanced Prompt Feature Probability": [1 - x["probability"] for x in new_eval.values()],
                "Old Remark": [x["remark"] for x in old_eval.values()],
                "Enhanced Remark": [x["remark"] for x in new_eval.values()]
            })
            st.markdown("<div class='tips-section'><b>Prompt Quality Comparison Table (LLM-Evaluated)</b></div>", unsafe_allow_html=True)
            st.dataframe(df.style.format({
                'Old Prompt Feature Probability': '{:.0%}',
                'Enhanced Prompt Feature Probability': '{:.0%}'
            }), use_container_width=True)
            st.markdown("<div class='tips-section'><b>Tips:</b><ul><li>Higher percentage means the feature is more likely present in the prompt.</li><li>Remarks highlight the main difference for each parameter.</li></ul></div>", unsafe_allow_html=True)
