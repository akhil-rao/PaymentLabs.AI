import streamlit as st
import pandas as pd
import random

# --- Page Config ---
st.set_page_config(page_title="ISO 20022 Data Quality Checker", layout="wide")
st.title("ISO 20022 Data Quality Checker")

st.markdown("""
This module simulates ISO 20022 `pacs.008` messages and checks the quality of structured data fields across 100 payment instructions. It highlights:
- Missing or improperly structured fields
- Data quality score per message
- Drill-down view for messages with issues
""")

# --- Generate Dummy Data ---
def generate_dummy_payments(num_messages=100):
    fields = ["Debtor Name", "Debtor LEI", "Debtor BIC", "Postal Address", "Purpose Code", "Remittance Info"]
    data = []

    for i in range(num_messages):
        message = {"Message ID": f"MSG{i+1:04d}"}
        for field in fields:
            message[field] = "Valid" if random.random() < 0.9 else "Missing"
        valid_count = sum(1 for f in fields if message[f] == "Valid")
        message["Quality Score"] = round((valid_count / len(fields)) * 100, 2)
        data.append(message)

    return pd.DataFrame(data)

df = generate_dummy_payments()

# --- Summary ---
st.subheader("Summary Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Messages", df.shape[0])
col2.metric("Fully Valid", df[df["Quality Score"] == 100].shape[0])
col3.metric("Partially Valid", df[(df["Quality Score"] < 100) & (df["Quality Score"] > 0)].shape[0])
col4.metric("Fully Invalid", df[df["Quality Score"] == 0].shape[0])

# --- Filter Toggle ---
st.subheader("Filter Messages")
filter_option = st.radio("Select messages to view", ["All", "Correct Only", "Incorrect Only"])

if filter_option == "Correct Only":
    display_df = df[df["Quality Score"] == 100]
elif filter_option == "Incorrect Only":
    display_df = df[df["Quality Score"] < 100]
else:
    display_df = df.copy()

# --- Two Column Layout for Table + Drill-down ---
st.subheader("Message Field Assessment")
left, right = st.columns([2, 1])

with left:
    selected_msg = st.selectbox("Select a message to view details", display_df["Message ID"].tolist())
    st.dataframe(display_df.set_index("Message ID"), use_container_width=True)

with right:
    st.markdown("### Message Details & Issues")
    msg_details = df[df["Message ID"] == selected_msg].iloc[0]
    issues = {field: msg_details[field] for field in df.columns if field not in ["Message ID", "Quality Score"] and msg_details[field] != "Valid"}

    st.markdown(f"**Message ID:** `{selected_msg}`")
    st.markdown(f"**Quality Score:** `{msg_details['Quality Score']}%`")
    
    if issues:
        st.error("Issues found:")
        for field, value in issues.items():
            st.markdown(f"- **{field}**: `{value}`")
    else:
        st.success("No issues. All fields are valid.")

# --- Footer ---
st.markdown("---")
st.markdown("Developed as part of **PaymentLabs.AI** | © 2025")
