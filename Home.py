import streamlit as st

# ---- Streamlit Page Setup (MUST BE FIRST!) ----
st.set_page_config(page_title="PaymentLabs.AI Sandbox", layout="wide")

# ---- Force Browser Tab Title (Change title after page config) ----
st.markdown(
    """
    <script>
    var newTitle = "PaymentLabs.AI Sandbox";
    document.title = newTitle;
    </script>
    """,
    unsafe_allow_html=True
)

# ---- Home Page Content ----
st.title("🚀 Welcome to PaymentLabs.AI Sandbox")

st.markdown("""
Welcome to **PaymentLabs.AI Sandbox** — a next-generation workspace where **AI** meets **ISO 20022 structured data** to transform cross-border payment operations.
""")

st.markdown("### 🧩 Available Modules:")

st.success("🔷 **Swift CBPR+ Structured Payment Copilot** — Now LIVE! Repair and enrich Swift CBPR+ payment messages with AI assistance.")
st.success("🔷 **Structured Address Validation** — Now LIVE! Validate and structure postal addresses with zero data loss.")
st.success("🔷 **Advanced Reporting (NLP-Based)** — Now LIVE! Generate smart cross-border payment reports from natural language input.")

st.markdown('---')

st.markdown("### 🧪 Upcoming Smart Agents:")

st.markdown("""
- 🛡️ **Sanctions Follow-Up Agent** *(Coming Soon)*  
- 🔄 **AI Reconciliation Assistant** *(Coming Soon)*  
- 🕵️‍♂️ **Payment Investigations Agent** *(Coming Soon)*  
- 💧 **Liquidity Management Copilot** *(Coming Soon)*  
- 📋 **Compliance Reporter Agent** *(Coming Soon)*  
- 🧹 **Payment Data Quality Checker** *(Coming Soon)*  
- 🌍 **Cross-Border Cost Predictor** *(Coming Soon)*  
- 🛡️ **Fraud Risk Investigator** *(Coming Soon)*
""")

st.markdown("---")

st.success("➡️ Use the sidebar to navigate and explore the live modules!")
