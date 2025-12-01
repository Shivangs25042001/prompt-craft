import streamlit as st
from openai import OpenAI
import json

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="PromptCraft AI", page_icon="✨", layout="wide")

# ---------------------------------------------------------
# 2. THE DESIGN SYSTEM (CSS)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Import Font */
    @import url('[https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap](https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap)');
    
    .stApp {
        background-color: #FAFAFA;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Default Header/Footer */
    header, footer {visibility: hidden;}
    
    /* Center the Main Logo */
    .main-header {
        text-align: center; 
        padding-top: 40px; 
        padding-bottom: 40px;
    }
    
    /* Input Box Styling */
    .stTextArea textarea {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 20px;
        font-size: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .stTextArea textarea:focus {
        border-color: #8B5CF6;
        box-shadow: 0 0 0 4px #F3E8FF;
    }

    /* -------------------------------------------------------
       CUSTOM RADIO BUTTONS -> TRANSFORMED INTO CARDS
       ------------------------------------------------------- */
    
    /* 1. Container Layout */
    .stRadio > div {
        display: flex;
        justify-content: center;
        gap: 20px;
        width: 100%;
        overflow-x: auto;
        padding-bottom: 10px;
    }

    /* 2. The Card (Label) Style */
    .stRadio > div > label {
        background-color: #FFFFFF !important;
        border: 2px solid #E5E7EB !important;
        border-radius: 16px !important;
        width: 160px !important;
        height: 140px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: flex-end !important;
        padding-bottom: 20px !important;
        cursor: pointer !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
        transition: all 0.2s ease !important;
        position: relative;
    }

    /* 3. Hover Effect */
    .stRadio > div > label:hover {
        border-color: #C4B5FD !important;
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.05) !important;
    }

    /* 4. Selected State (Purple Border) */
    .stRadio > div > label[data-baseweb="radio"] {
        background-color: #F5F3FF !important;
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 4px #DDD6FE !important;
    }

    /* 5. Hide the actual little circle */
    .stRadio div[role="radio"] {
        display: none !important;
    }

    /* 6. Text Styling */
    .stRadio p {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #374151 !important;
    }

    /* -------------------------------------------------------
       INJECTING LOGOS via CSS BACKGROUNDS
       ------------------------------------------------------- */
    /* This trick puts the image inside the card before the text */
    
    .stRadio > div > label::before {
        content: "";
        position: absolute;
        top: 25px;
        width: 50px;
        height: 50px;
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
    }

    /* GPT-4 Logo */
    .stRadio > div > label:nth-child(1)::before {
        background-image: url('[https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg](https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg)');
    }
    /* Claude Logo */
    .stRadio > div > label:nth-child(2)::before {
        background-image: url('[https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Anthropic.svg/1024px-Anthropic.svg.png](https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Anthropic.svg/1024px-Anthropic.svg.png)');
    }
    /* Gemini Logo */
    .stRadio > div > label:nth-child(3)::before {
        background-image: url('[https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg](https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg)');
    }
    /* Llama Logo */
    .stRadio > div > label:nth-child(4)::before {
        background-image: url('[https://cdn.icon-icons.com/icons2/4222/PNG/512/meta_logo_icon_262793.png](https://cdn.icon-icons.com/icons2/4222/PNG/512/meta_logo_icon_262793.png)');
    }
    /* General Logo */
    .stRadio > div > label:nth-child(5)::before {
        background-image: url('[https://cdn-icons-png.flaticon.com/512/3524/3524335.png](https://cdn-icons-png.flaticon.com/512/3524/3524335.png)');
        opacity: 0.5;
    }

    /* -------------------------------------------------------
       GENERATE BUTTON
       ------------------------------------------------------- */
    .stButton button {
        background: linear-gradient(90deg, #8B5CF6 0%, #7C3AED 100%) !important;
        color: white !important;
        border: none !important;
        padding: 16px !important;
        border-radius: 12px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        width: 100% !important;
        margin-top: 30px !important;
        transition: transform 0.2s !important;
    }
    .stButton button:hover {
        transform: scale(1.01) !important;
        box-shadow: 0 10px 20px rgba(139, 92, 246, 0.3) !important;
    }

    /* RESULT CARDS */
    .result-box {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .best-box {
        border: 2px solid #8B5CF6;
        background: linear-gradient(180deg, #FBF8FF 0%, #FFFFFF 100%);
    }
    
    .badge-purple {
        background: #F3E8FF;
        color: #7C3AED;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        float: right;
    }
    
    .badge-gray {
        background: #F3F4F6;
        color: #4B5563;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        float: right;
    }

    .best-match-label {
        position: absolute;
        top: -12px;
        left: 30px;
        background: #8B5CF6;
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 10px rgba(139, 92, 246, 0.3);
    }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. APP STRUCTURE
# ---------------------------------------------------------

# Header
st.markdown("<div class='main-header'><h1>✨ PromptCraft AI</h1><p style='color:#6B7280; font-size:18px;'>Turn your vague ideas into engineered master prompts.</p></div>", unsafe_allow_html=True)

# Input
st.markdown("### What do you want to achieve?")
user_input = st.text_area("label", placeholder="e.g. I want to create a meal plan for a vegan athlete...", height=100, label_visibility="collapsed")

st.write("")
st.markdown("### Select your target LLM")

# THE CARD SELECTOR
# We use st.radio, but the CSS above transforms it into the cards!
model = st.radio(
    "Select Model",
    ["GPT-4", "Claude 3.5", "Gemini", "Llama 3", "General"],
    horizontal=True,
    label_visibility="collapsed"
)

st.write("")

# Generate Button
if st.button("Generate Prompt Variations →"):
    api_key = st.secrets.get("OPENAI_API_KEY")
    
    if not api_key:
        st.error("⚠️ Please add your OpenAI API Key in Settings!")
    elif not user_input:
        st.warning("Please enter a goal first.")
    else:
        client = OpenAI(api_key=api_key)
        
        with st.spinner("Engineering optimized strategies..."):
            try:
                # Prompt Engineering Logic
                system_prompt = f"""
                You are a world-class Prompt Engineer. 
                Goal: "{user_input}"
                Model: {model}
                
                Generate 4 distinct strategies in valid JSON format:
                {{
                    "strategies": [
                        {{
                            "title": "Chain of Thought", 
                            "tag": "Reasoning",
                            "desc": "Forces step-by-step logic.",
                            "prompt": "..."
                        }},
                        ... (Role-Based, Structured, Few-Shot)
                    ]
                }}
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "Return JSON only."}, {"role": "user", "content": system_prompt}],
                    response_format={"type": "json_object"}
                )
                
                data = json.loads(response.choices[0].message.content)
                strategies = data.get("strategies", [])
                
                st.write("")
                st.markdown("<h2 style='text-align: center; margin: 40px 0;'>✨ Optimized Strategies</h2>", unsafe_allow_html=True)
                
                # GRID LAYOUT FOR RESULTS
                c1, c2 = st.columns(2)
                
                with c1:
                    # Strategy 1
                    s = strategies[0]
                    st.markdown(f"""
                    <div class="result-box best-box">
                        <div class="best-match-label">★ BEST MATCH</div>
                        <span class="badge-purple">{s['tag']}</span>
                        <h3 style="margin-top:15px; color:#1F2937;">{s['title']}</h3>
                        <p style="color:#6B7280; font-size:15px;">{s['desc']}</p>
                    </div>
                    , unsafe_allow_html=True)
                    st.code(s['prompt'], language="markdown")
                    
                    # Strategy 3
                    if len(strategies) > 2:
                        s = strategies[2]
                        st.markdown(f"""
                        <div class="result-box">
                            <span class="badge-gray">{s['tag']}</span>
                            <h3 style="margin-top:0; color:#1F2937;">{s['title']}</h3>
                            <p style="color:#6B7280; font-size:15px;">{s['desc']}</p>
                        </div>
                        , unsafe_allow_html=True)
                        st.code(s['prompt'], language="markdown")

                with c2:
                    # Strategy 2
                    s = strategies[1]
                    st.markdown(f"""
                    <div class="result-box">
                        <span class="badge-gray">{s['tag']}</span>
                        <h3 style="margin-top:0; color:#1F2937;">{s['title']}</h3>
                        <p style="color:#6B7280; font-size:15px;">{s['desc']}</p>
                    </div>
                    , unsafe_allow_html=True)
                    st.code(s['prompt'], language="markdown")

                    # Strategy 4
                    if len(strategies) > 3:
                        s = strategies[3]
                        st.markdown(f"""
                        <div class="result-box">
                            <span class="badge-gray">{s['tag']}</span>
                            <h3 style="margin-top:0; color:#1F2937;">{s['title']}</h3>
                            <p style="color:#6B7280; font-size:15px;">{s['desc']}</p>
                        </div>
                        , unsafe_allow_html=True)
                        st.code(s['prompt'], language="markdown")

            except Exception as e:
                st.error(f"Error: {e}")
