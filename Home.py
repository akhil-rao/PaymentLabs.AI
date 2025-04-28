import streamlit as st

# ---- Streamlit Page Setup (MUST BE FIRST!) ----
st.set_page_config(page_title="Transact-AI Sandbox", layout="wide")

# ---- Force Browser Tab Title (Change title after page config) ----
st.markdown(
    """
    <script>
    var newTitle = "Transact-AI Sandbox";
    document.title = newTitle;
    </script>
    """,
    unsafe_allow_html=True
)

# ---- Custom CSS Styling ----
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
    }
    .main-title {
        color: #015C92;
        font-size: 36px;
        font-weight: 700;
        text-align: center;
        margin-top: -30px;
    }
    .custom-text {
        color: #023d69;
        font-size: 18px;
    }
    .coming-soon {
        color: #03749c;
        font-size: 16px;
        font-style: italic;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Home Page Content ----
st.markdown('<div class="main-title">🚀 Welcome to Transact-AI Sandbox</div>', unsafe_allow_html=True)

st.markdown("""
<div class="custom-text">
Welcome to <b>Transact-AI Sandbox</b> — a next-generation workspace where <b>AI</b> meets <b>ISO 20022 structured data</b> to transform cross-border payment operations.
</div>
<br>
""", unsafe_allow_html=True)

st.markdown('<div class="custom-text"><h3>🧩 Available Modules:</h3></div>', unsafe_allow_html=True)

st.success("🔷 **Swift CBPR+ Structured Payment Copilot** — Now LIVE! Repair and enrich Swift CBPR+ payment messages with AI assistance.")
st.success("🔷 **Structured Address Validation** — Now LIVE! Validate and structure postal addresses using Nucleus API.")

st.markdown('---', unsafe_allow_html=True)

st.markdown('<div class="custom-text"><h3>🧪 Upcoming Smart Agents:</h3></div>', unsafe_allow_html=True)

st.markdown("""
<div class="custom-text">
- 🛡️ <b>Sanctions Follow-Up Agent</b> <span class="coming-soon">(Coming Soon)</span><br>
- 🔄 <b>AI Reconciliation Assistant</b> <span class="coming-soon">(Coming Soon)</span><br>
- 🕵️‍♂️ <b>Payment Investigations Agent</b> <span class="coming-soon">(Coming Soon)</span><br>
- 💧 <b>Liquidity Management Copilot</b> <span class="coming-soon">(Coming Soon)</span><br>
- 📋 <b>Compliance Reporter Agent</b> <span class="coming-soon">(Coming Soon)</span><br>
- 🧹 <b>Payment Data Quality Checker</b> <span class="coming-soon">(Coming Soon)</span><br>
- 🌍 <b>Cross-Border Cost Predictor</b> <span class="coming-soon">(Coming Soon)</span><br>
- 🛡️ <b>Fraud Risk Investigator</b> <span class="coming-soon">(Coming Soon)</span><br>
</div>
""", unsafe_allow_html=True)

st.markdown("---", unsafe_allow_html=True)

st.success("➡️ Use the sidebar to navigate and explore the live modules!")
