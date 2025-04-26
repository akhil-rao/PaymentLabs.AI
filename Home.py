import streamlit as st

st.set_page_config(page_title="Transact-AI Sandbox", layout="wide")
st.title("🚀 Welcome to Transact-AI Sandbox")

st.markdown("""
Shaping the Future of Payments with AI-Driven ISO 20022 Structured Intelligence.

Explore our smart assistants below:
""")

st.markdown("""
### 🧩 Available Modules:
- 🛠️ **Swift CBPR+ Structured Payment Copilot** – Fix structure, enrich fields, and Swift CBPR+ compliance.
- 🛡️ **Sanctions Follow-Up Agent** – (Coming Soon)
- 🔄 **AI Reconciliation Assistant** – (Coming Soon)
- 🕵️‍♂️ **Payment Investigations Agent** – (Coming Soon)
- 💧 **Liquidity Management Copilot** – (Coming Soon)
- 📋 **Compliance Reporting Agent** – (Coming Soon)
- 🧹 **Payment Data Quality Checker** – (Coming Soon)
- 🌍 **Cross-Border Cost Predictor** – (Coming Soon)
- 🛡️ **Fraud Risk Investigator** – (Coming Soon)
""")

st.info("Use the sidebar on the left ➡️ to navigate to each module!")
st.markdown(
    """
    <style>
    /* Hide Streamlit's default footer completely */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .css-cio0dv.ea3mdgi1 {visibility: hidden;}

    /* Custom footer */
    .custom-footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #023d69;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }
    </style>
    <div class="custom-footer">
        🔹 Powered by Transact-AI Sandbox 🔹
    </div>
    """,
    unsafe_allow_html=True
)
