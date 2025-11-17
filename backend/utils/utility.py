import httpx
from streamlit.runtime.uploaded_file_manager import UploadedFile
import json
from chromadb import Collection

# /Users/ashu/projects/python/review_manager/frontend/utils/utility.py

class Utility:
	@staticmethod
	def db_check():
		res = httpx.get('http://localhost:8000/db_status')
		return res.json()

	@staticmethod
	async def add_to_db(collection_name: Collection, doc, ids, mdt):
		await collection_name.add(
			documents=doc,
			ids=ids,
			metadatas=mdt
		)
