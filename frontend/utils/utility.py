import httpx
from streamlit.runtime.uploaded_file_manager import UploadedFile
import json
import os
from dotenv import load_dotenv
# from fastapi.responses import JSONResponse
load_dotenv()
DEV_URL = os.getenv("DEV_URL")

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
				url = f"{DEV_URL}/ingest"
				try:
					res = await client.post(url, json=data)
					res.raise_for_status()
					return res.json()
				except httpx.HTTPStatusError as e:
					# Server returned a non-2xx response
					return {"status": "error", "status_code": e.response.status_code, "detail": e.response.text}
				except httpx.RequestError as e:
					# Network error
					return {"status": "error", "detail": str(e)}
	
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
	
	@staticmethod
	def db_check() -> json:
		with httpx.Client() as client:
			url = f"{DEV_URL}/db_status"
			try:
				res = client.get(url)
				res.raise_for_status()
				return res.json()
			except httpx.HTTPStatusError as e:
				return {"status": "error", "status_code": e.response.status_code, "detail": e.response.text}
			except httpx.RequestError as e:
				return {"status": "error", "detail": str(e)}
	
	@staticmethod
	def get_reviews(limit : int | None, offset : int | None)->json:
		with httpx.Client() as client:
			url = f"{DEV_URL}/get_reviews"
			try:
				res = client.get(url, params={
					"limit" : limit if limit is not None else 0,
					"offset" : offset if offset is not None else 0,
				})
				res.raise_for_status()
				return res.json()
			except httpx.HTTPStatusError as e:
				return {"status": "error", "status_code": e.response.status_code, "detail": e.response.text}
			except httpx.RequestError as e:
				return {"status": "error", "detail": str(e)}