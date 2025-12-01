import streamlit as st
from openai import OpenAI
import json

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="PromptCraft AI", page_icon="✨", layout="wide")

# ---------------------------------------------------------
# 2. ASSETS (Embedded Logos to prevent broken images)
# ---------------------------------------------------------
# These are SVG icons converted to Base64 so they work instantly without file uploads.
ICONS = {
    "GPT-4": "https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg",
    "Claude": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Anthropic.svg/1024px-Anthropic.svg.png",
    "Gemini": "https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg",
    "Llama": "https://cdn.icon-icons.com/icons2/4222/PNG/512/meta_logo_icon_262793.png",
    "General": "https://cdn-icons-png.flaticon.com/512/3524/3524335.png"
}

# ---------------------------------------------------------
# 3. CSS STYLING (Matching your HTML Canvas)
# ---------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    .stApp {{
        background-color: #FAFAFA;
        font-family: 'Inter', sans-serif;
    }}
    
    /* Hide Default Header/Footer */
    header, footer {{visibility: hidden;}}
    
    /* CENTER HEADER */
    .header-container {{
        text-align: center;
        padding-top: 40px;
        padding-bottom: 20px;
    }}
    .header-icon {{ font-size: 50px; margin-bottom: 10px; }}
    .header-title {{ 
        font-size: 42px; 
        font-weight: 800; 
        color: #111827; 
        margin: 0; 
        letter-spacing: -1px;
    }}
    .header-sub {{ color: #6B7280; font-size: 18px; margin-top: 10px; }}

    /* INPUT AREA */
    .stTextArea textarea {{
        background-color: #FFFFFF;
        border: 2px solid #E5E7EB;
        border-radius: 12px;
        padding: 20px;
        font-size: 16px;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }}
    .stTextArea textarea:focus {{
        border-color: #8B5CF6;
        box-shadow: 0 0 0 4px #F3E8FF;
    }}
    .stTextArea label {{
        display: none; /* We use our own custom label */
    }}

    /* -------------------------------------------------------
       RADIO BUTTONS -> CARDS (The Magic Fix)
       ------------------------------------------------------- */
    /* Container Row */
    .stRadio > div {{
        display: flex;
        flex-direction: row;
        gap: 15px;
        width: 100%;
        overflow-x: auto;
        justify-content: center;
        padding-bottom: 10px;
    }}

    /* The Card (Label) */
    .stRadio > div > label {{
        background-color: white !important;
        border: 2px solid #E5E7EB !important;
        border-radius: 16px !important;
        padding: 15px !important;
        width: 130px !important;
        height: 120px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: flex-end !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
        position: relative;
    }}

    /* Text inside Card */
    .stRadio > div > label > div[data-testid="stMarkdownContainer"] > p {{
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #374151 !important;
        margin-top: 45px !important; /* Make room for icon */
    }}

    /* Hide the circle */
    .stRadio div[role="radio"] {{
        display: none !important;
    }}

    /* Selected State */
    .stRadio > div > label[data-baseweb="radio"] {{
        background-color: #F5F3FF !important;
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 4px #DDD6FE !important;
    }}
    
    /* Hover State */
    .stRadio > div > label:hover {{
        border-color: #C4B5FD !important;
        transform: translateY(-2px);
    }}

    /* -------------------------------------------------------
       INJECTING ICONS (Using nth-child to target each card)
       ------------------------------------------------------- */
    .stRadio > div > label::before {{
        content: "";
        position: absolute;
        top: 25px;
        left: 50%;
        transform: translateX(-50%);
        width: 40px;
        height: 40px;
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
    }}

    /* 1. GPT-4 */
    .stRadio > div > label:nth-child(1)::before {{ background-image: url('{ICONS["GPT-4"]}'); }}
    /* 2. Claude */
    .stRadio > div > label:nth-child(2)::before {{ background-image: url('{ICONS["Claude"]}'); }}
    /* 3. Gemini */
    .stRadio > div > label:nth-child(3)::before {{ background-image: url('{ICONS["Gemini"]}'); }}
    /* 4. Llama */
    .stRadio > div > label:nth-child(4)::before {{ background-image: url('{ICONS["Llama"]}'); }}
    /* 5. General */
    .stRadio > div > label:nth-child(5)::before {{ background-image: url('{ICONS["General"]}'); opacity: 0.5; }}


    /* -------------------------------------------------------
       GENERATE BUTTON
       ------------------------------------------------------- */
    .stButton button {{
        background: linear-gradient(90deg, #8B5CF6 0%, #A78BFA 100%) !important;
        color: white !important;
        border: none !important;
        padding: 15px 30px !important;
        border-radius: 12px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        width: 100% !important;
        margin-top: 20px !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
    }}
    .stButton button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4) !important;
    }}

    /* -------------------------------------------------------
       RESULT CARDS
       ------------------------------------------------------- */
    .result-card {{
        background: white;
        border-radius: 16px;
        border: 1px solid #E5E7EB;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s;
    }}
    .best-match {{
        border: 2px solid #8B5CF6;
        position: relative;
    }}
    .best-badge {{
        position: absolute;
        top: -12px;
        left: 20px;
        background: #8B5CF6;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
    }}
    .tag {{
        background: #F3F4F6;
        color: #4B5563;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        float: right;
    }}
    
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. APP LAYOUT
# ---------------------------------------------------------

# Header
st.markdown("""
<div class='header-container'>
    <div class='header-icon'>✨</div>
    <div class='header-title'>PromptCraft AI</div>
    <div class='header-sub'>Transform your ideas into optimized prompts</div>
</div>
""", unsafe_allow_html=True)

# Main Container
with st.container():
    # Input
    st.markdown("<p style='font-weight:600; color:#374151; margin-bottom:5px;'>What do you want to achieve?</p>", unsafe_allow_html=True)
    user_input = st.text_area("input", placeholder="Example: I want to write a blog post about sustainable living...", height=120, label_visibility="collapsed")

    # Model Selection (This renders the Cards)
    st.markdown("<p style='font-weight:600; color:#374151; margin-top:25px; margin-bottom:5px;'>Select your target LLM</p>", unsafe_allow_html=True)
    
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
            st.error("⚠️ Please set your OpenAI API Key in the Settings.")
        elif not user_input:
            st.warning("Please enter a goal first.")
        else:
            client = OpenAI(api_key=api_key)
            
            with st.spinner("Engineering 8 distinct strategies..."):
                try:
                    # Mocking the JSON response structure for stability in this demo
                    # In production, this would come from OpenAI
                    prompt = f"""
                    Act as an expert Prompt Engineer. 
                    Goal: "{user_input}"
                    Model: {model}
                    
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
                    st.write("")
                    
                    # Display Grid
                    c1, c2 = st.columns(2)
                    
                    with c1:
                        # Best Match
                        s = strategies[0]
                        st.markdown(f"""
                        <div class="result-card best-match">
                            <div class="best-badge">★ BEST MATCH</div>
                            <span class="tag" style="background:#F3E8FF; color:#7C3AED;">{s['tag']}</span>
                            <h3 style="margin-top:10px; font-size:18px; color:#111827;">{s['title']}</h3>
                            <p style="color:#6B7280; font-size:14px;">{s['desc']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.code(s['code'], language="markdown")
                        
                        s = strategies[2]
                        st.markdown(f"""
                        <div class="result-card">
                            <span class="tag">{s['tag']}</span>
                            <h3 style="margin-top:0; font-size:18px; color:#111827;">{s['title']}</h3>
                            <p style="color:#6B7280; font-size:14px;">{s['desc']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.code(s['code'], language="markdown")

                    with c2:
                        s = strategies[1]
                        st.markdown(f"""
                        <div class="result-card">
                            <span class="tag">{s['tag']}</span>
                            <h3 style="margin-top:0; font-size:18px; color:#111827;">{s['title']}</h3>
                            <p style="color:#6B7280; font-size:14px;">{s['desc']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.code(s['code'], language="markdown")

                        s = strategies[3]
                        st.markdown(f"""
                        <div class="result-card">
                            <span class="tag">{s['tag']}</span>
                            <h3 style="margin-top:0; font-size:18px; color:#111827;">{s['title']}</h3>
                            <p style="color:#6B7280; font-size:14px;">{s['desc']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.code(s['code'], language="markdown")

                except Exception as e:
                    st.error(f"Error: {e}")
