import streamlit as st
import requests

# ---- Streamlit Page Setup ----
st.set_page_config(page_title="Structured Address Validation", layout="wide")

st.title("🏛️ Structured Address Validation (Powered by Nucleus API)")

st.markdown("""
Upload or paste a Swift CBPR+ XML address.  
This demo will show live structured output from the Nucleus Address Parser.
""")

# ---- Upload XML ----
uploaded_file = st.file_uploader("Upload Address XML", type=["xml"])

example_xml = """<PstlAdr>
  <AdrLine>230 VICTORIA STREET BUGIS JUNCTION TOWERS</AdrLine>
  <AdrLine>06-03 SINGAPORE 188024 SG</AdrLine>
</PstlAdr>"""

if st.button("Load Example"):
    uploaded_file = io.StringIO(example_xml)

# ---- Process ----
if uploaded_file:
    if isinstance(uploaded_file, str):
        xml_content = uploaded_file
    else:
        xml_content = uploaded_file.read()

    st.subheader("📝 Original Unstructured Address (AdrLine Format)")
    st.code(xml_content, language='xml')

    # ---- Call Nucleus API ----
    st.subheader("🔄 Calling Nucleus Structured Address API...")

    api_url = "https://recorder-new.nucleus.wavelabs.in/structured-address/parseXml"

    files = {'file': ('address.xml', xml_content, 'application/xml')}

    response = requests.post(api_url, files=files)

    if response.status_code == 200:
        structured_address = response.json()
        st.success("✅ Structured Address Received Successfully!")

        st.subheader("🏛️ Structured Address Output")
        st.json(structured_address)

        st.markdown(
            """
            <div style="background-color:#e0f7fa;padding:10px;border-radius:10px;">
            ✅ <b>Zero Data Loss:</b> No parts of input address lost.<br>
            ❌ <b>No Enhancement:</b> Only structuring applied based on given data.<br>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error(f"❌ Error calling Nucleus API: {response.status_code}")
