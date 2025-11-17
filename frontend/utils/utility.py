import httpx
from streamlit.runtime.uploaded_file_manager import UploadedFile
import json


class Utility:
	@staticmethod
	async def post_review_file(payload: UploadedFile):
		if payload is not None:
			content = payload.read()
			# payload.read() may return bytes
			if isinstance(content, (bytes, bytearray)):
				content = content.decode()
			data = json.loads(content)
			async with httpx.AsyncClient() as client:
				res = await client.post("http://localhost:8000/ingest", json=data)
				return res.json()

		
			