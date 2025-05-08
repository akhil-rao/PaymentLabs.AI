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

    dbtr = root.find(".//Dbtr")
    if dbtr is not None:
        pstlAdr = dbtr.find("PstlAdr")
        if pstlAdr is not None:
            existing_fields = {child.tag: child.text for child in pstlAdr}

            if address_choice == "Structured":
                if "AdrLine" in existing_fields or any(child.tag == "AdrLine" for child in pstlAdr):
                    adr_lines = [child.text for child in pstlAdr if child.tag == "AdrLine"]
                    if adr_lines:
                        line1 = adr_lines[0]
                        line2 = adr_lines[1] if len(adr_lines) > 1 else ''
                        if ' ' in line1:
                            bldg, street = line1.split(' ', 1)
                        else:
                            bldg, street = '', line1
                        if ' ' in line2:
                            postcode, town = line2.split(' ', 1)
                        else:
                            postcode, town = '', line2

                        suggestions['StructuredAddress'] = {
                            'BldgNb': bldg.strip(),
                            'StrtNm': street.strip(),
                            'PstCd': postcode.strip(),
                            'TwnNm': town.strip(),
                            'Ctry': existing_fields.get('Ctry', 'SG')
                        }
                else:
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
                    line1 = f"{existing_fields.get('BldgNb', '')} {existing_fields.get('StrtNm', '')}".strip()
                    line2 = f"{existing_fields.get('PstCd', '')} {existing_fields.get('TwnNm', '')}".strip()
                    adr_lines = [line1, line2]

                suggestions['HybridAddress'] = {
                    'AdrLine1': adr_lines[0] if len(adr_lines) > 0 else '',
                    'AdrLine2': adr_lines[1] if len(adr_lines) > 1 else '',
                    'TwnNm': existing_fields.get('TwnNm', 'Singapore'),
                    'Ctry': existing_fields.get('Ctry', 'SG')
                }

    if user_choices.get('fix_lei', False):
        suggestions['LEI'] = '5493001KJTIIGC8Y1R12'
    if user_choices.get('fix_purpose', False):
        suggestions['PurposeCode'] = 'GDDS'
    if user_choices.get('fix_remittance', False):
        suggestions['RemittanceReference'] = 'RF712345678901234567'
    return suggestions

def apply_suggestions(root, suggestions):
    dbtr = root.find(".//Dbtr")
    if dbtr is not None:
        pstlAdr = dbtr.find("PstlAdr")
        if pstlAdr is None:
            pstlAdr = ET.SubElement(dbtr, "PstlAdr")
        else:
            pstlAdr.clear()

        if 'StructuredAddress' in suggestions:
            for field, value in suggestions['StructuredAddress'].items():
                ET.SubElement(pstlAdr, field).text = value

        if 'HybridAddress' in suggestions:
            for key, value in suggestions['HybridAddress'].items():
                if key.startswith('AdrLine'):
                    adrLine = ET.SubElement(pstlAdr, "AdrLine")
                    adrLine.text = value
                else:
                    ET.SubElement(pstlAdr, key).text = value

    if 'LEI' in suggestions:
        id_elem = dbtr.find("Id")
        if id_elem is None:
            id_elem = ET.SubElement(dbtr, "Id")
        org_id = id_elem.find("OrgId")
        if org_id is None:
            org_id = ET.SubElement(id_elem, "OrgId")
        lei = org_id.find("LEI")
        if lei is None:
            lei = ET.SubElement(org_id, "LEI")
        lei.text = suggestions['LEI']

    if 'PurposeCode' in suggestions:
        cdt_trf_tx_inf = root.find(".//CdtTrfTxInf")
        if cdt_trf_tx_inf is not None:
            pmt_tp_inf = cdt_trf_tx_inf.find("PmtTpInf")
            if pmt_tp_inf is None:
                pmt_tp_inf = ET.SubElement(cdt_trf_tx_inf, "PmtTpInf")
            purp = pmt_tp_inf.find("Purp")
            if purp is None:
                purp = ET.SubElement(pmt_tp_inf, "Purp")
            cd = purp.find("Cd")
            if cd is None:
                cd = ET.SubElement(purp, "Cd")
            cd.text = suggestions['PurposeCode']

    if 'RemittanceReference' in suggestions:
        cdt_trf_tx_inf = root.find(".//CdtTrfTxInf")
        if cdt_trf_tx_inf is not None:
            rmt_inf = cdt_trf_tx_inf.find("RmtInf")
            if rmt_inf is None:
                rmt_inf = ET.SubElement(cdt_trf_tx_inf, "RmtInf")
            strd = rmt_inf.find("Strd")
            if strd is None:
                strd = ET.SubElement(rmt_inf, "Strd")
            cdtr_ref_inf = strd.find("CdtrRefInf")
            if cdtr_ref_inf is None:
                cdtr_ref_inf = ET.SubElement(strd, "CdtrRefInf")
            ref = cdtr_ref_inf.find("Ref")
            if ref is None:
                ref = ET.SubElement(cdtr_ref_inf, "Ref")
            ref.text = suggestions['RemittanceReference']

    return root

def prettify_xml(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    return rough_string.decode('utf-8')


# ---- Streamlit App ----

st.set_page_config(page_title="Swift CBPR+ Structured Payment Copilot", layout="wide")
st.title("🚀 Swift CBPR+ Structured Payment Copilot")

st.subheader("📂 Upload Your Payment XML")
uploaded_file = st.file_uploader("Choose a Payment XML File", type=["xml"])

st.caption("Or use an example file below:")

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
        st.error("❌ Invalid XML format. Please upload a valid pacs.008 message.")
    else:
        st.subheader("🔍 Detected Issues")
        issues = find_missing_fields(root)

        if issues:
            st.warning("We found the following issues in your payment XML:")
            for issue in issues:
                st.write(f"- {issue}")

            st.subheader("🛠️ Select Repair Actions")

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

            if st.button("🚀 Apply Copilot Suggestions", key="apply_copilot"):
                suggestions = suggest_fixes(root, user_choices)
                original_root = parse_xml(xml_content)
                repaired_root = apply_suggestions(root, suggestions)
                st.success("✅ Suggestions Applied!")

                # Generate Repaired Swift Envelope
                fixed_xml_string = prettify_xml(repaired_root)

                start_apphdr = fixed_xml_string.find("<AppHdr")
                end_apphdr = fixed_xml_string.find("</AppHdr>") + len("</AppHdr>")
                apphdr_xml = fixed_xml_string[start_apphdr:end_apphdr]

                start_doc = fixed_xml_string.find("<Document")
                end_doc = fixed_xml_string.find("</Document>") + len("</Document>")
                document_xml = fixed_xml_string[start_doc:end_doc]

                final_xml = build_final_envelope(apphdr_xml, document_xml)

                # --- Show Before vs After ---
                st.subheader("📝 Before vs ✨ After Comparison")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 📝 Original Message")
                    st.code(prettify_xml(original_root), language='xml')

                with col2:
                    st.markdown("### ✨ Repaired Message")
                    st.code(final_xml, language='xml')

                # --- Changes Summary ---
                st.subheader("🛠️ Fields Updated by Copilot")
                changes_made = []
                if user_choices.get('fix_lei', False):
                    changes_made.append("• Debtor LEI added or updated")
                if user_choices.get('fix_purpose', False):
                    changes_made.append("• Purpose Code (Purp) added or updated")
                if user_choices.get('fix_remittance', False):
                    changes_made.append("• Remittance Information (RmtInf) added or updated")
                if address_type:
                    changes_made.append(f"• Address structured as **{address_type} Address**")

                if changes_made:
                    st.success("\n".join(changes_made))
                else:
                    st.info("No structural changes were required.")

                st.subheader("⬇️ Download Repaired Swift CBPR+ XML")
                st.download_button(
                    label="Download Repaired XML",
                    data=final_xml,
                    file_name="repaired_payment.xml",
                    mime="application/xml"
                )
        else:
            st.success("✅ No issues found. Payment is clean!")
            st.code(prettify_xml(root), language='xml')

# ---- Custom Footer ----
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .css-cio0dv.ea3mdgi1 {visibility: hidden;}
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
        🔹 Powered by PaymentLabs.AI Sandbox 🔹
    </div>
    """,
    unsafe_allow_html=True
)
