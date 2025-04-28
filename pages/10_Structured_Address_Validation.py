import streamlit as st
import requests

# ---- Streamlit Page Setup ----
st.set_page_config(page_title="Structured Address Validation", layout="wide")

st.title("🏛️ Structured Address Validation (Powered by Nucleus API)")

st.markdown("""
Paste your Swift CBPR+ Address XML below.  
This demo will live-validate and structure your address using the Nucleus Structured Address API.
""")

# ---- Input Section ----
example_xml = """<PstlAdr>
  <AdrLine>230 VICTORIA STREET BUGIS JUNCTION TOWERS</AdrLine>
  <AdrLine>06-03 SINGAPORE 188024 SG</AdrLine>
</PstlAdr>"""

st.markdown("### 📥 Paste Unstructured Address (AdrLine Format)")

user_input = st.text_area(
    "Paste your `<PstlAdr>` block here:",
    value=example_xml,
    height=200
)

# ---- On Button Click ----
if st.button("🚀 Structure Address"):
    if user_input.strip() == "":
        st.warning("⚠️ Please paste a valid unstructured address XML.")
    else:
        st.subheader("🔄 Sending to Nucleus API...")

        api_url = "https://recorder-new.nucleus.wavelabs.in/structured-address/parseXml"

        # Prepare file upload
        files = {'file': ('address.xml', user_input, 'application/xml')}

        try:
            response = requests.post(api_url, files=files)

            if response.status_code == 200:
                structured_address = response.json()

                st.success("✅ Structured Address Received Successfully!")

                st.markdown("### 🏛️ Structured Address Output")
                st.json(structured_address)

                st.markdown(
                    """
                    <div style="background-color:#e0f7fa;padding:15px;border-radius:10px; margin-top:20px;">
                    ✅ <b>Zero Data Loss:</b> No parts of your input address are lost.<br><br>
                    ❌ <b>No Enhancement:</b> Only fields present in your pasted data are structured.<br><br>
                    🚀 <b>Pure Structuring:</b> Exact transformation into Swift CBPR+ compliant address format.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.error(f"❌ Error calling Nucleus API: Status Code {response.status_code}")
                st.text(f"Server Response: {response.text}")

        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {e}")
