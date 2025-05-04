import streamlit as st
import pandas as pd
import random

# ---- Page Setup ----
st.set_page_config(page_title="Fraud Risk Investigator", layout="wide")
st.title("🛡️ Fraud Risk Investigator (MVP)")

st.markdown("""
This module simulates fraud detection using enriched ISO 20022 fields.
Each transaction is assessed against **FATF red flags**, **OpenSanctions**, and **Swift data quality** checks.
""")

# ---- Dummy Data ----
data = [
    {
        "Transaction ID": f"TXN{1000+i}",
        "Amount": round(random.uniform(5000, 500000), 2),
        "Currency": "USD",
        "Debtor": random.choice(["ACME Corp", "Global Exports", "Unknown Entity", "Midland Ltd"]),
        "Creditor": random.choice(["SafeBank", "XYZ Bank", "Iran Financial Org", "ABC Corp"]),
        "Country": random.choice(["IR", "US", "RU", "SG", "IN", "CN"]),
        "Purpose Code": random.choice(["SALA", "GDSV", "INTE", "CASH", "TAXS"]),
        "LEI": random.choice(["", "5493001KJTIIGC8Y1R12"]),
        "Sanction Match": random.choice([True, False, False]),
    }
    for i in range(50)
]

df = pd.DataFrame(data)

# ---- Forensic Summary Builder ----
def get_summary(row):
    reasons = []
    sources = []

    if row["Country"] in ["IR", "RU", "CN"]:
        reasons.append("Country is on FATF grey/black list")
        sources.append("FATF")

    if row["Purpose Code"] == "CASH":
        reasons.append("Unusual purpose code (CASH) for cross-border payment")
        sources.append("Swift Guidelines")

    if not row["LEI"]:
        reasons.append("Missing LEI for corporate sender")
        sources.append("Swift Data Quality")

    if row["Sanction Match"] and "Iran" in row["Creditor"]:
        reasons.append("Creditor flagged in OpenSanctions")
        sources.append("OpenSanctions")

    if row["Amount"] > 250000:
        reasons.append("High-value transaction requiring additional scrutiny")
        sources.append("FATF")

    if not reasons:
        return "✅ No fraud indicators detected", []

    return f"❌ Flagged for: {', '.join(reasons)}", list(set(sources))

# ---- Generate Summary and Sources ----
df["Risk Summary"], df["Sources"] = zip(*df.apply(get_summary, axis=1))

# ---- Display Table with Click to Expand ----
st.markdown("### 📋 Transactions Overview")
st.dataframe(df[["Transaction ID", "Amount", "Currency", "Debtor", "Creditor", "Country", "Purpose Code", "LEI", "Sanction Match"]])

selected_txn = st.selectbox("🔍 Select a Transaction to Investigate:", df["Transaction ID"].tolist())

if selected_txn:
    selected = df[df["Transaction ID"] == selected_txn].iloc[0]
    st.markdown(f"#### 🔍 Transaction Details: {selected['Transaction ID']}")
    st.markdown(f"💸 Amount: **{selected['Amount']} {selected['Currency']}**")
    st.markdown(f"👤 Debtor: **{selected['Debtor']}**")
    st.markdown(f"🏦 Creditor: **{selected['Creditor']}**")
    st.markdown(f"🌍 Country: **{selected['Country']}**")
    st.markdown(f"📄 Purpose Code: **{selected['Purpose Code']}**")
    st.markdown(f"🔗 LEI: **{selected['LEI'] or 'Missing'}**")
    st.markdown(f"🚨 Sanction Match: **{'Yes' if selected['Sanction Match'] else 'No'}**")
    st.info(f"{selected['Risk Summary']}")
    if selected['Sources']:
        st.warning(f"📚 Flagged against: {', '.join(selected['Sources'])}")
