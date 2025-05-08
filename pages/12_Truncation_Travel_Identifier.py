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
- 🔍 Detect truncation in **any MT103 field** (based on '+' marker)
- 🛡 Check compliance with U.S. Travel Rule in pacs.008
""")

# Upload files
uploaded_mt103 = st.file_uploader("Upload MT103 File (.txt)", type=["txt"])
uploaded_pacs008 = st.file_uploader("Upload pacs.008 XML File (.xml)", type=["xml"])

# Extract UETR from MT103 (supports multiple formats)
def extract_uetr_mt103(text):
    patterns = [
        r"\{3:\{121:([A-Za-z0-9\-]+)\}\}",
        r"\{121:([A-Za-z0-9\-]+)\}",
        r":121:([A-Za-z0-9\-]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return None

# Extract UETR and Travel Rule fields from pacs.008
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

# MAIN LOGIC
if uploaded_mt103 and uploaded_pacs008:
    mt_text = uploaded_mt103.read().decode("utf-8")
    pacs_text = uploaded_pacs008.read().decode("utf-8")

    mt_uetr = extract_uetr_mt103(mt_text)
    pacs_fields = extract_fields_pacs008(pacs_text)

    if mt_uetr and pacs_fields.get("UETR") == mt_uetr:
        st.success(f"✅ Matched UETR: {mt_uetr}")

        # Extract MT103 Block 4 and split by tags
        st.subheader("🧠 MT103 Truncation Check (based on '+')")

        mt_block4 = re.search(r"\{4:(.*?)-\}", mt_text, re.DOTALL)
        mt_fields = []
        if mt_block4:
            lines = mt_block4.group(1).strip().split('\n')
            current_tag = None
            current_value = ""
            for line in lines:
                tag_match = re.match(r":(\d{2}[A-Z]?):", line)
                if tag_match:
                    if current_tag:
                        mt_fields.append((current_tag, current_value.strip()))
                    current_tag = tag_match.group(1)
                    current_value = line.split(":", 2)[-1].strip()
                else:
                    current_value += " " + line.strip()
            if current_tag:
                mt_fields.append((current_tag, current_value.strip()))

        mt_truncation_df = pd.DataFrame([
            {
                "Field Tag": tag,
                "Value": val,
                "Truncated (ends with '+')": val.endswith('+')
            }
            for tag, val in mt_fields
        ])

        st.dataframe(mt_truncation_df)

        # Travel Rule Check
        st.subheader("🔐 Travel Rule Compliance in pacs.008")
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
