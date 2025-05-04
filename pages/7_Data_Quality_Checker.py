import streamlit as st
import pandas as pd
import random

# --- Page Config ---
st.set_page_config(page_title="ISO 20022 Data Quality Checker", layout="wide")
st.title("ISO 20022 Data Quality Checker")

st.markdown("""
This module is designed for **corporates** to assess and improve the quality of their ISO 20022 payment initiation data.  
It helps drive **Straight-Through Processing (STP)**, reduce **payment friction**, and enable the use of **rich structured data** in `pacs.008` messages — all critical for ISO 20022 compliance and operational excellence.
""")

# --- Dummy Data Generator ---
def generate_dummy_payments(num_messages=100):
    fields = {
        "Debtor Name": ["ABC Corp", "XYZ Ltd", "Global Inc"],
        "Debtor LEI": ["529900T8BM49AURSDO55", "", "875300T3KM43AURXYZ99"],
        "Debtor BIC": ["HDFCINBBXXX", "", "SBININBB123"],
        "Purpose Code": ["SALA", "", "CASH"],
        "Remittance Info": ["Invoice #123", "", "PO #45678"]
    }

    address_options = [
        "Hybrid Address: <AdrLine>#18-16 Leicester Road</AdrLine>",
        "Fully Structured Address: <StrtNm>Leicester Road</StrtNm> <BldgNb>18-16</BldgNb> <TwnNm>Singapore</TwnNm>",
        ""
    ]

    data = []
    for i in range(num_messages):
        row = {"Message ID": f"MSG{i+1:04d}"}
        valid_count = 0
        for field, options in fields.items():
            value = random.choice(options)
            row[field] = value
            if value:
                valid_count += 1

        # Postal Address separately
        postal_value = random.choice(address_options)
        row["Postal Address"] = postal_value
        if postal_value:
            valid_count += 1

        row["Quality Score"] = round((valid_count / 6) * 100, 2)  # 6 fields
        data.append(row)

    return pd.DataFrame(data)

# --- Generate Data ---
df = generate_dummy_payments()

# --- Filter UI ---
st.subheader("Filter Messages")
filter_option = st.radio("Select messages to view", ["All", "Correct Only", "Incorrect Only"])

if filter_option == "Correct Only":
    display_df = df[df["Quality Score"] == 100]
elif filter_option == "Incorrect Only":
    display_df = df[df["Quality Score"] < 100]
else:
    display_df = df.copy()

# --- Summary Metrics ---
st.subheader("Summary Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total", df.shape[0])
col2.metric("Fully Valid", df[df["Quality Score"] == 100].shape[0])
col3.metric("Partially Valid", df[(df["Quality Score"] < 100) & (df["Quality Score"] > 0)].shape[0])
col4.metric("Fully Invalid", df[df["Quality Score"] == 0].shape[0])

# --- Highlight Style for Missing ---
def highlight_missing(val):
    if val == "":
        return 'background-color: #ffd6d6'  # soft red for missing
    return ''

# --- Two Panel Layout ---
st.subheader("Messages")
left, right = st.columns([2, 1])

with left:
    st.markdown("#### Message Table (Red = Missing Field)")
    styled_df = display_df.drop(columns=["Quality Score"]).set_index("Message ID").style.applymap(highlight_missing)
    st.dataframe(styled_df, use_container_width=True)

with right:
    st.markdown("#### Selected Message")
    selected_msg = st.selectbox("Choose a Message ID", display_df["Message ID"].tolist())
    selected_row = df[df["Message ID"] == selected_msg].iloc[0]

    st.markdown(f"**Message ID:** `{selected_msg}`")
    st.markdown(f"**Quality Score:** `{selected_row['Quality Score']}%`")
    st.markdown("---")
    st.markdown("**Field Values:**")

    for field in df.columns[1:-1]:  # skip Message ID and Quality Score
        val = selected_row[field]
        if val == "":
            st.markdown(f"- **{field}**: ❌ *Missing*")
        else:
            st.markdown(f"- **{field}**: `{val}`")

# --- Footer ---
st.markdown("---")
st.markdown("Developed as part of **PaymentLabs.AI** | © 2025")
