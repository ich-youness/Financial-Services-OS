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


ComplianceOfficerAgent = Agent(
    name="Compliance Officer Agent",
    # model=OpenAIChat(id="gpt-4o-mini", api_key=api_key_openai),
    model=Gemini(id=id_gemini,api_key=api_key_gemini),
    description="""
An AI agent that monitors regulatory updates, internal policies, audit findings, and control assessments.
It recommends remediation actions, schedules monitoring tasks, and tracks compliance status and incidents.
""",
    instructions="""
You are the Compliance Officer Agent.

Your responsibilities:
1. Monitor and interpret regulatory updates and internal audit findings.
2. Evaluate the effectiveness of internal controls and compliance measures.
3. Recommend remediation steps for any compliance gaps or incidents.
4. Schedule monitoring activities and reporting deadlines.
5. Track the status of remediation efforts and incident resolutions.
6. Present clear and actionable compliance reports for management.

Always deliver your output as structured remediation plans, schedules, or status reports.
""",
    markdown=True,
    tools=[ FileTools()],
    reasoning=True,    
    show_tool_calls=True,
    stream=True,
)


ComplianceOfficerAgent.print_response("""
Regulatory Updates:
- New data privacy rules enacted effective next quarter.
- Recent audit found incomplete documentation in customer onboarding.

Internal Policies:
- Customer data must be encrypted in transit and at rest.
- All onboarding documents must be verified within 48 hours.

Control Assessments:
- Encryption controls operational but with minor logging gaps.
- Onboarding document verification process delayed by average 72 hours.

Incident Reports:
- One recent data breach due to misplaced device.

Tasks:
1. Identify compliance gaps based on the above inputs.
2. Recommend remediation steps with timelines.
3. Suggest monitoring schedules and reporting priorities.
4. Provide a status overview for senior management.
""")


ReportGeneratorBot = Agent(
    name="Report Generator Bot",
    # model=OpenAIChat(id=id_openai, api_key=api_key_openai),
    model=Gemini(id=id_gemini,api_key=api_key_gemini),
    description="""
An AI agent that automates the generation of regulatory reports by aggregating transaction data,
validating it against regulatory templates, and ensuring reports meet submission deadlines and quality standards.
""",
    instructions="""
You are the Report Generator Bot.

Your responsibilities:
1. Aggregate transaction and audit data relevant to the reporting period.
2. Validate data consistency and completeness according to regulatory templates.
3. Format reports clearly and accurately as per specified reporting requirements.
4. Check for any data validation errors or inconsistencies.
5. Prepare reports for timely submission and flag any potential compliance issues.
6. Provide summaries of report contents and validation results.

Output your reports and validation summaries in a clear, structured format.
""",
    markdown=True,
    tools=[FileTools(), ReasoningTools()]
)
ReportGeneratorBot.print_response("""
Transaction Data Summary:
- Total transactions: 15,000
- High-risk transactions flagged: 45
- Suspicious activities reported: 3

Regulatory Template:
- Requires monthly summary of total transactions and flagged cases.
- Data fields must include transaction ID, date, amount, flag reason.
- Reports must be submitted by the 10th of each month.

Reporting Period:
- March 2025

Tasks:
1. Aggregate and validate transaction data against the regulatory template.
2. Generate a compliant monthly report for March 2025.
3. Identify any data inconsistencies or missing fields.
4. Provide a validation summary and next steps for corrections if needed.
""")


AuditPreparationAgent = Agent(
    name="Audit Preparation Agent",
    # model=OpenAIChat(id=id_openai, api_key=api_key_openai),
    model=Gemini(id=id_gemini,api_key=api_key_gemini),
    description="""
An AI agent that supports audit preparation by managing documentation requests, control evidence,
testing samples, and audit findings. It organizes tasks to ensure audits proceed smoothly and compliantly.
""",
    instructions="""
You are the Audit Preparation Agent.

Your responsibilities:
1. Track audit requests and documentation requirements.
2. Organize and validate control evidence and testing samples.
3. Prepare response templates for auditors and stakeholders.
4. Monitor audit progress and track findings history.
5. Identify gaps or delays in audit preparations.
6. Provide checklists and next steps to ensure audit readiness.

Present your output as clear preparation plans, checklists, or status summaries.
""",
    markdown=True,
    tools=[FileTools(), ReasoningTools()]
)


AuditPreparationAgent.print_response("""
Audit Request:
- Upcoming regulatory audit scheduled in 3 weeks.
- Required documentation: control policies, transaction logs, employee training records.

Current Status:
- Control policies updated last month.
- Transaction logs complete through last week.
- Employee training records partially updated (70%).

Tasks:
1. Assess readiness for the upcoming audit.
2. Identify any missing or incomplete documentation.
3. Provide a checklist for final preparations.
4. Recommend priorities and timelines to close gaps.
""")
