import streamlit as st
import xml.etree.ElementTree as ET
import io
from lxml import etree

# --- Helper Functions ---

def build_final_envelope(apphdr_xml, document_xml):
    NSMAP = {
        'env': 'urn:swift:xsd:envelope',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }
    envelope = etree.Element("{urn:swift:xsd:envelope}Envelope", nsmap=NSMAP)
    apphdr = etree.fromstring(apphdr_xml)
    apphdr.attrib['xmlns'] = 'urn:iso:std:iso:20022:tech:xsd:head.001.001.02'
    document = etree.fromstring(document_xml)
    document.attrib['xmlns'] = 'urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08'
    envelope.append(apphdr)
    envelope.append(document)
    return etree.tostring(envelope, pretty_print=True, encoding='unicode')

def parse_xml(xml_string):
    try:
        root = ET.fromstring(xml_string)
        for elem in root.iter():
            if elem.tag.startswith('{'):
                elem.tag = elem.tag.split('}', 1)[1]
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
    address_choice = user_choices.get('address_type', 'Structured')
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
        suggestions['LEI'] = '5493001KJTIIGC8Y1R12'
    if user_choices.get('fix_purpose', False):
        suggestions['PurposeCode'] = 'GDDS'
    if user_choices.get('fix_remittance', False):
        suggestions['RemittanceReference'] = 'RF712345678901234567'
    return suggestions

def suggest_fixes(root, user_choices):
    suggestions = {}
    address_choice = user_choices.get('address_type', 'Structured')

    dbtr = root.find(".//Dbtr")
    if dbtr is not None:
        pstlAdr = dbtr.find("PstlAdr")

        if pstlAdr is not None:
            existing_fields = {child.tag: child.text for child in pstlAdr}

            if address_choice == "Structured":
                # Try to split AdrLine into StrtNm and BldgNb and PstCd etc. if AdrLine is present
                if "AdrLine" in existing_fields or any(child.tag == "AdrLine" for child in pstlAdr):
                    adr_lines = [child.text for child in pstlAdr if child.tag == "AdrLine"]
                    if adr_lines:
                        # Basic smart parsing
                        line1 = adr_lines[0]
                        line2 = adr_lines[1] if len(adr_lines) > 1 else ''

                        # Assume BldgNb and StrtNm are in line1
                        if ' ' in line1:
                            bldg, street = line1.split(' ', 1)
                        else:
                            bldg, street = '', line1

                        # Assume postcode and town are in line2
                        if ' ' in line2:
                            postcode, town = line2.split(' ', 1)
                        else:
                            postcode, town = '', line2

                        suggestions['StructuredAddress'] = {
                            'BldgNb': bldg.strip(),
                            'StrtNm': street.strip(),
                            'PstCd': postcode.strip(),
                            'TwnNm': town.strip(),
                            'Ctry': existing_fields.get('Ctry', 'SG')  # Use existing Ctry if available
                        }
                else:
                    # If already structured fields exist, just reuse them
                    suggestions['StructuredAddress'] = {
                        'StrtNm': existing_fields.get('StrtNm', ''),
                        'BldgNb': existing_fields.get('BldgNb', ''),
                        'PstCd': existing_fields.get('PstCd', ''),
                        'TwnNm': existing_fields.get('TwnNm', ''),
                        'Ctry': existing_fields.get('Ctry', 'SG')
                    }

            elif address_choice == "Hybrid":
                adr_lines = [child.text for child in pstlAdr if child.tag == "AdrLine"]
                if not adr_lines:
                    # Build AdrLines from StrtNm and BldgNb
                    line1 = f"{existing_fields.get('BldgNb', '')} {existing_fields.get('StrtNm', '')}".strip()
                    line2 = f"{existing_fields.get('PstCd', '')} {existing_fields.get('TwnNm', '')}".strip()
                    adr_lines = [line1, line2]

                suggestions['HybridAddress'] = {
                    'AdrLine1': adr_lines[0] if len(adr_lines) > 0 else '',
                    'AdrLine2': adr_lines[1] if len(adr_lines) > 1 else '',
                    'TwnNm': existing_fields.get('TwnNm', 'Singapore'),
                    'Ctry': existing_fields.get('Ctry', 'SG')
                }

    # Other fields (LEI, Purpose Code, Remittance) same logic
    if user_choices.get('fix_lei', False):
        suggestions['LEI'] = '5493001KJTIIGC8Y1R12'

    if user_choices.get('fix_purpose', False):
        suggestions['PurposeCode'] = 'GDDS'

    if user_choices.get('fix_remittance', False):
        suggestions['RemittanceReference'] = 'RF712345678901234567'

    return suggestions

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

            # 🧩 Copilot Repair Options Section inside issues block
            st.subheader("Copilot Repair Options")

            address_type = st.radio("Choose Address Type:", ("Structured", "Hybrid"), index=0)
            fix_lei = st.checkbox("Fix Missing LEI")
            fix_purpose = st.checkbox("Fix Missing Purpose Code")
            fix_remittance = st.checkbox("Fix Missing Remittance Information")

            user_choices = {
                'address_type': address_type,
                'fix_lei': fix_lei,
                'fix_purpose': fix_purpose,
                'fix_remittance': fix_remittance
            }

            if st.button("Apply Copilot Suggestions"):
                suggestions = suggest_fixes(root, user_choices)
                root = apply_suggestions(root, suggestions)
                st.success("Suggestions Applied!")

                fixed_xml_string = prettify_xml(root)

                start_apphdr = fixed_xml_string.find("<AppHdr")
                end_apphdr = fixed_xml_string.find("</AppHdr>") + len("</AppHdr>")
                apphdr_xml = fixed_xml_string[start_apphdr:end_apphdr]

                start_doc = fixed_xml_string.find("<Document")
                end_doc = fixed_xml_string.find("</Document>") + len("</Document>")
                document_xml = fixed_xml_string[start_doc:end_doc]

                final_xml = build_final_envelope(apphdr_xml, document_xml)

                st.subheader("Repaired Swift CBPR+ Message")
                st.code(final_xml, language='xml')

                st.download_button(
                    label="Download Repaired Swift XML",
                    data=final_xml,
                    file_name="repaired_payment.xml",
                    mime="application/xml"
                )
        else:
            st.success("No issues found. Payment is clean!")
