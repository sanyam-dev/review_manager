## **Goal**

Build a small web app for a multi-location business to **ingest customer reviews**, **search/filter**, **analyze sentiment/topics**, and **draft a suggested reply** using an LLM (or a local fallback).

* Frontend: React (or Streamlit if you prefer), deployed publicly.

* Backend: FastAPI with clean REST endpoints \+ OpenAPI docs at `/docs`. FastAPI provides automatic, interactive docs (Swagger UI). [FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/?utm_source=chatgpt.com)

* AI: use an LLM API if you have a key; otherwise use a tiny **Hugging Face `transformers` pipeline** (e.g., `sentiment-analysis`, `summarization`). [Hugging Face+1](https://huggingface.co/docs/transformers/en/main_classes/pipelines?utm_source=chatgpt.com)

* Search/RAG-lite: implement **TF-IDF \+ cosine similarity** to retrieve similar reviews for a query. Use scikit-learn’s `TfidfVectorizer` and `cosine_similarity`. [Scikit-learn+1](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html?utm_source=chatgpt.com)

## **Features**

### **1\) Ingest**

* Upload or POST a JSON array of reviews:  
   `{ id, location, rating (1–5), text, date }`

* Store in SQLite (or Postgres). Keep it simple.

### **2\) Browse & Search**

* Table view with filters: `location`, `sentiment` (once computed), text search.

* Clicking a row shows a **detail view**.

### **3\) Analytics**

* Counts by `sentiment` and by a coarse `topic` tag (e.g., “service”, “cleanliness”, “price”). Show a basic bar chart.

### **4\) AI-assist**

* Button: **“Suggest reply”** → generate a concise, empathetic draft response.

* Return `{ reply, tags: {sentiment, topic}, reasoning_log }`.

* Add basic safeguards (e.g., redact emails/phones; avoid toxic language) — a simple rules check is fine.

### **5\) Similar Reviews (RAG-lite)**

* Endpoint `GET /search?q=` returns top-5 similar reviews using **TF-IDF** vectors and **cosine similarity**. [Scikit-learn+1](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html?utm_source=chatgpt.com)


## **API (FastAPI)**

Expose these routes (with pydantic models \+ error handling):

* `POST /ingest` — accept the reviews array; persist.

* `GET /reviews?location=&sentiment=&q=&page=&page_size=` — server-side filtering \+ pagination.

* `GET /reviews/{id}` — full record.

* `POST /reviews/{id}/suggest-reply` — returns `{ reply, tags, reasoning_log }`.

* `GET /analytics` — counts by sentiment/topic.

* `GET /search?q=&k=` — TF-IDF \+ cosine similarity results.

* `GET /health`

Include automatic docs at `/docs` (Swagger UI) and `/redoc`. FastAPI generates these by default. [FastAPI](https://fastapi.tiangolo.com/reference/openapi/docs/?utm_source=chatgpt.com)

**Auth:** a single API key via header is enough for this exercise.

**Tests:** add at least one happy-path \+ one error-path test for any endpoint.

---

## **Frontend (React or Streamlit)**

* **Inbox page:** table with filters \+ search, pagination, loading/error states.

* **Detail page:** full review, AI tags, **editable** suggested reply with “Copy” action.

* **Analytics page:** simple bar chart (any chart lib or plain HTML/SVG).

If using **React**, call your FastAPI endpoints (don’t call models from the browser).

If using **Streamlit**, you may still keep FastAPI as a separate backend and call it from Streamlit (recommended to exercise both FE and BE). Deployment docs for **Streamlit Community Cloud** are here. [docs.streamlit.io](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app?utm_source=chatgpt.com)

---

## **AI Integration (pick one or support both)**

1. **LLM API path** (e.g., OpenAI/Claude) — read keys from env; expose basic knobs (temperature/system prompt/few-shots).

2. **Local fallback** — use `transformers` **pipelines** for:

   * `sentiment-analysis` → `sentiment`

   * `summarization` → a short gist to seed the reply  
      (Any small model is fine; keep downloads light.) [Hugging Face+1](https://huggingface.co/docs/transformers/en/main_classes/pipelines?utm_source=chatgpt.com)

---

## **Deployment (required)**

Provide a **public URL**. Choose one:

* **React frontend on Vercel** (quickstart here) or Netlify. [Vercel+1](https://vercel.com/guides/deploying-react-with-vercel?utm_source=chatgpt.com)

* **Streamlit app on Streamlit Community Cloud** (if you built Streamlit). [docs.streamlit.io](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app?utm_source=chatgpt.com)

If using React \+ FastAPI, deploy the **frontend** on **Vercel or Netlify**, and deploy the **backend** anywhere you like (Render/Railway/Fly/etc.). Vercel/Netlify docs cover the React deploy steps; follow their CLI or Git-based flow. [Vercel+1](https://vercel.com/guides/deploying-react-with-vercel?utm_source=chatgpt.com)

(If you prefer deploying React on Vercel via CLI, see `vercel --prod` guide. [Vercel](https://vercel.com/docs/deployments?utm_source=chatgpt.com))

---

## **What we’ll evaluate (100 pts)**

* **Backend design & correctness (25)** — clear models, pagination, errors, minimal tests.

* **Frontend UX & state (20)** — simple, robust flows; loading/error handling.

* **Applied-AI quality (25)** — useful reply, sensible tagging, basic guardrails.

* **Search/RAG-lite (10)** — TF-IDF \+ cosine similarity implemented correctly. [Scikit-learn+1](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html?utm_source=chatgpt.com)

* **Product thinking (10)** — pragmatic defaults; trade-offs noted.

* **Code quality (10)** — structure, typing, linting, README.

* **Bonus (+5)** — thoughtful touches (e.g., streaming replies, rate limiting, tiny E2E test).

---

## **Constraints & Notes**

* Keep it shippable within 6–8 hours; it’s fine to stub pieces. Call out what you’d do next with more time.

* Prefer small libs you already know.

* FastAPI generates interactive docs at `/docs` (Swagger UI) by default; don’t over-engineer. [FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/?utm_source=chatgpt.com)

* For TF-IDF search, `TfidfVectorizer` \+ `cosine_similarity` is sufficient. [Scikit-learn+1](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html?utm_source=chatgpt.com)

* For a quick AI fallback, use `transformers` pipelines (`pipeline('sentiment-analysis')`, `pipeline('summarization')`). [Hugging Face+1](https://huggingface.co/docs/transformers/en/main_classes/pipelines?utm_source=chatgpt.com)

---

## **Tiny sample (format)**

`[`  
  `{"id": 1, "location": "NYC", "rating": 2, "text": "Waited 40 min for pickup; staff seemed overwhelmed.", "date": "2025-06-12"},`  
  `{"id": 2, "location": "NYC", "rating": 5, "text": "Quick service and super friendly at checkout!", "date": "2025-06-13"},`  
  `{"id": 3, "location": "SF",  "rating": 3, "text": "Food was good but order notes were ignored.", "date": "2025-06-15"},`  
  `{"id": 4, "location": "SF",  "rating": 1, "text": "App kept crashing, couldn’t place order.", "date": "2025-06-16"},`  
  `{"id": 5, "location": "LA",  "rating": 4, "text": "Clean store, decent prices, parking a bit tight.", "date": "2025-06-18"},`  
  `{"id": 6, "location": "LA",  "rating": 2, "text": "Delivery late and items missing.", "date": "2025-06-20"}`  
`]`

