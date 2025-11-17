import streamlit as st
from utils.utility import Utility
st.header("Browse and Search")
st.text_input(label="enter search text here")
st.subheader("DB Stats:")

st.info(
    Utility.db_check()
)