import streamlit as st
import requests

st.title("Content Moderation Admin Dashboard")

st.header("Upload Text")
text_input = st.text_area("Enter text to moderate")
if st.button("Moderate Text"):
    if text_input.strip():
        response = requests.post(f"http://127.0.0.1:8000/moderate/text?text={text_input}")
        st.json(response.json())

st.header("Upload Image")
uploaded_file = st.file_uploader("Upload image", type=["png","jpg","jpeg"])
if uploaded_file:
    response = requests.post("http://127.0.0.1:8000/moderate/image", files={"file": uploaded_file})
    st.json(response.json())
