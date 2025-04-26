import streamlit as st
import xml.etree.ElementTree as ET
import io

# ---- Helper Functions ----
def parse_xml(xml_string):
    try:
        root = ET.fromstring(xml_string)
        return root
    except ET.ParseError:
        return None

def find_missing_fields(root):
    issues = []
    if root.find(".//PstlAdr") is None:
        issues.append("Missing Debtor Postal Address (PstlAdr)")
    if root.find(".//Purp") is None:
        issues.append("Missing Payment Purpose Code (Purp)")
    return issues

def suggest_fixes(root):
    suggestions = {}
    if root.find(".//PstlAdr") is None:
        suggestions['PstlAdr'] = {
            'StrtNm': 'Main Street',
            'BldgNb': '123',
            'TwnNm': 'Sampletown',
            'Ctry': 'US'
        }
    if root.find(".//Purp") is None:
        suggestions['Purp'] = {
            'Cd': 'GDDS'  # Goods Purchase as example
        }
    return suggestions

def apply_suggestions(root, suggestions):
    dbtr = root.find(".//Dbtr")
    if 'PstlAdr' in suggestions and dbtr is not None:
        pstlAdr = ET.SubElement(dbtr, "PstlAdr")
        for k, v in suggestions['PstlAdr'].items():
            ET.SubElement(pstlAdr, k).text = v
    pmtTpInf = root.find(".//PmtTpInf")
    if pmtTpInf is None:
        pmtTpInf = ET.SubElement(root, "PmtTpInf")
    if 'Purp' in suggestions:
        purp = ET.SubElement(pmtTpInf, "Purp")
        ET.SubElement(purp, "Cd").text = suggestions['Purp']['Cd']
    return root

def prettify_xml(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    return rough_string.decode('utf-8')

# ---- Streamlit App ----
st.set_page_config(page_title="Smart Payment Repair Copilot", layout="wide")
st.title("Smart Payment Repair Copilot")

uploaded_file = st.file_uploader("Upload Payment XML", type=["xml"])
example_xml = """
<pacs.008>
  <Dbtr>
    <Nm>John Doe</Nm>
  </Dbtr>
  <DbtrAcct>
    <IBAN>DE89370400440532013000</IBAN>
  </DbtrAcct>
  <RmtInf>
    <Ustrd>Invoice 9914</Ustrd>
  </RmtInf>
</pacs.008>
"""

if st.button("Load Example Message"):
    uploaded_file = io.StringIO(example_xml)

if uploaded_file:
    xml_content = uploaded_file.read()
    root = parse_xml(xml_content)

    if root is None:
        st.error("Invalid XML format. Please upload a valid pacs.008 message.")
    else:
        st.subheader("Original Message")
        st.code(prettify_xml(root), language='xml')

        issues = find_missing_fields(root)

        if issues:
            st.warning("Issues Found:")
            for issue in issues:
                st.write(f"- {issue}")

            suggestions = suggest_fixes(root)
            if st.button("Apply Copilot Suggestions"):
                root = apply_suggestions(root, suggestions)
                st.success("Suggestions Applied!")

                st.subheader("\ud83c\udf0a Repaired Message")
                st.code(prettify_xml(root), language='xml')

                st.download_button(
                    label="Download Repaired XML",
                    data=prettify_xml(root),
                    file_name="repaired_payment.xml",
                    mime="application/xml"
                )
        else:
            st.success("No issues found. Payment is clean!")
st.markdown(
    """
    <style>
    /* Hide Streamlit's default footer completely */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .css-cio0dv.ea3mdgi1 {visibility: hidden;}

    /* Custom footer */
    .custom-footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #023d69;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }
    </style>
    <div class="custom-footer">
        🔹 Powered by Transact-AI Sandbox 🔹
    </div>
    """,
    unsafe_allow_html=True
)
