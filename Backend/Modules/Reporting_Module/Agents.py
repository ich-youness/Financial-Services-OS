from agno.agent import Agent
from agno.team.team import Team
from agno.models.openai import OpenAIChat
from agno.models.google import Gemini
from agno.models.mistral import MistralChat
from agno.tools.scrapegraph import ScrapeGraphTools
from agno.tools.file import FileTools
from agno.tools.exa import ExaTools
from agno.tools.reasoning import ReasoningTools
from agno.models.huggingface import HuggingFace
from agno.tools.yfinance import YFinanceTools
from agno.tools.calculator import CalculatorTools
from dotenv import load_dotenv
import os
from polygon import RESTClient
import numpy as np
import pandas as pd
from scipy.stats import norm
from agno.knowledge.markdown import MarkdownKnowledgeBase

load_dotenv()
kb = MarkdownKnowledgeBase(path="Knowledge/subsidiary_assistance_kb.md")

# Initialize the agent
AssistanceToSubsidiariesAgent = Agent(
    name="AssistanceToSubsidiaries",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[ FileTools()],  # Add FileTools if you want the agent to read templates or other files
    reasoning=True,
    stream=True,
    show_tool_calls=True,
    knowledge=kb,
    description="""
    This agent provides guidance and support to subsidiaries during the consolidation process. 
    It answers questions on accounting treatments, provides reporting templates, and helps troubleshoot discrepancies.
    """,
    instructions="""
    - Always answer based on the knowledge base first.
    - Use templates or reporting examples when applicable.
    - If the question involves missing data or discrepancies, suggest corrective steps.
    - Keep explanations clear and concise for local finance teams.
    """
)

# Example query
# AssistanceToSubsidiariesAgent.print_response("How should we adjust intercompany sales according to IFRS 10 and our group policies?")


# Load your knowledge base (Markdown file with reporting instructions, templates, deadlines)
kb2 = MarkdownKnowledgeBase(path="Knowledge/group_instructions_kb.md")

# Initialize the agent
ProductionOfGroupInstructionsAgent = Agent(
    name="ProductionOfGroupInstructions",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[ FileTools()],  # FileTools for accessing templates or previous memos
    reasoning=True,
    knowledge=kb2,
    stream=True,
    show_tool_calls=True,
    description="""
    This agent prepares and distributes standardized guidance to subsidiaries before closing periods.
    It publishes reporting calendars, defines reporting packages, and issues special guidance memos for one-off transactions.
    """,
    instructions="""
    - Always reference the knowledge base for deadlines, templates, and guidance instructions.
    - Generate a clear and concise reporting timetable for subsidiaries.
    - Include format requirements, chart of accounts, and consolidation adjustments in instructions.
    - Draft special memos for unique transactions like divestitures, restructurings, or hedge accounting changes.
    - Ensure outputs are ready for distribution via email or internal portals.
    """
)


# Example query
# ProductionOfGroupInstructionsAgent("Prepare the reporting instructions for subsidiaries for the upcoming month-end close, including deadlines, templates, and special guidance for recent divestitures.")



# Load the knowledge base (Markdown file with compliance rules and standards)
kb3 = MarkdownKnowledgeBase(path="Knowledge/compliance_validation_kb.md")

# Initialize the agent
ValidationOfComplianceAgent = Agent(
    name="ValidationOfCompliance",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[ FileTools(), ExaTools()],  # FileTools can access subsidiary submissions if needed
    reasoning=True,
    knowledge=kb3,
    stream=True,
    show_tool_calls=True,
    
    description="""
    This agent validates that subsidiary financial submissions comply with group accounting standards.
    It checks local GAAP adjustments, FX translation, intercompany eliminations, and adoption of new policies.
    It flags deviations and suggests corrective actions.
    """,
    instructions="""
    - Always reference the knowledge base for compliance rules and standards first.
    - Compare subsidiary submissions to group policies, IFRS, and approved FX rates.
    - Flag deviations and provide suggested corrective actions.
    - Summarize adoption of new accounting standards across subsidiaries.
    - If data is missing or inconsistent, advise on reconciliation steps.

    Note: If you need to search the web for more details, use ExaTools().
    """
)


# Example query
# ValidationOfComplianceAgent.print_response("let's say we found a mismatches in intercompany FX, how can we solve it?.")

# Load the knowledge base for consolidation rules and adjustments
kb4 = MarkdownKnowledgeBase(path="Knowledge/consolidation_kb.md")

# Initialize the agent
CollectionAndConsolidationAgent = Agent(
    name="CollectionAndConsolidation",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[ FileTools()],  # FileTools to read subsidiary submissions and templates
    reasoning=True,
    stream=True,
    show_tool_calls=True,
    knowledge=kb4,
    description="""
    This agent gathers financial data from all subsidiaries, validates submissions, 
    performs intercompany reconciliations, converts currencies, and posts group-level consolidation adjustments.
    """,
    instructions="""
    - Pull financial submissions from all subsidiaries or ERP systems.
    - Validate that submissions are complete and received before deadlines.
    - Match and eliminate intercompany balances and transactions.
    - Convert subsidiary results into the group's reporting currency using approved FX rates.
    - Post group-level consolidation adjustments, including minority interest and investment eliminations.
    - Report any discrepancies or missing data.
    """
)


# Example query
# CollectionAndConsolidationAgent.print_response("what do we do if a subsidiary’s submission is incomplete?")

# Load knowledge base for control and validation rules
kb5 = MarkdownKnowledgeBase(path="Knowledge/consolidated_validation_kb.md")

# Initialize the agent
ControlAndValidationAgent = Agent(
    name="ControlAndValidationOfConsolidatedAccounts",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[ExaTools(),FileTools()],  # FileTools to access consolidated results
    # reasoning=True,
    stream=True,
    show_tool_calls=True,
    knowledge=kb5,
    description="""
    This agent performs final checks on consolidated accounts, including analytical review,
    IFRS/GAAP compliance, variance analysis, and audit preparation.
    """,
    instructions="""
    - Perform analytical review comparing actual results vs. prior period, budget, and forecast.
    - Validate IFRS/GAAP compliance for all financial statements.
    - Check completeness and correctness of disclosures.
    - Implement adjustments from audit findings.
    - Prepare supporting schedules and reports for auditors.
    - Flag significant variances or unusual items for further investigation.
    """
)


# Example query
# Sample consolidated data for Q2 (simplified example)
consolidated_data_q2 = {
    "P&L": {
        "Revenue": {"Actual": 1200000, "Budget": 1150000, "Prior": 1100000},
        "COGS": {"Actual": 700000, "Budget": 680000, "Prior": 650000},
        "Operating_Profit": {"Actual": 500000, "Budget": 470000, "Prior": 450000}
    },
    "Balance_Sheet": {
        "Assets": {"Actual": 2500000, "Prior": 2400000},
        "Liabilities": {"Actual": 1500000, "Prior": 1450000},
        "Equity": {"Actual": 1000000, "Prior": 950000}
    },
    "Cash_Flow": {
        "Operating": {"Actual": 300000, "Prior": 280000},
        "Investing": {"Actual": -50000, "Prior": -40000},
        "Financing": {"Actual": 20000, "Prior": 15000}
    },
    "Audit_Findings": [
        {"Issue": "Intercompany elimination missing for Subsidiary A", "AdjustmentRequired": True},
        {"Issue": "FX translation discrepancy for Subsidiary B", "AdjustmentRequired": True}
    ]
}

# Print response with the data included in the prompt
# ControlAndValidationAgent.print_response(
#     "Perform a control and validation check on the consolidated accounts for Q2, "
#     "highlight variances, ensure compliance, and prepare audit schedules. "
#     f"Here is the consolidated data to analyze: {consolidated_data_q2}"
# )

# Load knowledge base for closing process optimization
kb6 = MarkdownKnowledgeBase(path="Knowledge/closing_optimization_kb.md")

# Initialize the agent
ClosingOptimizationAgent = Agent(
    name="OptimizationOfClosingProcess",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[ FileTools()],  # FileTools to read historical close data, templates, and workflows
    reasoning=True,
    stream=True,
    show_tool_calls=True,
    knowledge=kb6,
    description="""
    This agent identifies bottlenecks in the closing process, recommends automation and workflow improvements,
    refines templates and instructions, and proposes continuous improvements for faster and more accurate reporting.
    """,
    instructions="""
    - Analyze historical close cycle data to identify recurring delays or bottlenecks.
    - Review templates, instructions, and workflows to find inefficiencies.
    - Recommend automation initiatives (e.g., submission tracking, automated validations).
    - Suggest improvements to training, interim close runs, and templates.
    - Produce a summary report highlighting bottlenecks, recommended actions, and expected time savings.
    """
)
# Sample historical close cycle data for testing
closing_cycle_data = {
    "Subsidiaries": ["France", "Germany", "Spain", "Italy"],
    "Months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "SubmissionTimes": {  # in days after period-end
        "France": [2, 3, 2, 4, 3, 2],
        "Germany": [3, 3, 4, 5, 3, 3],
        "Spain": [4, 5, 4, 6, 5, 4],
        "Italy": [2, 2, 3, 3, 2, 3]
    },
    "ErrorsReported": {
        "France": [1, 0, 2, 1, 0, 1],
        "Germany": [2, 1, 3, 2, 1, 1],
        "Spain": [3, 4, 2, 3, 2, 3],
        "Italy": [0, 1, 0, 1, 0, 1]
    },
    "IntercompanyDelays": {  # days needed for reconciliation
        "France": [1, 1, 2, 1, 1, 1],
        "Germany": [2, 2, 3, 2, 2, 2],
        "Spain": [3, 2, 3, 4, 3, 3],
        "Italy": [1, 1, 1, 1, 1, 1]
    },
    "TemplatesUsed": ["Standard v1", "Standard v1", "Standard v2", "Standard v2", "Standard v2", "Standard v2"]
}

# Pass the sample data along with the prompt
# ClosingOptimizationAgent.print_response(
#     "Analyze last 6 months of closing cycles, identify bottlenecks, suggest automation and process improvements, "
#     "and recommend template or training refinements. "
#     f"Here is the historical closing data to analyze: {closing_cycle_data}"
# )


# ---------------------------------------------------------
# Create a Routing Team Agent for Reporting Module
# ---------------------------------------------------------

ReportingTeam = Team(
    name="ReportingTeam",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    mode="route",
    members=[
        AssistanceToSubsidiariesAgent,
        ProductionOfGroupInstructionsAgent,
        ValidationOfComplianceAgent,
        CollectionAndConsolidationAgent,
        ControlAndValidationAgent,
        ClosingOptimizationAgent,
    ],
    
    description="""
    This is the Group Reporting Team Agent.
    It routes user requests to the appropriate specialized agent:
    - Assistance to Subsidiaries
    - Production of Group Instructions
    - Validation of Compliance
    - Collection and Consolidation
    - Control and Validation of Consolidated Accounts
    - Optimization of Closing Process
    """,
    instructions="""
    - Carefully analyze the user’s query and route it to the most relevant agent.
    - Only one agent should handle each request unless explicitly asked to collaborate.
    - If the query spans multiple domains (e.g., compliance and consolidation), clarify or
      decide the most relevant primary agent.
    - Provide responses as if the user is interacting directly with the correct agent.
    """
)

