import streamlit as st
import pandas as pd
import uuid
from datetime import datetime

# Full pacs.008 message mapped from the XML provided
full_pacs008_data = {
    "<InstrId>": "wS4",
    "<EndToEndId>": "Invoice ref 330",
    "<UETR>": "7b1beab5-886c-4a79-828e-c24d1005a401",
    "<IntrBkSttlmAmt Ccy=\"USD\">": "4001",
    "<IntrBkSttlmDt>": "2023-05-24",
    "<ChrgBr>": "SHAR",
    "<InstgAgt><BICFI>": "SBININBBXXX",
    "<InstdAgt><BICFI>": "XBANUS33XXX",
    "<Dbtr><Nm>": "ABC",
    "<Dbtr><PstlAdr1>": "2/Leicester Road,18 16",
    "<Dbtr><PstlAdr2>": "3/Singapore,358828",
    "<DbtrAcct><Id>": "NL63ABNA1234567890",
    "<DbtrAgt><BICFI>": "SBININBB",
    "<CdtrAgt><BICFI>": "CITIUS33",
    "<Cdtr><Nm>": "VOLKSWAGEN AG",
    "<Cdtr><PstlAdr1>": "2/Pine Grove,18 02 25",
    "<Cdtr><PstlAdr2>": "3/Singapore,597594",
    "<CdtrAcct><Id>": "919428058523484491",
    "<RmtInf><Ustrd>": "Payment is related to trade shipment from Maersk favouring DP World, Dubai, passing through Osmani Digna Port Su",
    "<Purp>": ""
}

# Full MT103 equivalent (read-only)
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

# Define editable fields (only safe-to-edit)
editable_fields = ["<RmtInf><Ustrd>", "<ChrgBr>", "<Purp>"]

if "pacs008_data" not in st.session_state:
    st.session_state.pacs008_data = full_pacs008_data.copy()

if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

st.set_page_config(page_title="MT-MX Edit Window")
st.title("🧾 MT-MX Edit Window")

st.markdown("---")
col1, col2 = st.columns(2)

# Display full MT103 (read-only)
with col1:
    st.subheader("📄 Full SWIFT MT103 (Read-only)")
    for field, value in mt103_data.items():
        st.markdown(f"**{field}**")
        st.text_area("", value, disabled=True)

# Display full pacs.008 with editable fields
with col2:
    st.subheader("✍️ Full pacs.008 (Editable Fields Highlighted)")
    for field, value in st.session_state.pacs008_data.items():
        if field in editable_fields:
            st.markdown(f"<span style='color:green;font-weight:bold'>{field}</span>", unsafe_allow_html=True)
            new_value = st.text_input("", value, key=field)
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
            st.markdown(f"**{field}**")
            st.text_input("", value, key=field, disabled=True)

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
