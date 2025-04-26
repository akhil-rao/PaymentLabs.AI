import streamlit as st

st.set_page_config(page_title="Transact-AI Sandbox", layout="wide")
st.title("🚀 Welcome to Transact-AI Sandbox")

st.markdown("""
Welcome to **Transact-AI Sandbox** — your AI-powered workspace for intelligent payment operations.

Explore our smart assistants below:
""")

st.markdown("""
### 🧩 Available Modules:
- 🛠️ **Smart Payment Repair Assistant** – Fix structure, enrich fields, and Swift CBPR+ compliance.
- 🛡️ **Sanctions Follow-Up Agent** – (Coming Soon)
- 🔄 **AI Reconciliation Assistant** – (Coming Soon)
- 🕵️‍♂️ **Payment Investigations Agent** – (Coming Soon)
- 💧 **Liquidity Management Copilot** – (Coming Soon)
- 📋 **Compliance Reporter Agent** – (Coming Soon)
- 🧹 **Payment Data Quality Checker** – (Coming Soon)
- 🌍 **Cross-Border Cost Predictor** – (Coming Soon)
- 🛡️ **Fraud Risk Investigator** – (Coming Soon)
""")

st.info("Use the sidebar on the left ➡️ to navigate to each module!")
st.markdown(
    """
    <style>
    footer {
        visibility: hidden;
    }
    footer:after {
        content:'🔹 Powered by Transact-AI Sandbox 🔹'; 
        visibility: visible;
        display: block;
        text-align: center;
        padding: 10px;
        color: white;
        background-color: #023d69;
        position: fixed;
        bottom: 0;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)
