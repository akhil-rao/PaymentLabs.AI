import streamlit as st
import pandas as pd
import uuid
from datetime import datetime

# Sample MT103 (read-only) derived from provided pacs.008
mt103_data = {
    ":20:": "wS4",
    ":23B:": "CRED",
    ":32A:": "230524USD4001,",
    ":50F:": "1/ABC\n2/Leicester Road,18 16\n3/Singapore,358828",
    ":52A:": "SBININBB",
    ":57A:": "CITIUS33",
    ":59F:": "1/VOLKSWAGEN AG\n2/Pine Grove,18 02 25\n3/Singapore,597594",
    ":70:": "/ROC/Invoice ref 330///URI/Payment is related to trade shipment from Maersk favouring DP World, Dubai, passing through Osmani Digna Port Su",
    ":71A:": "SHA"
}

# Sample pacs.008 (editable)
initial_pacs008_data = {
    "<EndToEndId>": "Invoice ref 330",
    "<RmtInf>": "Payment is related to trade shipment from Maersk favouring DP World, Dubai, passing through Osmani Digna Port Su",
    "<ChrgBr>": "SHAR",
    "<Purp>": ""
}

editable_fields = ["<RmtInf>", "<ChrgBr>", "<Purp>"]

if "pacs008_data" not in st.session_state:
    st.session_state.pacs008_data = initial_pacs008_data.copy()

if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

st.set_page_config(page_title="Page 14 - MX Mapping and Audit Trail")
st.title("🧾 Page 14: MX Mapping with Audit Trail")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 SWIFT MT103 (View Only)")
    for field, value in mt103_data.items():
        st.text_area(label=field, value=value, disabled=True)

with col2:
    st.subheader("✍️ pacs.008 Message (Editable Fields)")
    for field, value in st.session_state.pacs008_data.items():
        if field in editable_fields:
            new_value = st.text_input(f"{field}", value)
            if new_value != value:
                uetr = str(uuid.uuid4())
                st.session_state.audit_log.append({
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Session ID (UETR)": uetr,
                    "User (Login ID)": "daniel@example.com",
                    "Role": "Analyst",
                    "Field": field,
                    "Source": "MX",
                    "Action Type": "edit",
                    "Old Value": value,
                    "New Value": new_value,
                    "Justification": "Auto-logged from UI edit",
                    "Reverted": "No"
                })
                st.session_state.pacs008_data[field] = new_value
        else:
            st.text_input(f"{field}", value, disabled=True)

st.markdown("---")
if st.button("📜 View Audit Trail"):
    st.subheader("🔍 Audit Trail Log")
    audit_df = pd.DataFrame(st.session_state.audit_log)
    st.dataframe(audit_df, use_container_width=True)

# Required packages for this module:
# streamlit
# lxml
# pandas
# matplotlib
# openpyxl
