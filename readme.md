# TODOs
- switch to client-server db connection
- improve error handling
- embedding functionality	
	- test different embedding models
- creating graphs based on analysis
	-	caching graph data for faster retrieval and generation
	- graph analysis tool
	

# Features enabled

- post reviews in json format
	```[json]
	[
		{
			"id": 1,
			"location": "SF",
			"rating": 1,
			"text": "Food was cold and tasteless.",
			"date": "2025-06-13"
		},
	...,
	]
	```
- API made for record retrieval, db status and env health check
- Model used:
	`all-mpnet-base-v2`
	- reasons: Free, no limit, runs locally

- Semantic Search Enabled