from fastapi import FastAPI, HTTPException
from backend.schema import Review
import chromadb
import os
from dotenv import load_dotenv
from chromadb.utils import embedding_functions
from fastapi.responses import JSONResponse

#env variable
load_dotenv()
DB_PATH = os.getenv("DB_PATH")

app = FastAPI()
db_client = chromadb.PersistentClient(DB_PATH)
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-mpnet-base-v2"  # Better quality, 768 dimensions
)
# embedding_fn = embedding_functions.DefaultEmbeddingFunction()
reviews_collection = db_client.get_or_create_collection(
    name="reviews",
    embedding_function=embedding_fn
)


@app.get("/")
async def root():
		return {"message": "Hello World"}


@app.post("/ingest")
def post_review(payload: list[Review]):
	"""
	Ingests a list of Review objects into the database.

	Args:
		payload (list[Review]): A list of Review objects to be added.

	Returns:
		dict: A response indicating the status of the ingestion operation.
	"""
	# patch data to db
	try:
		valid_rev = [r for r in payload if r.text is not None and r.id is not None]
		if not valid_rev:
			raise HTTPException(status_code=400, detail="No valid reviews to add")
	
		reviews_collection.add(
			documents=[r.text for r in valid_rev],
			#  TODO: understand client side embedding
			# embeddings=embedding_fn,
			ids=[str(r.id) for r in valid_rev],
			metadatas=[{
				"location": r.location or None,
				"rating": r.rating or None,
				"date": r.date or None
			} for r in valid_rev],
		)			
		
		return {"status" : 200, "detail" : "reviews added successfully"}
	
	except HTTPException as e:
		return {'status' : e.status_code, 'detail' : e.detail}
	
	except Exception as e:
		return JSONResponse(
			status_code=500,
			content={"status": "error", "detail": e.__str__()}
		)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/db_status")
def db_check():
	try:
		count = reviews_collection.count()
		body = reviews_collection.get(limit=5)
		return JSONResponse(
			status_code=200,
			content = {"status": "ok", "record_count": count, "body" : body}
		)
	except Exception as e:
		return JSONResponse(
			status_code=500,
			content={"status": "error", "detail": str(e), "body" : body}
		)

@app.get("/get_reviews")
def get_reviews(
		limit: int,
		offset: int
) -> JSONResponse:
	try:
			#TODO: add error handling for timeouts
			res = reviews_collection.get(
					limit=limit, 
					offset=offset, 
					# include=["documents", "metadatas", "embeddings"]
			)

			return JSONResponse(
					status_code=200,
					content={"status": "ok", "body": res}
			)
	except Exception as e:
			return JSONResponse(
					status_code=500,
					content={"status": "error", "detail": str(e)}
			)
	
@app.delete("/reviews/{review_id}")
def delete_review(review_id: str):
    """Delete a single review by ID."""
    try:
        reviews_collection.delete(ids=[review_id])
        return {"status": "ok", "detail": f"Review {review_id} deleted"}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": str(e)}
        )


@app.delete("/reviews")
def delete_reviews(ids: list[str]):
    """Delete multiple reviews by IDs."""
    try:
        reviews_collection.delete(ids=ids)
        return {"status": "ok", "detail": f"Deleted {len(ids)} reviews"}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": str(e)}
        )


@app.delete("/collection")
def drop_collection():
    """Drop the entire collection (use with caution)."""
    try:
        db_client.delete_collection("reviews")
        # Recreate empty collection
        global reviews_collection
        reviews_collection = db_client.get_or_create_collection(
            name="reviews",
            embedding_function=embedding_fn
        )
        return {"status": "ok", "detail": "Collection dropped and recreated"}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": str(e)}
        )

@app.get("/search")
def search(query:str | None, n_responses: int | None) -> JSONResponse:
	"""enables semantic search"""
	try:
		query_list = [q.strip() for q in query.split(',')]
		res = reviews_collection.query(
			query_texts=query_list,
			n_results=n_responses
		)
		
		return JSONResponse(
			status_code=200,
			content={
				"status" : "ok",
				"body" : res
			}
		)
	except Exception as e:
		return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": str(e)}
        )