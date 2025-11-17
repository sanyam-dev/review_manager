import httpx
from streamlit.runtime.uploaded_file_manager import UploadedFile
import json


class Utility:
	@staticmethod
	async def post_review_file(payload: UploadedFile):
		"""
		Asynchronously posts a review file to the backend ingestion endpoint.
		Args:
			payload : UploadedFile
		Returns:
			dict: The JSON response from the backend ingestion endpoint.
		Raises:
			json.JSONDecodeError: If the file content is not valid JSON.
			httpx.HTTPError: If the HTTP request to the backend fails.
		"""
		if payload is not None:
			content = payload.read()
			# payload.read() may return bytes
			if isinstance(content, (bytes, bytearray)):
				content = content.decode()
			data = json.loads(content)
			async with httpx.AsyncClient() as client:
				res = await client.post("http://localhost:8000/ingest", json=data)
				return res.json()
	
	@staticmethod
	async def get_data(n: int):
		"""
		get the most recent 5 reviews added to the db
		
		Args:
			n: int => number of records to show
		Returns:
			dict: JSON response => Reponses from the db
		"""
		if n is None:
			n = 5
		
		