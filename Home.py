import streamlit as st

# ---- Sidebar Layout ----
with st.sidebar:
    st.markdown("## 🚀 Transact-AI Sandbox")
    st.page_link("Home", label="🏠 Home")
    st.page_link("About", label="ℹ️ About")
    
    st.markdown("---")
    st.markdown("### 🛠 Available Modules")
    st.page_link("pages/1_Swift_CBPR+_Structured_Payment_Copilot.py", label="🔷 Swift CBPR+ Payment Copilot")

    st.markdown("---")
    st.markdown("### 🧪 Upcoming AI Agents")
    st.page_link("pages/2_Sanctions_Follow_Up.py", label="🛡️ Sanctions Follow-Up Agent")
    st.page_link("pages/3_AI_Reconciliation.py", label="🔄 AI Reconciliation Assistant")
    st.page_link("pages/4_Payment_Investigations.py", label="🕵️‍♂️ Payment Investigations Agent")
    st.page_link("pages/5_Liquidity_Management.py", label="💧 Liquidity Management Copilot")
    st.page_link("pages/6_Compliance_Reporter.py", label="📋 Compliance Reporter Agent")
    st.page_link("pages/7_Data_Quality_Checker.py", label="🧹 Payment Data Quality Checker")
    st.page_link("pages/8_CrossBorder_Cost_Predictor.py", label="🌍 Cross-Border Cost Predictor")
    st.page_link("pages/9_Fraud_Risk_Investigator.py", label="🛡️ Fraud Risk Investigator")

st.set_page_config(page_title="Transact-AI Sandbox", layout="wide")
st.title("🚀 Welcome to Transact-AI Sandbox")

# --- Home Page Content ---
st.markdown("""
Welcome to **Transact-AI Sandbox** — a next-generation platform where AI meets ISO 20022 structured data to transform payment operations.

---

### 🧩 Available Modules:
- 🔷 **Swift CBPR+ Structured Payment Copilot** — Clean, enrich and validate payment XMLs.
- 🛡️ **Sanctions Follow-Up Agent** *(Coming Soon)*
- 🔄 **AI Reconciliation Assistant** *(Coming Soon)*
- 🕵️‍♂️ **Payment Investigations Agent** *(Coming Soon)*
- 💧 **Liquidity Management Copilot** *(Coming Soon)*
- 📋 **Compliance Reporter Agent** *(Coming Soon)*
- 🧹 **Payment Data Quality Checker** *(Coming Soon)*
- 🌍 **Cross-Border Cost Predictor** *(Coming Soon)*
- 🛡️ **Fraud Risk Investigator** *(Coming Soon)*

---
""")

st.success("Use the sidebar to explore available modules and upcoming innovations!")
