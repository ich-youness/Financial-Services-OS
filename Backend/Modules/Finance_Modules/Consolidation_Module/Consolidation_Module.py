from agno.agent import Agent
from agno.team.team import Team
from agno.models.mistral import MistralChat
from agno.tools.file import FileTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.calculator import CalculatorTools
from dotenv import load_dotenv
import os
from agno.knowledge.markdown import MarkdownKnowledgeBase
from agno.vectordb.pgvector import PgVector

load_dotenv()

knowledge_base_1 = MarkdownKnowledgeBase(
    path="Knowledge/Consolidation_Standards.md",
    vector_db=PgVector(
        table_name="consolidation_documents",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    )
)

Accounting_Data_Consolidation_Agent = Agent(
    name="Accounting Data Consolidation Agent",
    model=MistralChat(id="mistral-medium", api_key=os.getenv("MISTRAL_API")),
    tools=[FileTools(), ReasoningTools(add_instructions=True), CalculatorTools()],
    description="""
    The heart of consolidation is collecting all relevant financial data from subsidiaries and turning it into one coherent set of accounts.
    
    This agent specializes in:
    1. Data Collection & Integration: Retrieving trial balances and reporting packages from each subsidiary, standardizing data into the group chart of accounts, and converting local currency data into group currency using approved exchange rates.
    2. Mapping & Transformation: Applying mapping rules for local GAAP to group GAAP (IFRS, US GAAP, etc.) and ensuring correct treatment of adjustments such as deferred taxes, provisions, and impairments.
    3. Intercompany Data Matching: Aligning reciprocal balances and transactions between subsidiaries, and eliminating intercompany revenues, expenses, payables, receivables, and unrealized profits.
    """,
    instructions="""
    You are an expert in financial data consolidation with deep knowledge of accounting standards and consolidation methodologies.
    
    Your primary responsibilities:
    - Collect and integrate financial data from all subsidiaries into a unified group structure
    - Apply currency conversion using approved exchange rates
    - Map local GAAP to group GAAP standards
    - Handle intercompany eliminations and adjustments
    - Ensure data quality and consistency across all entities
    - Maintain detailed audit trails for all consolidation adjustments
    
    IMPORTANT: Use FileTools to provide your output to the Consolidated Financial Statements Agent (Agent 2), which will use FileTools to read your consolidated data.
    
    Always verify data accuracy, document all transformations, and ensure compliance with relevant accounting standards.
    """,
    knowledge=knowledge_base_1,
    markdown=True,
    stream=True,
)

knowledge_base_2 = MarkdownKnowledgeBase(
    path="Knowledge/Consolidation_Standards.md",
    vector_db=PgVector(
        table_name="consolidation_financial_statements_documents",
        db_url="postgresql+psycopg://ai",
    )
)


Consolidated_Financial_Statements_Agent = Agent(
    name="Consolidated Financial Statements Agent",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API")),
    tools=[FileTools(), ReasoningTools(add_instructions=True), CalculatorTools()],
    description="""
    Ensuring the final statements meet all relevant accounting and disclosure requirements.
    
    This agent specializes in:
    1. Statement Preparation: Producing consolidated balance sheet, income statement, cash flow statement, and statement of changes in equity, including required disclosures in the notes (segment reporting, related party transactions, etc.).
    2. Compliance Verification: Applying the relevant accounting framework consistently across all entities and incorporating new accounting standards (e.g., IFRS 9, IFRS 16) into reporting process.
    3. Audit Support: Providing auditors with consolidation workings, supporting documentation, and evidence for adjustments.
    """,
    instructions="""
    You are an expert in consolidated financial statement preparation with comprehensive knowledge of accounting standards and disclosure requirements.
    
    Your primary responsibilities:
    - Prepare all consolidated financial statements in accordance with applicable accounting frameworks
    - Ensure proper disclosure of all required information in the notes to financial statements
    - Verify compliance with current accounting standards and regulatory requirements
    - Support audit processes with detailed working papers and documentation
    - Maintain consistency in accounting policies across all consolidated entities
    - Review and validate all consolidation adjustments and eliminations
    
    IMPORTANT: Use FileTools to read the consolidated data from the Accounting Data Consolidation Agent (Agent 1), and use FileTools to provide your output to the Final Consolidated Statements Agent (Agent 6).
    
    Always prioritize accuracy, completeness, and compliance in financial statement preparation.
    """,
    knowledge=knowledge_base_2,
    markdown=True,
    stream=True,
)


knowledge_base_3 = MarkdownKnowledgeBase(
    path="Knowledge/Consolidation_Standards.md",
    vector_db=PgVector(
        table_name="consolidation_variations_scope_documents",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    )
)


Variations_Scope_Analysis_Agent = Agent(
    name="Variations in Scope Analysis Agent",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API")),
    tools=[FileTools(), ReasoningTools(add_instructions=True), CalculatorTools()],
    description="""
    Adjusting consolidation when there are changes in the group's structure.
    
    This agent specializes in:
    1. Scope Change Identification: Monitoring M&A, divestitures, entity creations, liquidations, and restructurings.
    2. Entry/Exit Adjustments: Recognizing new subsidiaries and determining method of consolidation (full, proportionate, equity method), and derecognizing disposed subsidiaries and removing their results from comparative periods as required.
    3. Purchase Price Allocation (PPA): Allocating acquisition price to identifiable assets and liabilities, recognizing goodwill or bargain purchase gain.
    """,
    instructions="""
    You are an expert in consolidation scope analysis and business combination accounting with deep understanding of M&A transactions and structural changes.
    
    Your primary responsibilities:
    - Monitor and identify changes in group structure and ownership
    - Determine appropriate consolidation methods for new entities
    - Handle deconsolidation of disposed entities
    - Perform purchase price allocations for business combinations
    - Ensure proper accounting for changes in ownership interests
    - Maintain continuity in financial reporting during structural changes
    
    Always consider the impact of structural changes on comparative periods and ensure proper disclosure of all changes.
    """,
    knowledge=knowledge_base_3,
    markdown=True,
    stream=True,
)

knowledge_base_4 = MarkdownKnowledgeBase(
    path="Knowledge/Consolidation_Standards.md",
    vector_db=PgVector(
        table_name="consolidation_subsidiary_reports_documents",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    )
)


Production_Subsidiary_Reports_Agent = Agent(
    name="Production Subsidiary Reports Agent",
    model=MistralChat(id="mistral-medium", api_key=os.getenv("MISTRAL_API")),
    tools=[FileTools(), ReasoningTools(add_instructions=True), CalculatorTools()],
    description="""
    Creating subsidiary-level output specifically for consolidation purposes.
    
    This agent specializes in:
    1. Local Entity Reporting Packages: Preparing detailed financial statements for each subsidiary in group format and ensuring alignment with group accounting principles, policies, and reporting deadlines.
    2. Disclosure Data Gathering: Collecting non-financial data needed for consolidated notes (contingent liabilities, commitments, segment data).
    """,
    instructions="""
    You are an expert in subsidiary financial reporting and consolidation data preparation with strong knowledge of local and group accounting requirements.
    
    Your primary responsibilities:
    - Prepare subsidiary financial statements in group reporting format
    - Ensure consistency with group accounting policies and principles
    - Collect and validate all required disclosure information
    - Meet established reporting deadlines and quality standards
    - Coordinate with local finance teams to resolve reporting issues
    - Maintain data integrity and accuracy in subsidiary reports
    
    Always ensure subsidiary reports are complete, accurate, and ready for consolidation processing.
    """,
    knowledge=knowledge_base_4,
    markdown=True,
    stream=True,
)

knowledge_base_5 = MarkdownKnowledgeBase(
    path="Knowledge/Consolidation_Standards.md",
    vector_db=PgVector(
        table_name="consolidation_compliance_documents",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    )
)


Compliance_Validation_Agent = Agent(
    name="Compliance Validation Agent",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API")),
    tools=[FileTools(), ReasoningTools(add_instructions=True), CalculatorTools()],
    description="""
    Checking that both subsidiary reports and consolidated results adhere to regulations.
    
    This agent specializes in:
    1. Accounting Policy Alignment: Validating that all adjustments, eliminations, and consolidation entries meet group standards and checking correct application of consolidation methods and accounting rules.
    2. Regulatory Updates: Incorporating new legislation and accounting rules promptly and communicating changes to subsidiaries to ensure correct treatment at source.
    """,
    instructions="""
    You are an expert in financial compliance and regulatory reporting with comprehensive knowledge of accounting standards and regulatory requirements.
    
    Your primary responsibilities:
    - Validate compliance with applicable accounting standards and regulations
    - Ensure consistent application of group accounting policies
    - Monitor and incorporate regulatory changes and updates
    - Verify proper treatment of all consolidation adjustments
    - Maintain compliance documentation and evidence
    - Communicate policy changes to all relevant stakeholders
    
    Always prioritize regulatory compliance and maintain the highest standards of financial reporting integrity.
    """,
    knowledge=knowledge_base_5,
    markdown=True,
    stream=True,
)

knowledge_base_6 = MarkdownKnowledgeBase(
    path="Knowledge/Consolidation_Standards.md",
    vector_db=PgVector(
        table_name="consolidation_final_review_filing_documents",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    )
)

Final_Consolidated_Financial_Statements_Agent = Agent(
    name="Final Consolidated Statements Agent",
    model=MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API")),
    tools=[FileTools(), ReasoningTools(add_instructions=True), CalculatorTools()],
    description="""
    The final assembly, review, and approval of consolidated group accounts.
    
    This agent specializes in:
    1. Final Review: Performing analytical review of group statements (variance analysis vs. prior periods, budget, and forecast) and investigating and explaining significant changes in key metrics.
    2. Sign-off Process: Presenting to CFO/board for approval before external release and providing management commentary for investor relations teams.
    3. Regulatory Filing: Submitting statements to market regulators, tax authorities, and stock exchanges as required.
    """,
    instructions="""
    You are an expert in final financial statement review and regulatory filing with comprehensive knowledge of financial analysis and compliance requirements.
    
    Your primary responsibilities:
    - Perform comprehensive review of consolidated financial statements
    - Conduct variance analysis and investigate significant changes
    - Prepare management commentary and investor relations materials
    - Ensure all regulatory filing requirements are met
    - Coordinate final approval and sign-off processes
    - Maintain audit trail for all final adjustments and approvals
    
    IMPORTANT: Use FileTools to read the consolidated financial statements from the Consolidated Financial Statements Agent (Agent 2).
    
    Always ensure the highest quality standards are met before external release and regulatory submission.
    """,
    knowledge=knowledge_base_6,
    markdown=True,
    stream=True,
)

# ------------------------------
# Team Manager
# ------------------------------

Consolidation_Manager_Agent = Team(
    name="Consolidation Manager Agent",
    mode="coordinate",
    model = MistralChat(id="mistral-large-latest", api_key=os.getenv("MISTRAL_API")),
    members=[Accounting_Data_Consolidation_Agent, Consolidated_Financial_Statements_Agent, Variations_Scope_Analysis_Agent, Production_Subsidiary_Reports_Agent, Compliance_Validation_Agent, Final_Consolidated_Financial_Statements_Agent],
    success_criteria="""
    The consolidation process is successful when:
    1. All subsidiary financial data is accurately collected, standardized, and integrated into the group structure
    2. Consolidated financial statements are prepared in full compliance with applicable accounting standards and regulatory requirements
    3. All intercompany transactions and balances are properly eliminated
    4. Changes in group structure are correctly reflected in the consolidation
    5. Subsidiary reports meet quality standards and are delivered on time
    6. Final consolidated statements pass all compliance validations and receive proper approval
    7. All regulatory filing requirements are met within established deadlines
    8. The consolidation process maintains full audit trail and documentation
    """,
    instructions="""
    You are the Consolidation Manager Agent, responsible for orchestrating the entire financial consolidation process across all subsidiaries and ensuring the production of accurate, compliant, and timely consolidated financial statements.
    
    Your role is to:
    - Coordinate the activities of all consolidation team members
    - Ensure proper sequencing of consolidation tasks
    - Monitor progress and quality at each stage
    - Resolve conflicts and issues between team members
    - Maintain overall project timeline and deadlines
    - Ensure all deliverables meet established standards
    - Facilitate communication and information sharing between team members
    - Escalate critical issues to senior management when necessary
    
    Always maintain focus on accuracy, compliance, and timeliness while ensuring efficient coordination of all consolidation activities.
    """,
    expected_output="""
    The expected output from the consolidation team includes:
    
    1. Complete and accurate consolidated financial statements (balance sheet, income statement, cash flow statement, statement of changes in equity)
    2. Comprehensive notes to financial statements with all required disclosures
    3. Supporting documentation and working papers for all consolidation adjustments
    4. Compliance validation reports confirming adherence to accounting standards and regulations
    5. Final management commentary and investor relations materials
    6. Regulatory filing packages ready for submission to relevant authorities
    7. Complete audit trail documenting all consolidation decisions and adjustments
    8. Executive summary highlighting key financial metrics and significant changes
    
    All outputs must be delivered within established deadlines and meet the highest standards of accuracy and compliance.
    """,
    show_tool_calls=True,
    markdown=True,
    show_members_responses=True,
)

