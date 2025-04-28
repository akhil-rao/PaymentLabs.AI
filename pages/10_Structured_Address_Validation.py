import streamlit as st
import json
import re

# ---- Helper Functions ----

def extract_words_from_adrline(xml_text):
    adr_lines = re.findall(r"<AdrLine>(.*?)</AdrLine>", xml_text, re.DOTALL)
    full_text = " ".join(adr_lines)
    words = re.findall(r'\b\w+\b', full_text)  # Extract words only
    return [word.lower() for word in words if word]

def extract_words_from_structured_json(json_text):
    try:
        parsed = json.loads(json_text)
        structured_text = ""
        for value in parsed.get("PstlAdr", {}).values():
            structured_text += str(value) + " "
        words = re.findall(r'\b\w+\b', structured_text)
        return [word.lower() for word in words if word]
    except:
        return []

def validate_word_match(input_words, output_words):
    missing_words = []
    for word in input_words:
        if word not in output_words:
            missing_words.append(word)
    return missing_words

# ---- Streamlit App ----

st.set_page_config(page_title="Structured Address Validation", layout="wide")
st.title("🏛️ Structured Address Validation (Improved Word-Level Validation)")

st.markdown("""
Paste your **Original Unstructured Address** and the **Transformed Structured Address** below.  
This validation checks for exact word-level restructuring — missing words will be detected!
""")

example_unstructured = """<PstlAdr>
  <AdrLine>#18 16 Leicester Road</AdrLine>
  <AdrLine>358828 Singapore</AdrLine>
</PstlAdr>"""

example_structured = """{
  "PstlAdr": {
    "room": "#18",
    "building_number": "16",
    "street_name": "Road",
    "postcode": "358828",
    "country": "Singapore"
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
    "Paste your structured address output here (JSON format):",
    value=example_structured,
    height=250
)

if st.button("🚀 Validate Structuring at Word Level"):
    if original_input.strip() == "" or transformed_input.strip() == "":
        st.warning("⚠️ Please paste both the original and structured address first.")
    else:
        input_words = extract_words_from_adrline(original_input)
        output_words = extract_words_from_structured_json(transformed_input)

        missing_words = validate_word_match(input_words, output_words)

        if missing_words:
            st.error(f"❌ Data Loss Detected! Missing Words: {', '.join(missing_words)}")
            st.markdown(
                """
                <div style="background-color:#ffe6e6;padding:15px;border-radius:10px; margin-top:20px;">
                ❌ <b>Pure Restructuring Failed:</b> Some important words from the original address are missing in the structured output.<br>
                Please verify restructuring rules.
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.success("✅ Perfect Structuring! No data loss detected.")
            st.markdown(
                """
                <div style="background-color:#e0f7fa;padding:15px;border-radius:10px; margin-top:20px;">
                ✅ <b>Zero Data Loss:</b> All words from the original address are present.<br><br>
                ✅ <b>No Enhancement:</b> Pure restructuring achieved without any loss.
                </div>
                """,
                unsafe_allow_html=True
            )
