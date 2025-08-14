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



TransactionMonitorBot = Agent(
    name="Transaction Monitor Bot",
    # model=OpenAIChat(id=id_openai, api_key=api_key_openai),
    model=Gemini(id=id_gemini,api_key=api_key_gemini),
    description="""
An AI agent that monitors real-time transaction streams to detect anomalous or potentially fraudulent activity.
It analyzes transaction data, account profiles, device fingerprints, location info, and behavioral patterns.
It applies configurable anomaly thresholds and rule sets to flag suspicious transactions for immediate review.
""",
    instructions="""
You are TransactionMonitorBot.
Your tasks:
1. Analyze incoming transactions in real-time, comparing them against account profiles, device IDs, locations, and behavioral baselines.
2. Apply anomaly detection rules and thresholds to detect suspicious activity.
3. Assign a confidence score to each flagged transaction.
4. Generate alerts with clear reasoning explaining why the transaction was flagged.
5. Minimize false positives by considering contextual factors.
6. Prioritize alerts based on severity and potential risk.

Present your output as a structured alert report for each flagged transaction.
""",
    markdown=True,
    tools=[ FileTools()],
    reasoning=True,    
    show_tool_calls=True,
    stream=True,    

)

# TransactionMonitorBot.print_response("""
# Transaction Details:
# - Transaction ID: TXN123456
# - Account ID: ACC78910
# - Amount: $12,500
# - Transaction Type: Online Purchase
# - Location: New York, USA
# - Device Fingerprint: Device_ABC123
# - Time: 3:45 AM UTC
# - Account Profile: 
#     * Account holder usually transacts between $10 and $500.
#     * Typical transaction locations: San Francisco, Los Angeles.
#     * Device Fingerprints used previously: Device_XYZ789, Device_ABC123 (last used 6 months ago).
#     * Behavioral Pattern: Transactions mostly during business hours (9 AM to 6 PM local time).

# Task:
# 1. Analyze this transaction for any suspicious or anomalous behavior.
# 2. Assign a confidence score indicating the likelihood of fraud.
# 3. Provide a detailed explanation for any flags raised.
# 4. Suggest whether the transaction should be automatically blocked, reviewed, or allowed.
# """)


PatternRecognitionAgent = Agent(
    name="Pattern Recognition Agent",
    model=OpenAIChat(id=id_openai, api_key=api_key_openai),
    description="""
An AI agent that analyzes historical fraud cases and transaction sequences to identify complex fraud patterns.
It applies network analysis and feature engineering to improve fraud detection sensitivity and reduce false positives.
""",
    instructions="""
You are the Pattern Recognition Agent.
Your tasks:
1. Analyze historical transaction and fraud case data to identify recurring patterns and suspicious sequences.
2. Use network analysis to detect linked accounts or coordinated fraudulent activity.
3. Apply feature engineering techniques to extract meaningful fraud indicators.
4. Recommend adjustments to fraud detection rules to improve accuracy.
5. Balance detection sensitivity with false positive tolerance.

Present your findings and recommendations clearly, with examples of identified patterns.
""",
    markdown=True,
    tools=[ReasoningTools(), FileTools()]
)


# PatternRecognitionAgent.print_response("""
# Historical Fraud Cases Summary:
# - Case 1: Multiple small transactions just below $100 from different devices linked by IP addresses.
# - Case 2: Rapid succession of high-value transfers between accounts with similar names and addresses.
# - Case 3: Series of login attempts from geographically distant locations within short time spans.

# Tasks:
# 1. Identify common patterns and suspicious behaviors across these cases.
# 2. Suggest potential new fraud detection rules or features that could catch similar activity.
# 3. Evaluate how these patterns could inform anomaly thresholds and false positive management.
# 4. Provide examples of how network analysis could uncover linked fraudulent accounts.

# Please provide a detailed analysis and actionable recommendations.
# """)



InvestigationCoordinatorBot = Agent(
    name="Investigation Coordinator Bot",
    model=OpenAIChat(id=id_openai, api_key=api_key_openai),
    description="""
An AI agent that manages fraud investigation workflows by prioritizing alerts, routing cases to investigators,
and tracking resolution status. It enforces escalation rules and ensures timely case closure.
""",
    instructions="""
You are the Investigation Coordinator Bot.
Your tasks:
1. Receive fraud alerts with associated case details and priorities.
2. Evaluate investigator availability and expertise.
3. Route cases to appropriate investigators based on workload and priority.
4. Track case progress, deadlines, and escalate overdue or high-risk cases.
5. Maintain audit logs and provide summary reports of investigation statuses.
6. Recommend resource reallocation if bottlenecks occur.

Present your workflow decisions clearly, prioritizing efficiency and compliance.
""",
    markdown=True,
    tools=[ReasoningTools(), FileTools()]
)


# InvestigationCoordinatorBot.print_response("""
# Current Fraud Alerts:
# - Alert 1: Transaction TXN001, high priority, linked to potential identity theft.
# - Alert 2: Transaction TXN002, medium priority, suspicious login pattern.
# - Alert 3: Transaction TXN003, low priority, flagged for manual review.

# Investigator Availability:
# - Investigator A: Available, expertise in identity theft cases.
# - Investigator B: Busy, expertise in login security.
# - Investigator C: Available, general fraud investigations.

# Tasks:
# 1. Prioritize and assign the alerts to investigators based on priority and expertise.
# 2. Suggest escalation steps if any case is overdue or at risk.
# 3. Recommend any resource adjustments to balance workloads.
# 4. Provide a summary of current investigation statuses and next steps.

# Please respond with a clear case management plan.
# """)
