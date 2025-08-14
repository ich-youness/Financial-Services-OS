import time
from fastapi import FastAPI, Query
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import routing_agent, chatbot_agent



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Real Estate Listings API is running"}

@app.get("/listings", response_model=List[Listing])
def get_listings(
    source: Optional[str] = None,
    type: Optional[str] = Query(None, regex="^(rent|sell)$"),
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    use_airtable: Optional[bool] = True,
):
    # Load listings from either Airtable or JSON
    if use_airtable: # airtable working corretly
        listings = get_airtable_listings()
        # print("listings from the airtable",listings)


    return listings

class ScrapeRequest(BaseModel):
    urls: List[str]

@app.post("/scrape")
def scrape_urls(request: ScrapeRequest):
    print("Received URLs:", request.urls)
    for url in request.urls:
        for _ in range(3):  
            results = routing_agent.run(message=f"scrape the listings from this url after identifying the type of the listing rent or sale based on the url: {url}")
            print(f"Results for {url}:", results.content)
            time.sleep(65)
    return {"received": request.urls}

# @app.post("/scrape", response_model=List[Listing])
# def scrape_listings(    urls: List[str] = Query(..., description="List of URLs to scrape"),
#     use_airtable: Optional[bool] = True,
# ):
#     print("Scraping URLs:", urls)
#     # Load listings from either Airtable or JSON
#     # if use_airtable: # airtable working corretly
#     #     listings = get_airtable_listings()
#     #     print("listings from the airtable",listings)


    # return  urls
# i will add later the endpoint for calling the agents on the chatbot

class ChatRequest(BaseModel):
    prompt: str


@app.post("/chat")
def chat_with_bot(request: ChatRequest):
    print("User prompt:", request.prompt)
    results = chatbot_agent.print_response(request.prompt , markdown=True)
    print(results)
    # dummy response for now
    return {
        f"{results}",
        
    }

