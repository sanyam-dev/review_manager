import streamlit as st
from utils.utility import Utility
import json
from pandas import DataFrame as df


def helper_utility_check() -> json:
	res : json = Utility.db_check()
	return res

def helper_get_reviews(limit: int | None, offset: int | None):
	res: json = Utility.get_reviews(limit, offset)
	body = res['body']
	data = df({
		"ids": [int(r) for r in body["ids"]],
		"documents" : body["documents"],
		"location" : [r["location"] for r in body["metadatas"]],
		"rating" : [r["rating"] for r in body["metadatas"]],
		"date" : [r["date"] for r in body["metadatas"]]
	})
	return data, data.shape

get_review_res, df_shape = helper_get_reviews(10, 0)

# Reponse of DB stat
db_stat_res : json = helper_utility_check()

# UI code
st.header("Browse and Search")
st.text_input(label="enter search text here")

st.write("Response:")

if df_shape is not None or (0,0):
	st.dataframe(get_review_res, width='stretch', hide_index=True)
else:
	st.error(f"❌ Error: {str(get_review_res)}")

st.markdown("----------")

st.subheader("DB Stats:")
if db_stat_res["status"] == "ok":
	st.success("✅ Success: " + str(db_stat_res["record_count"]) + " records")
else:
	st.error(f"❌ Error: {str(db_stat_res)}")

