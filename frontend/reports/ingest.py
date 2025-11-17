import streamlit as st
from utils.utility import Utility
import asyncio

# Header
st.header("Ingest reviews")
st.markdown("----------")
st.subheader("2). Upload a JSON file")
uploaded = st.file_uploader("Choose a .json file (array of reviews)", type=["json"])
if st.button("Submit"):
	if uploaded is not None:
		res = asyncio.run(Utility.post_review_file(uploaded))
		st.write(res)
	else:
		st.write("Empty file(s)")