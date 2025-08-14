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
    model=Gemini(id=id_gemini,api_key=api_key_gemini),
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
AccountInquiryBot.print_response("""
Customer Inquiry:
- Customer Name: John Smith
- Authentication Provided: Last 4 digits of SSN, birthdate
- Query: "Can you tell me my current checking account balance and the last three transactions?"

Additional Context:
- Account Balance: $3,250.75
- Recent Transactions:
    1. Grocery Store - $45.23 - 2025-08-05
    2. Gas Station - $32.10 - 2025-08-03
    3. Online Subscription - $12.99 - 2025-08-01

Task:
1. Verify authentication.
2. Provide a summary of the account balance and recent transactions.
3. Respond politely and clearly.
""")
