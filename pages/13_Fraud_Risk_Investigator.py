import streamlit as st
import pandas as pd
import random

# ---- Page Config ----
st.set_page_config(page_title="Fraud Risk Investigator", layout="wide")
st.title("🛡️ Fraud Risk Investigator")

st.markdown("""
This simulator uses structured ISO 20022 data fields like **LEI**, **BIC**, **Purpose Codes**, and **Remittance Keywords** to simulate fraud detection.

It flags suspicious transactions based on:
- High-risk jurisdictions
- Presence of crypto-related keywords
- Missing or mismatched party identifiers
- FATF and Travel Rule risk patterns

---
""")

# ---- Generate Dummy Data ----
random.seed(42)

countries = ['US', 'UK', 'DE', 'SG', 'IN', 'NG', 'RU']  # Nigeria and Russia as high-risk
purposes = ['SALA', 'TAXS', 'CASH', 'INTC', 'GDSV', 'SCVE']
remittance_keywords = ['Invoice 123', 'Payment for services', 'crypto wallet', 'Consulting Fee', 'Loan Settlement', 'ICO transfer']
bics = ['BOFAUS3N', 'DEUTDEFF', 'SCBLINBB', 'NATAGB2L', 'CBNINGS1', 'VTBRRUMM']
leis = ['5493001KJTIIGC8Y1R12', '213800D1EI4B9WTWWD28', '724500PMK9IGKBC9G407', '', '213800LUZ6AO6YJ36V04']

risk_flags = []
data = []

for i in range(100):
    country = random.choice(countries)
    bic = random.choice(bics)
    lei = random.choice(leis)
    purpose = random.choice(purposes)
    rem = random.choice(remittance_keywords)

    risk = []
    if 'crypto' in rem.lower() or 'ico' in rem.lower():
        risk.append("🔴 Crypto-related keyword")
    if country in ['NG', 'RU']:
        risk.append(f"🟠 High-risk country ({country})")
    if lei == '':
        risk.append("🟡 Missing LEI")
    if purpose == 'CASH':
        risk.append("🟠 High-risk purpose (CASH)")

    risk_flags.append(", ".join(risk) if risk else "✅ No risk")

    data.append({
        'TransactionID': f'TXN{i+1:03d}',
        'BIC': bic,
        'LEI': lei,
        'PurposeCode': purpose,
        'RemittanceInfo': rem,
        'Country': country,
        'RiskFlags': risk_flags[-1]
    })

# ---- Display Table ----
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

# ---- Filter Tools ----
st.sidebar.header("🔍 Filter")
purpose_filter = st.sidebar.multiselect("Purpose Code", options=purposes)
country_filter = st.sidebar.multiselect("Country", options=countries)
risk_filter = st.sidebar.selectbox("Show Only", options=["All", "Flagged Only", "No Risk Only"])

filtered_df = df.copy()
if purpose_filter:
    filtered_df = filtered_df[filtered_df['PurposeCode'].isin(purpose_filter)]
if country_filter:
    filtered_df = filtered_df[filtered_df['Country'].isin(country_filter)]
if risk_filter == "Flagged Only":
    filtered_df = filtered_df[~filtered_df['RiskFlags'].str.contains("No risk")]
elif risk_filter == "No Risk Only":
    filtered_df = filtered_df[filtered_df['RiskFlags'].str.contains("No risk")]

st.markdown("---")
st.subheader("🧾 Filtered Results")
st.dataframe(filtered_df, use_container_width=True)

# ---- Download Option ----
st.download_button(
    label="📥 Download Filtered Results (CSV)",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name="fraud_risk_investigation_results.csv",
    mime="text/csv"
)
