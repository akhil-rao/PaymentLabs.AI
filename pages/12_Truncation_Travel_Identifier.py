import pandas as pd
import xml.etree.ElementTree as ET
import re
import streamlit as st

# Set page title
st.set_page_config(page_title="12_Truncation_Travel_Identifier")
st.title("📍 Truncation & Travel Rule Identifier")

st.markdown("""
Upload a pair of MT103 and translated pacs.008 messages. This module will:
- ✅ Match messages using UETR
- 🔍 Detect truncation in key fields
- 🛡 Check compliance with U.S. Travel Rule
""")

# Upload section
uploaded_mt103 = st.file_uploader("Upload MT103 File (.txt)", type=["txt"])
uploaded_pacs008 = st.file_uploader("Upload pacs.008 XML File (.xml)", type=["xml"])

# Function to extract UETR from MT103 (handles multiple formats)
def extract_uetr_mt103(text):
    patterns = [
        r"\{3:\{121:([A-Za-z0-9\-]+)\}\}",  # {3:{121:UETR}}
        r"\{121:([A-Za-z0-9\-]+)\}",        # {121:UETR}
        r":121:([A-Za-z0-9\-]+)"            # :121:UETR
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return None

# Function to extract UETR and key fields from pacs.008
def extract_fields_pacs008(xml_content):
    try:
        root = ET.fromstring(xml_content)
        ns = {'ns': 'urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08'}
        return {
            "UETR": root.find('.//ns:CdtTrfTxInf/ns:PmtId/ns:UETR', ns).text if root.find('.//ns:CdtTrfTxInf/ns:PmtId/ns:UETR', ns) is not None else None,
            "Debtor Name": root.find('.//ns:Dbtr/ns:Nm', ns).text if root.find('.//ns:Dbtr/ns:Nm', ns) is not None else "",
            "Debtor Address": " ".join([e.text for e in root.findall('.//ns:Dbtr/ns:PstlAdr/ns:AdrLine', ns)]),
            "Creditor Name": root.find('.//ns:Cdtr/ns:Nm', ns).text if root.find('.//ns:Cdtr/ns:Nm', ns) is not None else "",
            "Creditor Address": " ".join([e.text for e in root.findall('.//ns:Cdtr/ns:PstlAdr/ns:AdrLine', ns)])
        }
    except:
        return {}

# Function to detect truncation
def detect_truncation(mt_val, pacs_val, max_len):
    return len(pacs_val) < len(mt_val) and ('+' in mt_val or len(mt_val) > max_len)

# Main logic
if uploaded_mt103 and uploaded_pacs008:
    mt_text = uploaded_mt103.read().decode("utf-8")
    pacs_text = uploaded_pacs008.read().decode("utf-8")

    mt_uetr = extract_uetr_mt103(mt_text)
    pacs_fields = extract_fields_pacs008(pacs_text)

    if mt_uetr and pacs_fields.get("UETR") == mt_uetr:
        st.success(f"✅ Matched UETR: {mt_uetr}")

        # Extract simple 1-line names from MT103
        mt_debtor = re.search(r":50[FK]:.*?\n(.+)", mt_text)
        mt_creditor = re.search(r":59[F]?:.*?\n(.+)", mt_text)
        mt_debtor_val = mt_debtor.group(1).strip() if mt_debtor else ""
        mt_creditor_val = mt_creditor.group(1).strip() if mt_creditor else ""

        comparison = pd.DataFrame([
            {
                "Field": "Debtor Name",
                "MT103": mt_debtor_val,
                "pacs.008": pacs_fields["Debtor Name"],
                "Truncated": detect_truncation(mt_debtor_val, pacs_fields["Debtor Name"], 140)
            },
            {
                "Field": "Creditor Name",
                "MT103": mt_creditor_val,
                "pacs.008": pacs_fields["Creditor Name"],
                "Truncated": detect_truncation(mt_creditor_val, pacs_fields["Creditor Name"], 140)
            }
        ])

        st.subheader("🧠 Truncation Check")
        st.dataframe(comparison)

        st.subheader("🔐 Travel Rule Compliance")
        for field in ["Debtor Name", "Debtor Address", "Creditor Name", "Creditor Address"]:
            value = pacs_fields.get(field, "").strip()
            if value:
                st.success(f"{field}: ✅ Present")
            else:
                st.error(f"{field}: ❌ Missing or Incomplete")

    else:
        st.error("❌ UETRs do not match or could not be extracted.")
else:
    st.info("📥 Please upload both files to begin analysis.")
