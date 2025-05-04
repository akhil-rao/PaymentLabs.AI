import streamlit as st

# ---- Page Config ----
st.set_page_config(
    page_title="PaymentLabs.AI Sandbox",
    page_icon="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhrg7_v6ZTv0DH9cwycBEk1Sf9_KxYFkBT09c6i_lY2CzSpJHGA-XX4-Jy4Rqm_a0oK3JJohC56DC1N13aAeIvM-7HhHJrfKid4LQee-T_KqYgqWu7LmU5E6GuN9ZIwRW5M1i8v3zoVmT8qbMIH7clJFKeUhEidQ0wTg0nwWxCCEf_f8YhUjrUnav-iCoYx/s1600/PaymentLabsAi_mnemonic.png",
    layout="wide"
)

# ---- Logo in Sidebar (Mnemonic Only) ----
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"]::before {
            content: "";
            display: block;
            margin-left: auto;
            margin-right: auto;
            margin-top: 20px;
            margin-bottom: 20px;
            height: 60px;
            width: 60px;
            background-image: url('https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhrg7_v6ZTv0DH9cwycBEk1Sf9_KxYFkBT09c6i_lY2CzSpJHGA-XX4-Jy4Rqm_a0oK3JJohC56DC1N13aAeIvM-7HhHJrfKid4LQee-T_KqYgqWu7LmU5E6GuN9ZIwRW5M1i8v3zoVmT8qbMIH7clJFKeUhEidQ0wTg0nwWxCCEf_f8YhUjrUnav-iCoYx/s1600/PaymentLabsAi_mnemonic.png');
            background-repeat: no-repeat;
            background-size: contain;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Main Banner Logo ----
st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhEQwVB3xOa8g1-Wzo06ufMf04Cw3IXQA9yzuUXq-OGoXb86tNh0FiLP6MLZWJkKsxnkJK8VemqhnVocrxztBzmjAFFeNH-TsAZ58WynqNRbfKf7w32ExKkRQGmFRSFfKHrsXhLp7bB5Beb9l4B39pi1ggnyyIZVjeTS4sc5J2YibAdhFAGNMYRTlbt_RqE/s16000/PaymentLabsAi_PNG.png' width='300'/>
    </div>
    """,
    unsafe_allow_html=True
)

# ---- Main Content ----
st.markdown("## Welcome to PaymentLabs.AI Sandbox")
st.markdown("A next-generation workspace where **AI** meets **ISO 20022 structured data** to transform cross-border payments.")

st.markdown("### 🧩 Available Modules:")
st.success("🔷 **Swift CBPR+ Structured Payment Copilot** — Now LIVE! Repair and enrich Swift CBPR+ payment messages with AI assistance.")
st.success("🔷 **Structured Address Validation** — Now LIVE! Validate and structure postal addresses with zero data loss.")
st.success("🔷 **Advanced Reporting (NLP-Based)** — Now LIVE! Generate smart cross-border payment reports from natural language input.")
st.success("🔷 **Fraud Risk Investigator** — Now LIVE! Simulate fraud detection using structured ISO 20022 fields and global rules.")

st.markdown("---")
st.markdown("### 🧪 Upcoming Smart Agents:")

st.markdown("""
- 🛡️ **Sanctions Follow-Up Agent** *(Coming Soon)*  
- 🔄 **AI Reconciliation Assistant** *(Coming Soon)*  
- 🕵️‍♂️ **Payment Investigations Agent** *(Coming Soon)*  
- 💧 **Liquidity Management Copilot** *(Coming Soon)*  
- 📋 **Compliance Reporter Agent** *(Coming Soon)*  
- 🧹 **Payment Data Quality Checker** *(Coming Soon)*  
- 🌍 **Cross-Border Cost Predictor** *(Coming Soon)*
""")

st.markdown("---")
st.success("➡️ Use the sidebar to navigate and explore the live modules!")
