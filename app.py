import streamlit as st
import xml.etree.ElementTree as ET
import io
from lxml import etree

def build_final_envelope(apphdr_xml, document_xml):
    NSMAP = {
        'env': 'urn:swift:xsd:envelope',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }
    
    envelope = etree.Element("{urn:swift:xsd:envelope}Envelope", nsmap=NSMAP)

    # Parse AppHdr
    apphdr = etree.fromstring(apphdr_xml)
    apphdr.attrib['xmlns'] = 'urn:iso:std:iso:20022:tech:xsd:head.001.001.02'

    # Parse Document
    document = etree.fromstring(document_xml)
    document.attrib['xmlns'] = 'urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08'

    # Attach them inside Envelope
    envelope.append(apphdr)
    envelope.append(document)

    return etree.tostring(envelope, pretty_print=True, encoding='unicode')

# ---- Helper Functions ----
def parse_xml(xml_string):
    try:
        # Parse the XML
        root = ET.fromstring(xml_string)
        
        # Check and clean namespaces if they exist
        for elem in root.iter():
            if elem.tag.startswith('{'):
                elem.tag = elem.tag.split('}', 1)[1]  # Remove namespace part
        
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

def suggest_fixes(root, user_choices):
    suggestions = {}

    address_choice = user_choices.get('address_type', 'Structured')  # Default to Structured if not selected

    if address_choice == "Structured":
        suggestions['StructuredAddress'] = {
            'StrtNm': 'Main Street',
            'BldgNb': '123',
            'PstCd': '12345',
            'TwnNm': 'Sampletown',
            'Ctry': 'US'
        }
    elif address_choice == "Hybrid":
        suggestions['HybridAddress'] = {
            'AdrLine1': '123 Main Street',
            'AdrLine2': 'Sampletown 12345'
        }

    if user_choices.get('fix_lei', False):
        suggestions['LEI'] = '5493001KJTIIGC8Y1R12'  # Example dummy LEI

    if user_choices.get('fix_purpose', False):
        suggestions['PurposeCode'] = 'GDDS'  # Example: Goods Purchase

    if user_choices.get('fix_remittance', False):
        suggestions['RemittanceReference'] = 'RF712345678901234567'  # Dummy Creditor Reference

    return suggestions

def apply_suggestions(root, suggestions):
    dbtr = root.find(".//Dbtr")
    if 'PstlAdr' in suggestions and dbtr is not None:
        pstlAdr = dbtr.find("PstlAdr")
        if pstlAdr is None:
            pstlAdr = ET.SubElement(dbtr, "PstlAdr")
            for k, v in suggestions['PstlAdr'].items():
                ET.SubElement(pstlAdr, k).text = v

    if 'Purp' in suggestions:
        # Find the CdtTrfTxInf block
        cdt_trf_tx_inf = root.find(".//CdtTrfTxInf")
        if cdt_trf_tx_inf is not None:
            # Check if PmtTpInf already exists
            pmt_tp_inf = cdt_trf_tx_inf.find("PmtTpInf")
            if pmt_tp_inf is None:
                pmt_tp_inf = ET.SubElement(cdt_trf_tx_inf, "PmtTpInf")
            
            purp = pmt_tp_inf.find("Purp")
            if purp is None:
                purp = ET.SubElement(pmt_tp_inf, "Purp")
            
            cd = purp.find("Cd")
            if cd is None:
                cd = ET.SubElement(purp, "Cd")
            
            cd.text = suggestions['Purp']['Cd']
            
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
                # 🧩 Copilot Repair Options Section
st.subheader("Copilot Repair Options")

# Address type choice
address_type = st.radio(
    "Choose Address Type:",
    ("Structured", "Hybrid"),
    index=0
)

# Checkboxes for optional fixes
fix_lei = st.checkbox("Fix Missing LEI")
fix_purpose = st.checkbox("Fix Missing Purpose Code")
fix_remittance = st.checkbox("Fix Missing Remittance Information")

# Collect user choices into a dictionary
user_choices = {
    'address_type': address_type,
    'fix_lei': fix_lei,
    'fix_purpose': fix_purpose,
    'fix_remittance': fix_remittance
}

if st.button("Apply Copilot Suggestions"):
    suggestions = suggest_fixes(root, user_choices)  # Call suggest_fixes properly
    root = apply_suggestions(root, suggestions)
    st.success("Suggestions Applied!")

    # --- New XML building and Display code ---

    # Step 1: Convert repaired root to a string
    fixed_xml_string = prettify_xml(root)

    # Step 2: Extract AppHdr and Document separately
    start_apphdr = fixed_xml_string.find("<AppHdr")
    end_apphdr = fixed_xml_string.find("</AppHdr>") + len("</AppHdr>")
    apphdr_xml = fixed_xml_string[start_apphdr:end_apphdr]

    start_doc = fixed_xml_string.find("<Document")
    end_doc = fixed_xml_string.find("</Document>") + len("</Document>")
    document_xml = fixed_xml_string[start_doc:end_doc]

    # Step 3: Build final Swift-compliant Envelope
    final_xml = build_final_envelope(apphdr_xml, document_xml)

    # Step 4: Show final Swift CBPR+ XML
    st.subheader("Repaired Swift CBPR+ Message")
    st.code(final_xml, language='xml')

    # Step 5: Allow Download
    st.download_button(
        label="Download Repaired Swift XML",
        data=final_xml,
        file_name="repaired_payment.xml",
        mime="application/xml"
    )
