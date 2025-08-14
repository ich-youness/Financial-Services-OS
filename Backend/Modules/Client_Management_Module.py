from agno.agent import Agent
from agno.team.team import Team
from agno.models.openai import OpenAIChat
from agno.models.google import Gemini
from agno.tools.scrapegraph import ScrapeGraphTools
from agno.tools.file import FileTools
from agno.tools.exa import ExaTools
from agno.tools.reasoning import ReasoningTools
from agno.models.huggingface import HuggingFace
from agno.tools.yfinance import YFinanceTools
from agno.tools.calculator import CalculatorTools
from agno.models.mistral import MistralChat
from dotenv import load_dotenv
import os


load_dotenv()
id_gemini=os.getenv("id")
api_key_gemini=os.getenv("api_key")
id_openai = os.getenv("id_openai")
api_key_openai = os.getenv("api_key_openai")


RelationshipManagerAgent = Agent(
    name="Relationship Manager Agent",
    # model=OpenAIChat(id=id_openai, api_key=api_key_openai),
    model=Gemini(id=id_gemini,api_key=api_key_gemini),
    description="""
An AI-powered relationship manager that analyzes client data, interactions, and life events 
to generate personalized engagement strategies. Helps maintain high satisfaction and loyalty.
    """,
    instructions="""
You are the Relationship Manager Agent.
Your objectives:
1. Review client interaction history, account activity, and service requests.
2. Identify opportunities for proactive outreach or follow-up.
3. Suggest personalized engagement actions based on life events, preferences, and satisfaction trends.
4. Prioritize at-risk clients and recommend actions to improve retention.
5. Ensure communication is empathetic, relevant, and professional.

Always present results in a clear, actionable engagement plan format.
    """,
    markdown=True,
    tools=[FileTools(), ],
    reasoning=True,    
    show_tool_calls=True,
    stream=True,
)

# RelationshipManagerAgent.print_response("""
# Client: Sarah Johnson
# Interaction History: Last spoke with RM 4 months ago; submitted service request for credit card replacement last month.
# Account History: Long-term client, high-value accounts, regular investment contributions.
# Life Events: Recently purchased a new home (per mortgage activity).
# Satisfaction Score: 7/10 (last survey)

# Task: 
# 1. Analyze this client’s data and identify the best next touchpoint.
# 2. Recommend the timing, channel, and key talking points for the outreach.
# 3. Include any personalized offers or services that could be relevant.
# """)


UpsellIdentifierBot = Agent(
    name="Upsell Identifier Bot",
    # model=OpenAIChat(id=id_openai, api_key=api_key_openai),
    
    description="""
An AI agent that identifies cross-sell and upsell opportunities for clients 
based on account data, life stage, product usage, and peer benchmarks.
    """,
    instructions="""
You are the Upsell Identifier Bot.
Your objectives:
1. Review client account data, product usage, and eligibility criteria.
2. Compare the client's profile to similar clients to identify gaps or potential opportunities.
3. Score each opportunity based on potential value, likelihood of acceptance, and timing.
4. Recommend the top opportunities with a suggested pitch approach.
5. Ensure recommendations comply with suitability rules and avoid overly aggressive sales tactics.

Always present recommendations in a concise report format with reasoning.
    """,
    markdown=True,
    tools=[FileTools(), ],
    reasoning=True,    
    show_tool_calls=True,
    stream=True,
)

# UpsellIdentifierBot.print_response("""
# Client: David Lee
# Age: 35
# Current Products: Checking account, basic credit card, 401(k) with employer match
# Recent Activity: Large direct deposit from a new job, increased debit card spending, no travel card usage.
# Peer Benchmark: 70% of similar clients use premium credit cards with travel rewards.
# Eligibility: Pre-approved for Platinum Travel Rewards Card, no outstanding credit issues.

# Task:
# 1. Identify potential upsell opportunities for this client.
# 2. Score each opportunity based on revenue potential and conversion likelihood.
# 3. Suggest timing and messaging for the offer.
# """)


OnboardingGuideAgent = Agent(
    name="Onboarding Guide Agent",
    # model=OpenAIChat(id=id_openai, api_key=api_key_openai),

    description="""
An AI onboarding assistant that ensures new clients complete all required steps
for account setup, identity verification, and product activation in compliance with regulations.
    """,
    instructions="""
You are the Onboarding Guide Agent.
Your objectives:
1. Review submitted KYC documents, account applications, and product selections.
2. Validate that all information is complete, accurate, and compliant with jurisdiction rules.
3. Identify any missing steps, documents, or inconsistencies.
4. Provide a clear, ordered onboarding plan to complete the process.
5. Flag potential compliance or approval issues before account activation.

Always return results in a structured checklist format with next steps.
    """,
    markdown=True,
    tools=[FileTools(), ],
    reasoning=True,    
    show_tool_calls=True,
    stream=True,
)

OnboardingGuideAgent.print_response("""
Client: Emily Parker
Jurisdiction: US
Submitted Documents: Passport copy, utility bill (address verification)
Account Application: Individual brokerage account, margin enabled
Product Selections: US equity trading, options trading
Funding Source: Linked checking account (verification pending)
Missing: Social Security Number

Task:
1. Review the onboarding status.
2. Identify missing steps and potential compliance issues.
3. Provide a clear checklist for completion.
""")
