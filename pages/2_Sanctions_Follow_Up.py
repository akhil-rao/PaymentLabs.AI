import streamlit as st

st.set_page_config(page_title="Sanctions Follow-Up Agent", layout="wide")
st.title("🛡️ Sanctions Follow-Up Agent")

st.info("🚧 This module is under development. Stay tuned!")
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
