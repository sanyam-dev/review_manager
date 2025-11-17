import streamlit as st
from utils.utility import Utility
import json
from pandas import DataFrame as df


def helper_utility_check() -> json:
	res : json = Utility.db_check()
	return res

def helper_get_reviews(limit: int | None, offset: int | None):
	res: json = Utility.get_reviews(limit, offset)
	try:
		body = res['body']
	except Exception as e:
		return  {"status": "error", "detail": str(res)} , (0,0)
	data = df({
		"ids": [int(r) for r in body["ids"]],
		"documents" : body["documents"],
		"location" : [r["location"] for r in body["metadatas"]],
		"rating" : [r["rating"] for r in body["metadatas"]],
		"date" : [r["date"] for r in body["metadatas"]]
	})
	return data, data.shape

def helper_search_query(search_query: str | None) -> tuple:
    results: json = Utility.search(search_query)
    try:
        body = results["body"]
        data = df({
            "ids": body["ids"][0],  # Flatten from [['1', '13', ...]] to ['1', '13', ...]
            "documents": body["documents"][0],
            "distances": body["distances"][0],
            "location": [r["location"] for r in body["metadatas"][0]],
            "rating": [r["rating"] for r in body["metadatas"][0]],
            "date": [r["date"] for r in body["metadatas"][0]]
        })
        return data, None
    except Exception as e:
        return None, str(e)
	
get_review_res, df_shape = helper_get_reviews(10, 0)

# Reponse of DB stat
db_stat_res : json = helper_utility_check()

# UI code
st.header("Browse and Search")
# Capture search input
search_query = st.text_input(label="Enter search text here", placeholder="e.g., cold food, slow service...")
if search_query:
	with st.spinner("Searching..."):
		search_results, error = helper_search_query(search_query)
		if error:
				st.error(f"❌ Search error: {error}")
		else:
				st.write(f"Search Results for: '{search_query}'")
				st.dataframe(search_results, width='stretch', hide_index=True)
else:
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

