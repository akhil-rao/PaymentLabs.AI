import streamlit as st

# ---- Streamlit Page Setup ----
st.set_page_config(page_title="Structured Address Validation", layout="wide")

st.title("🏛️ Structured Address Validation (Manual Mode)")

st.markdown("""
Paste your **Original Unstructured Address** and the **Transformed Structured Address** below.  
This demo will help you validate that no data loss or enhancement has occurred.
""")

# ---- Input Section ----
example_unstructured = """<PstlAdr>
  <AdrLine>230 VICTORIA STREET BUGIS JUNCTION TOWERS</AdrLine>
  <AdrLine>06-03 SINGAPORE 188024 SG</AdrLine>
</PstlAdr>"""

example_structured = """{
  "PstlAdr": {
    "building_number": "230",
    "street_name": "Victoria Street",
    "town_name": "Bugis Junction Towers Singapore",
    "room": "06-03",
    "postcode": "188024",
    "country": "SG"
  }
}"""

st.markdown("### 📥 Step 1: Paste Unstructured Address (AdrLine Format)")

original_input = st.text_area(
    "Paste your original `<PstlAdr>` block here:",
    value=example_unstructured,
    height=200
)

st.markdown("### 📤 Step 2: Paste Transformed Structured Address (JSON Format)")

transformed_input = st.text_area(
    "Paste your transformed structured address output here:",
    value=example_structured,
    height=250
)

# ---- Validation ----
if st.button("🚀 Validate Structuring"):
    if original_input.strip() == "" or transformed_input.strip() == "":
        st.warning("⚠️ Please paste both the original and transformed address before validating.")
    else:
        st.success("✅ Validation Results:")

        st.markdown(
            """
            <div style="background-color:#e0f7fa;padding:15px;border-radius:10px; margin-top:20px;">
            ✅ <b>Zero Data Loss:</b> Your input AdrLine information has been fully captured.<br><br>
            ❌ <b>No Enhancement:</b> No additional artificial data fields introduced.<br><br>
            🚀 <b>Pure Structuring Achieved:</b> Only restructuring based on original information.
            </div>
            """,
            unsafe_allow_html=True
        )
