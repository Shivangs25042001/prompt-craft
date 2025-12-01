import streamlit as st
from openai import OpenAI
import json

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="PromptCraft AI", page_icon="✨", layout="wide")

# ---------------------------------------------------------
# 2. EMBEDDED LOGOS (Base64 SVGs)
# ---------------------------------------------------------
# These are the actual logos converted to code so they NEVER fail to load.
LOGOS = {
    "GPT-4": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0MSA0MSI+PHBhdGggZmlsbD0iIzEwYTM3ZiIgZD0iMzcucjQgMTUuMmExMC4yIDEwLjIgMCAwIDAtLjg4LTguM2MxMC4zMiAxMC4zMiAwIDAgMC0xMS4wOC00LjlsLS4wMi0uMDFhOC4xMiA4LjEyIDAgMCAwLTEzLjYgMTEuOTggMTAuMTcgMTAuMTcgMCAwIDAtNi44IDQuOTIgMTAuMiAxMC4yIDAgMCAwIDEuMjYgMTIuMDYgMTAuMTcgMTAuMTcgMCAwIDAgMTEuMDggNC45bC4wMi4wMWE4LjEyIDguMTIgMCAwIDAgMTMuNi0xMS45OCAxMC4xNyAxMC4xNyAwIDAgMCA2LjgtNC45MmguMDF6bS0xNS4zNCAyMS40M2E3LjYyIDcuNjIgMCAwIDEtNC44OS0xLjc3bC4yNC0uMTQgOC4xMy00LjY5YTEuMzYgMS4zNiAwIDAgMCAuNjctMS4xNnYtMTEuNDZsMy40MyAyYTEuMjkgMS4yOSAwIDAgMCAuMDYuMDl2OS41MWE3LjY2IDcuNjYgMCAwIDEtNy42NCA3LjYzem0tMTYuNDQtNy4wMmE3LjYgNy42IDAgMCAxLS45MS01LjEzbC4yNC4xNSA4LjEzIDQuNjlhMS4zMSAxLjMxIDAgMCAwIDEuMzMgMGw5Ljk0LTUuNzN2NC45NmEuMTYuMTYgMCAwIDEtLjA2LjFsLTguMjIgNC43NGE3LjY1IDcuNjUgMCAwIDEtMTAuNDUtMy42MnpNMy45OCAxMy40M2E3LjYzIDcuNjMgMCAwIDEgNC4wMy0zLjM1VjE5LjhjMCAuNDcuMjMuOS42NiAxLjE1bDkuODkgNS43MS0zLjQ0IDEuOTlhMS4yOSAxLjI5IDAgMCAxLS4xMiAwTC44NyAxOS4wNmE3LjY2IDcuNjYgMCAwIDEgMy4xMS01LjYzem0yOC4yMyA2LjU2TDIyLjI5IDE0LjIgbDIuNTctMS40OGExLjI5IDEuMjkgMCAwIDEgLjEyIDBsOC4yMiA0Ljc1YTcuNjUgNy42NSAwIDAgMS0xLjE1IDEzLjc5di05LjY2YTEuMzUgMS4zNSAwIDAgMC0uNjktMS4xNHptMy40Mi01LjE1bC0uMjQtLjE0LTguMTItNC43M2ExLjMyIDEuMzIgMCAwIDAtMS4zMyAwbC05Ljk0IDUuNzNWMTEuNzNhLjExLjExIDAgMCAxIC4wNS0uMWw4LjIyLTQuNzVhNy42NSA3LjY1IDAgMCAxIDExLjM2IDcuOTN6bS0xOS44IDE2LjhMNy43NiAyMS44aC4wNmEubMTIuNTUgNy4yNXY1Ljg4YTcuNjUgNy42NSAwIDAgMS00LjUzIDYuNzRsLS4yNC4xNC0uMTMtLjF6bTEuODUtMy45NWwyNi4xMSAxMi4xLTEwLjA1IDUuOGE3LjY1IDcuNjUgMCAwIDEtLjEtOS42NnptMCAwIi8+PC9zdmc+",
    "Claude": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48cGF0aCBmaWxsPSIjZDk3NzU3IiBkPSJNNTAgNUwyMCA5MGg2MEw1MCA1eiIvPjwvc3ZnPg==", 
    "Gemini": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0idXJsKCNhKSIgZD0iTTIyIDEyYTEwIDEwIDAgMCAxLTEwIDEwQTEwIDEwIDAgMCAxIDIgMTJhMTAgMTAgMCAwIDEgMTAtMTBBMTAgMTAgMCAwIDEgMjIgMTJ6Ii8+PGRlZnM+PGxpbmVhckdyYWRpZW50IGlkPSJhIiB4MT0iMCIgeTE9IjAiIHgyPSIyNCIgeTI9IjI0IiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjNGE5MGUyIi8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjYTg1NWY3Ii8+PC9saW5lYXJHcmFkaWVudD48L2RlZnM+PC9zdmc+",
    "Llama": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDA2OGUxIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+PHBhdGggZD0iTTEyIDJDMiAxMiA1IDIyIDUgMjJzOS02IDctMTJzMTAtNC41IDEwLTQuNVMxOSAyIDEyIDJ6Ii8+PC9zdmc+",
    "General": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjNmI3MjgwIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+PHJlY3QgeD0iMyIgeT0iMyIgd2lkdGg9IjE4IiBoZWlnaHQ9IjE4IiByeD0iMiIgcnk9IjIiLz48bGluZSB4MT0iMyIgeTE9IjkiIHgyPSIyMSIgeTI9IjkiLz48bGluZSB4MT0iOSIgeTE9IjIxIiB4Mj0iOSIgeTI9IjkiLz48L3N2Zz4="
}

# ---------------------------------------------------------
# 3. ADVANCED STYLING (Pixel-Perfect Fixes)
# ---------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    .stApp {{
        background-color: #FAFAFA;
        font-family: 'Inter', sans-serif;
    }}
    
    /* 1. LAYOUT CONSTRAINTS (Fixes the "stretched" look) */
    .main-container {{
        max-width: 800px;
        margin: 0 auto;
        padding: 0 20px;
    }}
    
    /* Hide Streamlit Header */
    header, footer {{visibility: hidden;}}
    .block-container {{ padding-top: 2rem; }}

    /* 2. INPUT BOX (Modern & Clean) */
    .stTextArea textarea {{
        background-color: #FFFFFF;
        border: 2px solid #E5E7EB;
        border-radius: 12px;
        padding: 16px;
        font-size: 16px;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }}
    .stTextArea textarea:focus {{
        border-color: #8B5CF6;
        box-shadow: 0 0 0 4px #F3E8FF;
    }}
    
    /* Label Styling */
    p {{
        font-size: 16px;
        font-weight: 600;
        color: #374151;
        margin-bottom: 8px;
    }}

    /* 3. CARD SELECTION GRID (The Real Fix) */
    /* Container */
    .stRadio > div {{
        display: grid;
        grid-template-columns: repeat(5, 1fr); /* Force 5 columns */
        gap: 15px;
        width: 100%;
    }}
    
    /* Individual Cards */
    .stRadio > div > label {{
        background-color: #FFFFFF !important;
        border: 2px solid #E5E7EB !important;
        border-radius: 16px !important;
        height: 120px !important;
        width: 100% !important;
        min-width: 0 !important; /* Prevents overflow */
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: flex-end !important;
        padding-bottom: 15px !important;
        cursor: pointer !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        transition: all 0.2s ease !important;
        position: relative;
    }}

    /* Hover */
    .stRadio > div > label:hover {{
        border-color: #C4B5FD !important;
        transform: translateY(-4px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.05) !important;
    }}

    /* Selected */
    .stRadio > div > label[data-baseweb="radio"] {{
        background-color: #F5F3FF !important;
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 4px #DDD6FE !important;
    }}

    /* Text */
    .stRadio p {{
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #374151 !important;
    }}

    /* Hide Circle */
    .stRadio div[role="radio"] {{ display: none !important; }}

    /* LOGO INJECTION */
    .stRadio > div > label::before {{
        content: "";
        position: absolute;
        top: 25px;
        width: 40px;
        height: 40px;
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
    }}

    /* Specific Logos */
    .stRadio > div > label:nth-child(1)::before {{ background-image: url('{LOGOS["GPT-4"]}'); }}
    .stRadio > div > label:nth-child(2)::before {{ background-image: url('{LOGOS["Claude"]}'); }}
    .stRadio > div > label:nth-child(3)::before {{ background-image: url('{LOGOS["Gemini"]}'); }}
    .stRadio > div > label:nth-child(4)::before {{ background-image: url('{LOGOS["Llama"]}'); }}
    .stRadio > div > label:nth-child(5)::before {{ background-image: url('{LOGOS["General"]}'); opacity: 0.5; }}

    /* 4. GENERATE BUTTON */
    .stButton button {{
        background: linear-gradient(90deg, #8B5CF6 0%, #7C3AED 100%) !important;
        color: white !important;
        border: none !important;
        height: 55px !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        margin-top: 20px !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
    }}
    .stButton button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4) !important;
    }}

    /* 5. RESULTS UI */
    .result-card {{
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }}
    .best-match {{
        border: 2px solid #8B5CF6;
        background: linear-gradient(180deg, #FBF8FF 0%, #FFFFFF 100%);
    }}
    .badge-best {{
        background: #8B5CF6; color: white; padding: 4px 12px;
        border-radius: 20px; font-size: 11px; font-weight: 800;
        text-transform: uppercase; display: inline-block; margin-bottom: 10px;
    }}
    .badge-tag {{
        background: #F3F4F6; color: #4B5563; padding: 4px 10px;
        border-radius: 8px; font-size: 12px; font-weight: 600;
        float: right;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. APP LAYOUT
# ---------------------------------------------------------

# Center Container to fix the "Stretched" look
c_spacer_l, c_main, c_spacer_r = st.columns([1, 6, 1])

with c_main:
    # Header
    st.markdown("""
    <div style='text-align: center; margin-bottom: 40px;'>
        <div style='font-size: 50px; margin-bottom: 10px;'>✨</div>
        <h1 style='color: #111827; margin: 0; font-size: 36px; font-weight: 900;'>PromptCraft AI</h1>
        <p style='color: #6B7280; font-size: 16px; margin-top: 10px;'>Transform your ideas into engineered master prompts.</p>
    </div>
    """, unsafe_allow_html=True)

    # Input
    st.markdown("<p>What do you want to achieve?</p>", unsafe_allow_html=True)
    user_input = st.text_area("label", placeholder="e.g. I want to create a meal plan for a vegan athlete...", height=100, label_visibility="collapsed")

    # Model Selector
    st.write("")
    st.markdown("<p>Select your target LLM</p>", unsafe_allow_html=True)
    model = st.radio(
        "Model",
        ["GPT-4", "Claude", "Gemini", "Llama", "General"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # Generate Button
    if st.button("Generate Prompt Variations →"):
        api_key = st.secrets.get("OPENAI_API_KEY")
        
        if not api_key:
            st.error("⚠️ Please set your OpenAI API Key in Settings!")
        elif not user_input:
            st.warning("Please enter a goal first.")
        else:
            client = OpenAI(api_key=api_key)
            
            with st.spinner("Engineering 8 distinct strategies..."):
                try:
                    # PROMPT LOGIC
                    prompt = f"""
                    Act as an expert Prompt Engineer. Goal: "{user_input}". Model: {model}.
                    Generate 4 distinct strategies in valid JSON:
                    {{
                        "strategies": [
                            {{"title": "Chain of Thought", "tag": "Reasoning", "desc": "Breaks down complex problems.", "code": "Let's think step by step..."}},
                            {{"title": "Role-Based Expert", "tag": "Persona", "desc": "Assigns an expert role.", "code": "You are a World-Class Expert..."}},
                            {{"title": "Structured Output", "tag": "Format", "desc": "Ensures organized output.", "code": "## Summary\\n..."}},
                            {{"title": "Few-Shot Prompting", "tag": "Examples", "desc": "Provides examples to guide style.", "code": "Input: ... Output: ..."}}
                        ]
                    }}
                    """
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "system", "content": "Return JSON only."}, {"role": "user", "content": prompt}],
                        response_format={"type": "json_object"}
                    )
                    data = json.loads(response.choices[0].message.content)
                    strategies = data.get("strategies", [])
                    
                    st.write("")
                    st.markdown("<h3 style='text-align:center; margin: 40px 0;'>✨ Optimized Strategies</h3>", unsafe_allow_html=True)
                    
                    # RESULTS GRID
                    r1c1, r1c2 = st.columns(2)
                    
                    with r1c1:
                        s = strategies[0]
                        st.markdown(f"""
                        <div class="result-card best-match">
                            <span class="badge-best">★ BEST MATCH</span>
                            <span class="badge-tag">{s['tag']}</span>
                            <h3 style="margin-top:10px; font-size:18px; color:#1F2937;">{s['title']}</h3>
                            <p style="color:#6B7280; font-size:14px;">{s['desc']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.code(s['code'], language="markdown")
                        
                        s = strategies[2]
                        st.markdown(f"""
                        <div class="result-card">
                            <span class="badge-tag">{s['tag']}</span>
                            <h3 style="margin-top:0; font-size:18px; color:#111827;">{s['title']}</h3>
                            <p style="color:#6B7280; font-size:14px;">{s['desc']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.code(s['code'], language="markdown")

                    with r1c2:
                        s = strategies[1]
                        st.markdown(f"""
                        <div class="result-card">
                            <span class="badge-tag">{s['tag']}</span>
                            <h3 style="margin-top:0; font-size:18px; color:#111827;">{s['title']}</h3>
                            <p style="color:#6B7280; font-size:14px;">{s['desc']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.code(s['code'], language="markdown")

                        s = strategies[3]
                        st.markdown(f"""
                        <div class="result-card">
                            <span class="badge-tag">{s['tag']}</span>
                            <h3 style="margin-top:0; font-size:18px; color:#111827;">{s['title']}</h3>
                            <p style="color:#6B7280; font-size:14px;">{s['desc']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.code(s['code'], language="markdown")

                except Exception as e:
                    st.error(f"Error: {e}")
