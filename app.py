import streamlit as st
from openai import OpenAI
import json

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="PromptCraft AI", page_icon="✨", layout="wide")

# ---------------------------------------------------------
# 2. CSS STYLING (The Design System)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    .stApp {
        background-color: #FAFAFA;
        font-family: 'Inter', sans-serif;
    }
    
    /* Remove top padding */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 5rem;
    }
    
    /* Hide Default Elements */
    header, footer {visibility: hidden;}

    /* -------------------------------------------------------
       CUSTOM COMPONENT STYLES
       ------------------------------------------------------- */
    
    /* INPUT BOX */
    .stTextArea textarea {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 20px;
        font-size: 16px;
        color: #1F2937;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .stTextArea textarea:focus {
        border-color: #8B5CF6;
        box-shadow: 0 0 0 4px #F3E8FF;
    }
    .stTextArea label {
        color: #111827 !important;
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 10px;
    }

    /* MODEL SELECTION CARDS */
    /* This creates the white box look */
    div.stButton > button {
        background-color: #FFFFFF;
        border: 2px solid #E5E7EB;
        border-radius: 16px;
        color: #374151;
        font-weight: 600;
        height: 120px;
        width: 100%;
        transition: all 0.2s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }

    /* Hover State */
    div.stButton > button:hover {
        border-color: #C4B5FD;
        transform: translateY(-3px);
        background-color: #FFFFFF;
        color: #8B5CF6;
    }

    /* GENERATE BUTTON (Specific Styling) */
    /* We target the specific 'Generate' button using a custom class we add in Python */
    .primary-btn button {
        background: linear-gradient(90deg, #8B5CF6 0%, #7C3AED 100%) !important;
        color: white !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(139, 92, 246, 0.3) !important;
    }
    .primary-btn button:hover {
        transform: translateY(-2px) !important;
        color: white !important;
    }

    /* RESULT CARDS */
    .result-box {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        position: relative;
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

    /* Highlight Selected Card */
    .selected-card button {
        border-color: #8B5CF6 !important;
        background-color: #F5F3FF !important;
        box-shadow: 0 0 0 4px #DDD6FE !important;
    }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. APP HEADER
# ---------------------------------------------------------
st.markdown("""
    <div style='text-align: center; margin-bottom: 50px;'>
        <div style='font-size: 60px; margin-bottom: 10px;'>✨</div>
        <h1 style='color: #111827; font-size: 42px; margin: 0; font-weight: 900;'>PromptCraft AI</h1>
        <p style='color: #6B7280; font-size: 18px; margin-top: 10px;'>Turn your vague ideas into engineered master prompts.</p>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. STATE MANAGEMENT
# ---------------------------------------------------------
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = "GPT-4"

# ---------------------------------------------------------
# 5. INPUT & SELECTION UI
# ---------------------------------------------------------
st.markdown("##### What do you want to achieve?")
user_input = st.text_area("Label", placeholder="e.g. I want to create a meal plan for a vegan athlete...", height=120, label_visibility="collapsed")

st.write("")
st.markdown("##### Select your target LLM")

# Create 5 Columns for the cards
c1, c2, c3, c4, c5 = st.columns(5)

# Helper function to create a selection card
def model_card(col, name, icon):
    with col:
        # If selected, add a special CSS class container
        if st.session_state.selected_model == name:
            with st.container():
                st.markdown(f'<div class="selected-card">', unsafe_allow_html=True)
                if st.button(f"{icon}  {name}", key=name, use_container_width=True):
                    st.session_state.selected_model = name
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            if st.button(f"{icon}  {name}", key=name, use_container_width=True):
                st.session_state.selected_model = name
                st.rerun()

# Render the cards (Using Emojis as Icons to guarantee stability without file uploads)
model_card(c1, "GPT-4", "🟢")
model_card(c2, "Claude 3.5", "🟠")
model_card(c3, "Gemini", "🔹")
model_card(c4, "Llama 3", "🔵")
model_card(c5, "General", "⚪")

st.write("")
st.write("")

# ---------------------------------------------------------
# 6. GENERATE BUTTON
# ---------------------------------------------------------
# We wrap this in a container to apply the "Primary Button" style
with st.container():
    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
    generate_clicked = st.button("Generate Prompt Variations →", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if generate_clicked:
    api_key = st.secrets.get("OPENAI_API_KEY")
    
    if not api_key:
        st.error("⚠️ Please add your OpenAI API Key in Settings!")
    elif not user_input:
        st.warning("Please enter a goal first.")
    else:
        client = OpenAI(api_key=api_key)
        
        with st.spinner(f"Engineering prompts for {st.session_state.selected_model}..."):
            try:
                # System Prompt
                system_prompt = f"""
                You are a world-class Prompt Engineer. 
                Goal: "{user_input}"
                Model: {st.session_state.selected_model}
                
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
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "Return JSON only."}, {"role": "user", "content": system_prompt}],
                    response_format={"type": "json_object"}
                )
                
                data = json.loads(response.choices[0].message.content)
                strategies = data.get("strategies", [])
                
                st.write("")
                st.markdown("---")
                st.markdown("<h2 style='text-align: center; margin: 40px 0;'>✨ Optimized Strategies</h2>", unsafe_allow_html=True)
                
                # GRID LAYOUT FOR RESULTS
                col1, col2 = st.columns(2)
                
                with col1:
                    # Strategy 1 (Best Match)
                    s = strategies[0]
                    st.markdown(f"""
                    <div class="result-box best-box">
                        <div class="best-match-label">★ BEST MATCH</div>
                        <span class="badge-purple">{s['tag']}</span>
                        <h3 style="margin-top:15px; color:#1F2937;">{s['title']}</h3>
                        <p style="color:#6B7280; font-size:15px;">{s['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.code(s['prompt'], language="markdown")
                    
                    # Strategy 3
                    if len(strategies) > 2:
                        s = strategies[2]
                        st.markdown(f"""
                        <div class="result-box">
                            <span class="badge-purple" style="background:#F3F4F6; color:#4B5563;">{s['tag']}</span>
                            <h3 style="margin-top:0; color:#1F2937;">{s['title']}</h3>
                            <p style="color:#6B7280; font-size:15px;">{s['desc']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.code(s['prompt'], language="markdown")

                with col2:
                    # Strategy 2
                    s = strategies[1]
                    st.markdown(f"""
                    <div class="result-box">
                        <span class="badge-purple" style="background:#F3F4F6; color:#4B5563;">{s['tag']}</span>
                        <h3 style="margin-top:0; color:#1F2937;">{s['title']}</h3>
                        <p style="color:#6B7280; font-size:15px;">{s['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.code(s['prompt'], language="markdown")

                    # Strategy 4
                    if len(strategies) > 3:
                        s = strategies[3]
                        st.markdown(f"""
                        <div class="result-box">
                            <span class="badge-purple" style="background:#F3F4F6; color:#4B5563;">{s['tag']}</span>
                            <h3 style="margin-top:0; color:#1F2937;">{s['title']}</h3>
                            <p style="color:#6B7280; font-size:15px;">{s['desc']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.code(s['prompt'], language="markdown")

            except Exception as e:
                st.error(f"Error: {e}")
```

**4. Create a `requirements.txt` file** in the same folder with this content:
```text
streamlit
openai
```

---

### **Phase 2: Deploy on Streamlit Cloud (The Free & Easy Way)**

We are abandoning Hugging Face because it makes file management too hard for this specific design. Streamlit Cloud is built for this.

**Step 1: Upload to GitHub**
1.  Go to [GitHub.com](https://github.com/) and sign up (Free).
2.  Click the **+** (top right) -> **New Repository**.
3.  Name it `prompt-craft`.
4.  Click **Create Repository**.
5.  Click the link that says **"uploading an existing file"**.
6.  Drag and drop your `app.py` and `requirements.txt`.
7.  Click **Commit changes**.

**Step 2: Connect to Streamlit Cloud**
1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Sign in with **GitHub**.
3.  Click **"New App"**.
4.  It will see your `prompt-craft` repository automatically. Select it.
5.  Click **"Deploy!"**.

**Step 3: Add your API Key**
1.  Your app will load and might show an error. This is normal.
2.  Click **"Manage App"** (bottom right).
3.  Click the **three dots** (Settings).
4.  Click **Secrets**.
5.  Paste this:
    ```toml
    OPENAI_API_KEY = "sk-..."
