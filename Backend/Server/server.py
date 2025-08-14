import time
from fastapi import FastAPI
from typing import List, Optional, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from Modules.Risk_Assessment_Module import financial_router_team
from Modules.Investment_Analysis_Module import investment_router_team
from Modules.Client_Management_Module import client_service_router_team
from Modules.Fraud_Detection_Module import fraud_detection_router_team
from Modules.Regulatory_Compliance_Module import compliance_router_team
from Modules.Customer_Support_Module import customer_service_router_team

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend API is running"}


# Pydantic model for request
class ModuleRequest(BaseModel):
    moduleId: str
    agentId: str
    prompt: str
    config: Dict[str, Any]  # dynamic config


@app.post("/module")
def get_module(request: ModuleRequest):
    print("\nModule endpoint called")
    print("Module ID:", request.moduleId)
    print("Agent ID:", request.agentId)
    print("Prompt:", request.prompt)
    print("Config:", request.config)

    if request.moduleId == "risk-assessment":
        print("Running Risk Assessment Module")
        response = financial_router_team.run(f"""run the agent {request.agentId} with the prompt: {request.prompt}""")
        print("Response from Risk Assessment Module:", response.content)
        return response.content
    elif request.moduleId == "investment-analysis":
        print("Running Investment Analysis Module")
        response= investment_router_team.run(f"""run the agent {request.agentId} with the prompt: {request.prompt}""")
        print("Response from Investment Analysis Module:", response.content)
        return response.content
    elif request.moduleId == "client-management":
        print("Running Client Management Module")
        response = client_service_router_team.run(f"""run the agent {request.agentId} with the prompt: {request.prompt}""")
        print("Response from Client Management Module:", response.content)
        return response.content
    elif request.moduleId == "fraud-detection":
        print("Running Fraud Detection Module")
        response = fraud_detection_router_team.run(f"""run the agent {request.agentId} with the prompt: {request.prompt}""")
        print("Response from Fraud Detection Module:", response.content)
        return response.content
    elif request.moduleId == "regulatory-compliance":
        print("Running Regulatory Compliance Module")
        response = compliance_router_team.run(f"""run the agent {request.agentId} with the prompt: {request.prompt}""")
        print("Response from Regulatory Compliance Module:", response.content)
        return response.content
    elif request.moduleId == "customer-support":
        print("Running Customer Support Module")
        response = customer_service_router_team.run(f"""run the agent {request.agentId} with the prompt: {request.prompt}""")
        print("Response from Customer Support Module:", response.content)
        return response.content
    
    # Dummy return for now
    return {
        "status": "success",
        "moduleId": request.moduleId,
        "agentId": request.agentId,
        "output": f"Processed prompt for agent {request.agentId}"
    }

# @app.get("/listings", response_model=List[Listing])
# def get_listings(
#     source: Optional[str] = None,
#     type: Optional[str] = Query(None, regex="^(rent|sell)$"),
#     min_price: Optional[float] = None,
#     max_price: Optional[float] = None,
#     use_airtable: Optional[bool] = True,
# ):
#     # Load listings from either Airtable or JSON
#     if use_airtable: # airtable working corretly
#         listings = get_airtable_listings()
#         # print("listings from the airtable",listings)


#     return listings

# class ScrapeRequest(BaseModel):
#     urls: List[str]

# @app.post("/scrape")
# def scrape_urls(request: ScrapeRequest):
#     print("Received URLs:", request.urls)
#     for url in request.urls:
#         for _ in range(3):  
#             results = routing_agent.run(message=f"scrape the listings from this url after identifying the type of the listing rent or sale based on the url: {url}")
#             print(f"Results for {url}:", results.content)
#             time.sleep(65)
#     return {"received": request.urls}

# # @app.post("/scrape", response_model=List[Listing])
# # def scrape_listings(    urls: List[str] = Query(..., description="List of URLs to scrape"),
# #     use_airtable: Optional[bool] = True,
# # ):
# #     print("Scraping URLs:", urls)
# #     # Load listings from either Airtable or JSON
# #     # if use_airtable: # airtable working corretly
# #     #     listings = get_airtable_listings()
# #     #     print("listings from the airtable",listings)


#     # return  urls
# # i will add later the endpoint for calling the agents on the chatbot

# class ChatRequest(BaseModel):
#     prompt: str


# @app.post("/chat")
# def chat_with_bot(request: ChatRequest):
#     print("User prompt:", request.prompt)
#     results = chatbot_agent.print_response(request.prompt , markdown=True)
#     print(results)
#     # dummy response for now
#     return {
#         f"{results}",
        
#     }

