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

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.file import FileTools
from agno.tools.reasoning import ReasoningTools
from dotenv import load_dotenv
import os

load_dotenv()
id_openai = os.getenv("id_openai")
api_key_openai = os.getenv("api_key_openai")

AccountInquiryBot = Agent(
    name="Account Inquiry Bot",
    # model=OpenAIChat(id=id_openai, api_key=api_key_openai),
    # model=Gemini(id=id_gemini,api_key=api_key_gemini),
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    description="""
An AI agent that handles customer account inquiries by answering questions about account data,
transaction history, and FAQs. It verifies customer identity securely and escalates complex queries as needed.
""",
    instructions="""
You are the Account Inquiry Bot.

Your responsibilities:
1. Authenticate the customer based on provided information before sharing sensitive details.
2. Answer queries regarding account balances, recent transactions, and product details.
3. Use the FAQ database to respond to common questions efficiently.
4. Detect and escalate security-sensitive or complex issues to human agents.
5. Provide clear, polite, and accurate responses in all communications.

Always ensure customer data privacy and security in your responses.
""",
    markdown=True,
    tools=[FileTools(), ],
    reasoning=True,

)

# AccountInquiryBot.print_response("""
# Customer Inquiry:
# - Customer Name: John Smith
# - Authentication Provided: Last 4 digits of SSN, birthdate
# - Query: "Can you tell me my current checking account balance and the last three transactions?"

# Additional Context:
# - Account Balance: $3,250.75
# - Recent Transactions:
#     1. Grocery Store - $45.23 - 2025-08-05
#     2. Gas Station - $32.10 - 2025-08-03
#     3. Online Subscription - $12.99 - 2025-08-01

# Task:
# 1. Verify authentication.
# 2. Provide a summary of the account balance and recent transactions.
# 3. Respond politely and clearly.
# """)



TransactionProcessorAgent = Agent(
    name="Transaction Processor Agent",
    # model=Gemini(id=id_gemini, api_key=api_key_gemini),
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    description="""
An AI agent that processes customer transaction requests while ensuring compliance with
account limits, restrictions, and approval requirements. It validates each request and
provides confirmations or error messages.
""",
    instructions="""
You are the Transaction Processor Agent.

Your responsibilities:
1. Validate transaction requests against account balances and daily limits.
2. Check for any restrictions or approval requirements before processing.
3. Ensure the transaction request is complete and properly formatted.
4. If validation passes, confirm the transaction execution.
5. If validation fails, clearly explain why and suggest corrective actions.
6. Notify customers of successful or failed transactions using configured templates.
7. Log all processed transactions for auditing and compliance.

Always follow security protocols to protect customer data.
""",
    markdown=True,
    tools=[FileTools(), CalculatorTools(), ReasoningTools()],
    reasoning=True,
)


# TransactionProcessorAgent.print_response("""
# Transaction Request:
# - Customer Name: John Smith
# - Account Balance: $5,000
# - Requested Transfer: $2,500 to Account #XXXX4321
# - Daily Transfer Limit: $3,000
# - No pending restrictions

# Task:
# 1. Validate the request.
# 2. Process if valid.
# 3. Respond with confirmation message.
# """)


FinancialEducatorBot = Agent(
    name="Financial Educator Bot",
    # model=Gemini(id=id_gemini, api_key=api_key_gemini),
    model=MistralChat(id="magistral-medium-2507", api_key=os.getenv("MISTRAL_API")),
    description="""
An AI agent that educates customers about financial literacy based on their profile,
goals, and knowledge level. It recommends personalized learning paths and tracks progress.
""",
    instructions="""
You are the Financial Educator Bot.

Your responsibilities:
1. Review the customer's financial profile and goals.
2. Assess their current knowledge level using provided assessments.
3. Recommend tailored educational content and learning paths.
4. Provide explanations of financial concepts in simple, engaging language.
5. Track progress and suggest next steps to improve knowledge.
6. Offer tips, best practices, and strategies for reaching financial goals.
7. Use engagement metrics to adapt future recommendations.

Always keep advice educational — do not give specific investment recommendations.
""",
    markdown=True,
    tools=[FileTools(), ReasoningTools()],
    reasoning=True,
)


# FinancialEducatorBot.print_response("""
# Customer Profile:
# - Name: Sarah Lee
# - Goal: Save for a home down payment in 5 years
# - Knowledge Level: Beginner
# - Recent Progress: Completed 3 lessons on budgeting and savings

# Task:
# 1. Recommend next lessons for Sarah.
# 2. Provide encouragement and motivation.
# """)


customer_service_router_team = Team(
    name="Customer Service Router Team",
    mode="route",
    model=Gemini(id=id_gemini, api_key=api_key_gemini),
    members=[AccountInquiryBot, TransactionProcessorAgent, FinancialEducatorBot],
    show_tool_calls=True,
    markdown=True,
    description="You are a customer service query router that directs questions to the appropriate specialized agent.",
    instructions=[
        "Identify the main topic of the user's query and direct it to the relevant agent.",
        "If the query is about account balances, transaction history, or FAQs related to account details, route to AccountInquiryBot.",
        "If the query is about processing transaction requests, validating transfers, or handling account limits and restrictions, route to TransactionProcessorAgent.",
        "If the query is about financial education, learning paths, or guidance on financial concepts and goals, route to FinancialEducatorBot.",
        "If the query does not match any of the above categories, respond in English with: 'I can only handle queries related to account inquiries, transaction processing, or financial education. Please rephrase your question accordingly.'",
        "Always analyze the query's content before routing to an agent.",
        "For ambiguous queries, ask for clarification before routing.",
    ],
    show_members_responses=True,
)