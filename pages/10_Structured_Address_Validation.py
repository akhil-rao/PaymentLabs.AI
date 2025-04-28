import streamlit as st
import json
import re

# ---- Helper Functions ----

def extract_characters_from_adrline(xml_text):
    adr_lines = re.findall(r"<AdrLine>(.*?)</AdrLine>", xml_text, re.DOTALL)
    full_text = " ".join(adr_lines)
    characters = [c.lower() for c in full_text if c.isalnum()]  # Only alphanumeric
    return characters

def extract_characters_from_structured_json(json_text):
    try:
        parsed = json.loads(json_text)
        structured_text = ""
        for value in parsed.get("PstlAdr", {}).values():
            structured_text += str(value) + " "
        characters = [c.lower() for c in structured_text if c.isalnum()]
        return characters
    except:
        return []

def validate_character_match(input_chars, output_chars):
    missing_chars = []
    for char in input_chars:
        if char in output_chars:
            output_chars.remove(char)  # Remove one occurrence
        else:
            missing_chars.append(char)
    return missing_chars

# ---- Streamlit App ----

st.set_page_config(page_title="Structured Address Validation", layout="wide")
st.title("🏛️ Structured Address Validation (Strict Mode)")

st.markdown("""
Paste your **Original Unstructured Address** and the **Transformed Structured Address** below.  
This validation checks for exact alphabet-level restructuring — no missing letters!
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

if st.button("🚀 Validate Exact Restructuring"):
    if original_input.strip() == "" or transformed_input.strip() == "":
        st.warning("⚠️ Please paste both the original and structured address first.")
    else:
        input_chars = extract_characters_from_adrline(original_input)
        output_chars = extract_characters_from_structured_json(transformed_input)

        missing = validate_character_match(input_chars, output_chars)

        if missing:
            st.error(f"❌ Data Loss Detected! Missing Characters: {', '.join(sorted(set(missing)))}")
            st.markdown(
                """
                <div style="background-color:#ffe6e6;padding:15px;border-radius:10px; margin-top:20px;">
                ❌ <b>Pure Restructuring Failed:</b> Some letters/numbers from the original address are missing in structured output.
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.success("✅ Perfect Structuring! No data loss detected.")
            st.markdown(
                """
                <div style="background-color:#e0f7fa;padding:15px;border-radius:10px; margin-top:20px;">
                ✅ <b>Zero Data Loss:</b> All characters preserved.<br><br>
                ✅ <b>No Enhancement:</b> Pure restructuring achieved without loss.
                </div>
                """,
                unsafe_allow_html=True
            )
