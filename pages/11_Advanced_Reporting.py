import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# ---- Streamlit Page Setup ----
st.set_page_config(page_title="Advanced Reporting (NLP-Based)", layout="wide")
st.title("📊 Advanced Reporting (NLP-Based)")

# ---- Dummy Swift CBPR+ Data ----
data = {
    "SettlementDate": pd.date_range(start="2025-04-01", periods=10, freq='D'),
    "TxnRef": [f"TRX00{i}" for i in range(1, 11)],
    "InstdAmt": [5000, 15000, 7500, 9800, 12300, 6700, 8500, 5400, 10900, 15000],
    "Ccy": ["USD", "EUR", "GBP", "USD", "SGD", "EUR", "GBP", "USD", "SGD", "EUR"],
    "DbtrNm": ["John Doe", "Jane Corp", "Alice Ltd", "Bob LLC", "ZenCorp", "Prime Bank", "Mary Jane", "QuickPay", "EasyCorp", "TrustCo"],
    "DbtrAcct": ["US123", "DE789", "GB321", "US456", "SG123", "FR654", "GB123", "US987", "SG789", "FR321"],
    "CdtrNm": ["ABC Ltd", "XYZ Inc", "FinTech Co", "TradeHub", "TravelEx", "Axis Corp", "Shipping Ltd", "EuroBank", "FinServe", "PaymentsHub"],
    "CdtrAcct": ["CA456", "FR321", "IN654", "HK987", "MY789", "AE321", "SG321", "DE654", "IN123", "AE987"],
    "CdtrCountry": ["CA", "FR", "IN", "HK", "MY", "AE", "SG", "DE", "IN", "AE"],
    "PurposeCode": ["SALA", "SUPP", "INTC", "SALA", "SUPP", "INTC", "SALA", "SUPP", "INTC", "SALA"]
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

    # Filter by Country
    countries = {
        "canada": "CA",
        "france": "FR",
        "india": "IN",
        "hong kong": "HK",
        "malaysia": "MY",
        "uae": "AE",
        "germany": "DE",
        "singapore": "SG"
    }
    for name, code in countries.items():
        if name in query:
            filtered_df = filtered_df[filtered_df["CdtrCountry"] == code]
            break

    # Filter by Purpose
    purposes = {
        "salaries": "SALA",
        "salary": "SALA",
        "supplier": "SUPP",
        "supplies": "SUPP",
        "internal": "INTC",
        "intercompany": "INTC"
    }
    for keyword, purpose_code in purposes.items():
        if keyword in query:
            filtered_df = filtered_df[filtered_df["PurposeCode"] == purpose_code]
            break

    # Detect type of report
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

