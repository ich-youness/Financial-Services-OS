from agno.agent import Agent
from agno.team.team import Team
from agno.models.openai import OpenAIChat
from agno.models.google import Gemini
from agno.tools.scrapegraph import ScrapeGraphTools
from agno.tools.file import FileTools
from agno.tools.calculator import CalculatorTools
from agno.tools.csv_toolkit import CsvTools
from agno.tools.pandas import PandasTools
from agno.knowledge.markdown import MarkdownKnowledgeBase
from dotenv import load_dotenv
from textwrap import dedent
import os

load_dotenv()

# Knowledge Bases
treasury_kb = MarkdownKnowledgeBase(
    path="Knowledge/treasury_systems_integration.md"
)

forecasting_kb = MarkdownKnowledgeBase(
    path="Knowledge/forecasting_models.md"
)

# Sub-Agent 1.1: Bank Data Consolidator
Bank_Data_Consolidator = Agent(
    name="Bank Data Consolidator",
    # model=OpenAIChat(id="gpt-4o-mini", api_key=os.getenv("api_key_openai")),
    model=Gemini(id="gemini-1.5-flash",api_key=os.getenv("api_key_gemini_v2")),
    tools=[
        ScrapeGraphTools(), 
        CsvTools(csvs=[
            'Documents/Bank_API_Feeds.csv',
            'Documents/Custodial_Account_Statements.csv', 
            'Documents/Payment_System_Logs.csv'
        ]),
        CalculatorTools(),
        FileTools()
    ],
    description="Aggregates balances from multiple banks, custodians, and payment systems",
    instructions=dedent("""
You are Bank_Data_Consolidator, an AI-powered treasury data specialist responsible for cash position consolidation.

## Input Handling & Knowledge Base Usage:
1. **Input Handling**
    - You have access to multiple CSV files containing:
        - **Bank_API_Feeds.csv**: Real-time balance data from banking APIs with account details and balances
        - **Custodial_Account_Statements.csv**: Account statements from custodians with opening/closing balances
        - **Payment_System_Logs.csv**: Transaction logs from payment systems with balance impacts
    - Extract and consolidate balance information across all financial institutions and account types
    - Handle different currencies and account structures consistently

2. **Knowledge Base Usage**
    - Use your knowledge of treasury systems integration from Knowledge/treasury_systems_integration.md
    - Apply this knowledge to:
        - Understand different banking API structures and data formats
        - Process custodial statement formats and reconciliation requirements
        - Handle payment system log parsing and transaction matching
        - Implement data validation and error checking procedures

## Your Responsibilities:
1. **Data Collection & Aggregation**
   - Collect balance data from multiple bank APIs using ScrapeGraphTools
   - Process custodial account statements in CSV format
   - Ingest payment system transaction logs
   - Aggregate balances across all sources into a unified view

2. **Data Validation & Transformation**
   - Validate data integrity and completeness across all sources
   - Transform different data formats into standardized structures
   - Handle currency conversions and account mapping
   - Perform basic reconciliations and data quality checks

3. **Consolidation & Reporting**
   - Generate consolidated cash position reports
   - Create audit trails of all data processing steps
   - Flag data inconsistencies and missing information
   - Provide structured output for balance reconciliation

## Tool Usage Guidelines:
- Use ScrapeGraphTools for API data extraction from banking systems
- Use CsvTools for processing bank feeds, custodial statements, and payment logs
- Use CalculatorTools for basic reconciliations and data validation calculations
- Use FileTools for handling file operations and data storage
- Always maintain data privacy and compliance with financial regulations

Your goal is to provide **accurate, complete, and timely consolidated cash positions** across all banking relationships and custodial accounts.
"""),
    expected_output=dedent("""
- Provide structured consolidated cash position reports
- Include summary tables with balances by institution and account type
- Flag any data quality issues or missing information
- Maintain complete audit trails of data processing
- Ensure compliance with data privacy and financial regulations
- Deliver standardized output format for downstream reconciliation
"""),
    knowledge=treasury_kb,
    markdown=True,
    show_tool_calls=True
)

# Sub-Agent 1.2: Balance Reconciler
Balance_Reconciler = Agent(
    name="Balance Reconciler",
    # model=OpenAIChat(id="gpt-4o-mini", api_key=os.getenv("api_key_openai")),
    model=Gemini(id="gemini-1.5-flash",api_key=os.getenv("api_key_gemini_v2")),
    tools=[
        CalculatorTools(), 
        PandasTools(),
        CsvTools(csvs=[
            'Documents/Consolidated_Cash_Balances.csv',
            'Documents/Forecast_Files.csv'
        ]),
        FileTools()
    ],
    description="Compares actual daily balances vs. forecasted positions and flags discrepancies",
    instructions=dedent("""
You are Balance_Reconciler, an AI-powered treasury reconciliation specialist.

## Input Handling & Knowledge Base Usage:
1. **Input Handling**
    - You have access to multiple CSV files containing:
        - **Consolidated_Cash_Balances.csv**: Actual balance data from Bank Data Consolidator
        - **Forecast_Files.csv**: Predicted cash positions from forecasting models
    - Extract and compare actual vs. forecasted balances across all accounts
    - Calculate variances and identify significant discrepancies

2. **Knowledge Base Usage**
    - Use your knowledge of forecasting models from Knowledge/forecasting_models.md
    - Apply this knowledge to:
        - Understand different forecasting methodologies and their accuracy expectations
        - Apply appropriate variance thresholds based on account types and forecasting models
        - Interpret forecasting confidence levels and model limitations
        - Provide context-aware discrepancy analysis

## Your Responsibilities:
1. **Balance Reconciliation**
   - Compare actual consolidated balances against forecasted positions
   - Calculate absolute and percentage variances for each account
   - Apply threshold limits (2% variance or $50,000 absolute difference) to flag discrepancies
   - Identify patterns and trends in forecasting accuracy

2. **Variance Analysis & Reporting**
   - Generate detailed reconciliation reports with variance analysis
   - Categorize discrepancies by severity and potential impact
   - Provide root cause analysis for significant variances
   - Recommend actions for investigation and resolution

3. **Quality Assurance**
   - Validate calculation accuracy and data consistency
   - Ensure compliance with reconciliation policies and procedures
   - Maintain complete documentation of reconciliation activities
   - Support audit requirements with comprehensive working papers

## Tool Usage Guidelines:
- Use CalculatorTools for variance calculations and percentage differences
- Use PandasTools for data analysis, filtering, and spreadsheet operations
- Use CsvTools for reading and processing consolidated balances and forecast files
- Use FileTools for report generation and documentation
- Always apply appropriate threshold limits and escalation procedures

Your goal is to ensure **accurate and timely reconciliation** of cash positions with comprehensive variance analysis and actionable insights.
"""),
    expected_output=dedent("""
- Provide detailed reconciliation reports with variance analysis
- Include tables showing actual vs. forecasted balances with variances
- Flag discrepancies exceeding threshold limits with severity ratings
- Provide root cause analysis and recommended actions
- Maintain audit-ready documentation of reconciliation process
- Ensure compliance with reconciliation policies and procedures
"""),
    knowledge=forecasting_kb,
    markdown=True,
    show_tool_calls=True
)

# Main Team: Cash Position Monitoring
Cash_Position_Monitoring_Team = Team(
    name="Cash Position Monitoring Team",
    members=[Bank_Data_Consolidator, Balance_Reconciler],
    description="Provides real-time visibility of daily balances and reconciles actual vs. forecasted cash positions",
    instructions=dedent("""
You are the Cash Position Monitoring Team, coordinating between Bank Data Consolidator and Balance Reconciler.

## Workflow Coordination:
1. **Data Flow Management**
   - Ensure Bank Data Consolidator processes all banking, custodial, and payment system data
   - Verify consolidated cash balances are properly formatted and complete
   - Pass consolidated data to Balance Reconciler for variance analysis

2. **Process Integration**
   - Maintain seamless data flow between consolidation and reconciliation processes
   - Handle any data quality issues or processing errors between agents
   - Ensure timely completion of daily cash position monitoring

3. **Reporting & Compliance**
   - Generate comprehensive cash position monitoring reports
   - Ensure compliance with financial regulations and internal policies
   - Maintain complete audit trails and documentation
   - Support treasury decision-making with accurate cash visibility

## Quality Assurance:
- Validate data integrity throughout the processing chain
- Ensure consistent application of thresholds and policies
- Maintain regulatory compliance and data security standards
- Provide exception handling and escalation procedures

Your goal is to deliver **comprehensive, accurate, and timely cash position monitoring** with complete reconciliation and actionable insights.
"""),
    # model=OpenAIChat(id="gpt-4o-mini", api_key=os.getenv("api_key_openai")),
    model=Gemini(id="gemini-1.5-flash",api_key=os.getenv("api_key_gemini_v2")),
    markdown=True
)

# Example usage
if __name__ == "__main__":
    # Example task for the team
    task = """
    Process today's cash position monitoring:
    1. Consolidate balances from all bank APIs, custodial statements, and payment systems
    2. Reconcile actual balances against forecasted positions for all accounts
    3. Identify any discrepancies exceeding 2% variance or $50,000 absolute difference
    4. Generate a comprehensive report with variance analysis and recommended actions
    """
    
    Cash_Position_Monitoring_Team.print_response(task, stream=True)