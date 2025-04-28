import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import io

# ---- Streamlit Page Setup ----
st.set_page_config(page_title="Advanced Reporting (NLP-Based)", layout="wide")
st.title("📊 Advanced Reporting (NLP-Based)")

# ---- Dummy Swift CBPR+ Data ----
random.seed(42)  # for consistency
currencies = ['USD', 'EUR', 'GBP', 'SGD']
purposes = ['SALA', 'SUPP', 'INTC']
countries = ['CA', 'FR', 'IN', 'HK', 'MY', 'AE', 'DE', 'SG']

data = {
    "SettlementDate": pd.date_range(start="2025-04-01", periods=50, freq='D'),
    "TxnRef": [f"TRX{str(i).zfill(3)}" for i in range(1, 51)],
    "InstdAmt": [random.randint(4000, 20000) for _ in range(50)],
    "Ccy": [random.choice(currencies) for _ in range(50)],
    "DbtrNm": [f"Debtor {i}" for i in range(1, 51)],
    "DbtrAcct": [f"DBTRACCT{i}" for i in range(1, 51)],
    "CdtrNm": [f"Creditor {i}" for i in range(1, 51)],
    "CdtrAcct": [f"CDTRACCT{i}" for i in range(1, 51)],
    "CdtrCountry": [random.choice(countries) for _ in range(50)],
    "PurposeCode": [random.choice(purposes) for _ in range(50)]
}

df = pd.DataFrame(data)

# ---- User Inputs ----
st.markdown("### ✍️ Enter Your Report Request")
user_query = st.text_area(
    "Example: 'Show me number of payments to Canada with purpose code SALA'",
    height=150
)

st.markdown("### 🗂️ Select Output Format")
output_format = st.radio(
    "Choose output format:",
    ("Chart Only", "Excel Download"),
    index=0
)

# ---- Basic NLP Parsing Function ----
def parse_nlp_query(query, df):
    query = query.lower()
    filtered_df = df.copy()

    # Country matching
    countries_map = {
        "canada": "CA",
        "france": "FR",
        "india": "IN",
        "hong kong": "HK",
        "malaysia": "MY",
        "uae": "AE",
        "germany": "DE",
        "singapore": "SG"
    }
    for name, code in countries_map.items():
        if name in query:
            filtered_df = filtered_df[filtered_df["CdtrCountry"] == code]
            break

    # Purpose matching
    purposes_map = {
        "salaries": "SALA",
        "salary": "SALA",
        "supplier": "SUPP",
        "supplies": "SUPP",
        "internal": "INTC",
        "intercompany": "INTC"
    }
    for keyword, purpose_code in purposes_map.items():
        if keyword in query:
            filtered_df = filtered_df[filtered_df["PurposeCode"] == purpose_code]
            break

    # Report type
    if "amount" in query or "volume" in query:
        report_type = "amount"
    elif "count" in query or "number of payments" in query:
        report_type = "count"
    else:
        report_type = "general"

    return filtered_df, report_type

# ---- Report Generation Section ----
if st.button("🚀 Generate Report"):
    if not user_query.strip():
        st.warning("⚠️ Please enter a report description.")
    else:
        filtered_df, report_type = parse_nlp_query(user_query, df)

        if filtered_df.empty:
            st.error("❌ No matching data found for your query.")
        else:
            st.success(f"✅ {len(filtered_df)} matching transactions found!")

            if output_format == "Chart Only":
                st.markdown("### 📈 Chart View")

                if report_type == "amount":
                    grouped = filtered_df.groupby("CdtrCountry")["InstdAmt"].sum()
                    st.bar_chart(grouped)
                elif report_type == "count":
                    grouped = filtered_df.groupby("CdtrCountry")["TxnRef"].count()
                    st.bar_chart(grouped)
                else:
                    st.dataframe(filtered_df)

            elif output_format == "Excel Download":
                st.markdown("### 📄 Excel Download")
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    filtered_df.to_excel(writer, index=False, sheet_name='Report')
                st.download_button(
                    label="⬇️ Download Report Excel",
                    data=output.getvalue(),
                    file_name="generated_report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
