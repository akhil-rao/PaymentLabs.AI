import streamlit as st
import pandas as pd
import random

# ---- Page Config ----
st.set_page_config(page_title="Fraud Risk Investigator", layout="wide")
st.title("🛡️ Fraud Risk Investigator")

st.markdown("""
This module simulates fraud risk detection using ISO 20022 structured fields (BIC, LEI, country, purpose) and known red flags from FATF, FinCEN, and OpenSanctions guidelines.
""")

# ---- Generate Dummy Data ----
random.seed(42)

countries = ['US', 'GB', 'DE', 'SG', 'IN', 'CN', 'AE', 'RU', 'IR', 'KP', 'SY']
purpose_codes = ['SALA', 'SUPP', 'TAXS', 'GDSV', 'INVS', 'DIVD', 'GIFT', 'CHAR']
currencies = ['USD', 'EUR', 'GBP', 'SGD', 'INR', 'CNY', 'AED']
bics = ['BOFAUS3N', 'DEUTDEFF', 'HSBCGB2L', 'DBSSSGSG', 'ICICINBB', 'NBADAEAAXXX']
leis = ['5493001KJTIIGC8Y1R12', '213800D1EI4B9WTWWD28', '529900T8BM49AURSDO55', '7245009RSUFTN6UBGF94']
risky_keywords = ['crypto', 'weapons', 'offshore', 'shell']

data = []
for i in range(100):
    country = random.choice(countries)
    purpose = random.choice(purpose_codes)
    currency = random.choice(currencies)
    amount = round(random.uniform(1000, 100000), 2)
    remittance = random.choice(['Invoice Payment', 'Salary Payment', 'Consulting Fee', 'Loan Repayment', 'Gift', 'Donation', 'crypto investment', 'weapons deal', 'offshore transfer', 'shell company funding'])
    bic = random.choice(bics)
    lei = random.choice(leis)
    risk = 'Low'
    if country in ['IR', 'KP', 'SY', 'RU'] or any(keyword in remittance.lower() for keyword in risky_keywords):
        risk = 'High'
    data.append({
        'TransactionID': f'TXN{i+1:03d}',
        'DebtorBIC': bic,
        'DebtorLEI': lei,
        'Country': country,
        'Currency': currency,
        'Amount': amount,
        'PurposeCode': purpose,
        'RemittanceInfo': remittance,
        'RiskFlag': risk
    })

df = pd.DataFrame(data)

# ---- Sidebar Filters ----
st.sidebar.header("🔍 Filter")
selected_purpose = st.sidebar.multiselect("Purpose Code", options=purpose_codes)
selected_country = st.sidebar.multiselect("Country", options=countries)
risk_filter = st.sidebar.selectbox("Risk Level", options=["All", "High", "Low"])

filtered_df = df.copy()
if selected_purpose:
    filtered_df = filtered_df[filtered_df['PurposeCode'].isin(selected_purpose)]
if selected_country:
    filtered_df = filtered_df[filtered_df['Country'].isin(selected_country)]
if risk_filter != "All":
    filtered_df = filtered_df[filtered_df['RiskFlag'] == risk_filter]

# ---- Display Table ----
st.markdown("### 📋 Transaction Risk Summary")
st.dataframe(filtered_df, use_container_width=True)

# ---- Download Option ----
st.download_button(
    label="📥 Download Filtered Results (CSV)",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name="fraud_risk_investigation_results.csv",
    mime="text/csv"
)
