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
from Modules.Finance_Modules.AccountantModule.AccountantModule import manager_agent
from Modules.Finance_Modules.TaxSpecialistModule.Tax_Specialist_Module import  TaxSpecialistTeam
from Modules.Finance_Modules.Accounting_Controller_Module.Accounting_Controller_Module import  AccountingComplianceTeam
from Modules.Finance_Modules.Reporting_Module.Agents import ReportingTeam
from Modules.Finance_Modules.Consolidation_Module.Consolidation_Module import Consolidation_Manager_Agent
from Modules.Finance_Modules.StructuralRiskAnalystModule.structural_risk_analyst_module import StructuralRiskAnalystTeam
from Modules.Finance_Modules.TreasurerModule.TreasurerModule import manager_agent



from Modules.Reporting_Module.Agents import ReportingTeam

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
    
    ##### the others
    elif request.moduleId == "accounting-finance":
        print("Running Accounting & Finance Module")
        response = manager_agent.run(f"""run the agent {request.agentId} with the prompt: {request.prompt}""")
        print("Response from Accounting & Finance Module:", response.content)
        return response.content
    elif request.moduleId == "tax-specialist":
        print("Running Tax Specialist Module")
        response = TaxSpecialistTeam.run(f"""run the agent {request.agentId} with the prompt: {request.prompt}""")
        print("Response from Tax Specialist Module:", response.content)
        return response.content
    elif request.moduleId == "accounting-compliance":
        print("Running Accounting Compliance Module")
        response = AccountingComplianceTeam.run(f"""run the agent {request.agentId} with the prompt: {request.prompt}""")
        print("Response from Accounting Compliance Module:", response.content)
        return response.content
    
    
    ##### Monday::
    elif request.moduleId == "reporting":
        print("Running Reporting Module")
        response = ReportingTeam.run(f"""run the agent {request.agentId} with the prompt: {request.prompt}""")
        print("Response from Reporting Module:", response.content)
        return response.content
    elif request.moduleId == "consolidation":
        print("Running Consolidation Module")
        response = Consolidation_Manager_Agent.run(f"""run the agent {request.agentId} with the prompt: {request.prompt}""")
        print("Response from Consolidation Module:", response.content)
        return response.content
    elif request.moduleId == "structural-risk-analyst":
        print("Running Structural Risk Analyst Module")
        response = StructuralRiskAnalystTeam.run(f"""run the agent {request.agentId} with the prompt: {request.prompt}""")
        print("Response from Structural Risk Analyst Module:", response.content)
        return response.content
    elif request.moduleId == "treasurer":
        print("Running Treasurer Module")
        response = manager_agent.run(f"""run the agent {request.agentId} with the prompt: {request.prompt}""")
        print("Response from Treasurer Module:", response.content)
        return response.content
    
    

    
    # Dummy return for now
    return {
        "status": "success",
        "moduleId": request.moduleId,
        "agentId": request.agentId,
        "output": f"Processed prompt for agent {request.agentId}"
    }
