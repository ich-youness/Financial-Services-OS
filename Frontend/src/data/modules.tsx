import { 
  Shield, 
  TrendingUp, 
  Users, 
  AlertTriangle, 
  FileCheck, 
  Headphones,
  LucideIcon, 
  FileText,
  FolderArchive,
  ShieldAlert,
  Banknote,
  BarChart3
} from "lucide-react";

export interface Agent {
  id: string;
  name: string;
  description: string;
  inputs: {
    text: string;
    fileUploads?: boolean;
  };
  config: {
    [key: string]: {
      type: 'dropdown' | 'slider' | 'toggle' | 'numeric' | 'text';
      label: string;
      options?: string[];
      min?: number;
      max?: number;
      default?: any;
      placeholder?: string;
    };
  };
  outputs: string[];
}

// New sub-team interface used by modules that organize agents into sub-teams
export interface SubTeam {
  id: string;
  name: string;
  mode: 'Coordinate' | 'Collaborate' | 'Route';
  description?: string;
  agents: Agent[];
}

export interface Module {
  id: string;
  title: string;
  description: string;
  icon: LucideIcon;
  colorClass: string;
  agents?: Agent[];
  subTeams?: SubTeam[];
}

export const modules: Module[] = [
   {
    id: "actuarial-modeling",
    title: "Actuarial Modeling Module",
    description: "The Actuarial Modeling module is a sophisticated multi-agent module, designed to automate and enhance core actuarial functions across the entire insurance and financial services spectrum. It operates as a team-of-teams architecture where specialized sub-teams collaborate across actuarial domains to deliver comprehensive, end-to-end actuarial solutions.",
    icon: FileText,
    colorClass: "module-card-actuarial",
    subTeams: [
      {
        id: "stm-model-dev",
        name: "Team 1: Development of Actuarial Models",
        mode: "Coordinate",
        agents: [
          {
            id: "life-nonlife-models",
            name: "Agent 1: Life & Non-Life Insurance Models",
            description: "Builds life and P&C models for pricing, reserving, and forecasting.",
            inputs: {
              text: "Upload exposure, claims, lapse/mortality, and policy data.",
              fileUploads: true
            },
            config: {
              modelClass: { type: 'dropdown', label: 'Model Class', options: ['Life', 'Non-Life', 'Both'] },
              method: { type: 'dropdown', label: 'Methodology', options: ['GLM', 'Survival', 'Stochastic'] },
              versioning: { type: 'toggle', label: 'Enable Versioning', default: true }
            },
            outputs: ['Model Spec', 'Calibrated Parameters', 'Training Summary']
          },
          {
            id: "pension-retirement-models",
            name: "Agent 2: Pension & Retirement Models",
            description: "Designs actuarial models for pensions and retirement products.",
            inputs: {
              text: "Upload demographic tables, contributions, benefits, and salary growth.",
              fileUploads: true
            },
            config: {
              valuationBasis: { type: 'dropdown', label: 'Valuation Basis', options: ['Projected Unit', 'Entry Age', 'Aggregate'] },
              discountRate: { type: 'numeric', label: 'Discount Rate (%)', default: 3 },
              mortalityTable: { type: 'dropdown', label: 'Mortality Table', options: ['Custom', 'Standard'] }
            },
            outputs: ['Actuarial Valuation', 'Contribution Requirements', 'Sensitivity Summary']
          },
          {
            id: "capital-solvency-models",
            name: "Agent 3: Capital & Solvency Models",
            description: "Develops capital and solvency models to meet regulatory and internal targets.",
            inputs: {
              text: "Upload risk exposures, capital components, and stress assumptions.",
              fileUploads: true
            },
            config: {
              framework: { type: 'dropdown', label: 'Framework', options: ['Solvency II', 'IFRS', 'Internal'] },
              targetRatio: { type: 'numeric', label: 'Target Capital Ratio (%)', default: 150 }
            },
            outputs: ['Capital Ratio', 'SCR/MCR Summary', 'Capital Plan']
          },
          {
            id: "alm-integration",
            name: "Agent 4: ALM Integration",
            description: "Integrates actuarial models with ALM for balance sheet consistency.",
            inputs: {
              text: "Upload asset/liability cash flows and rate scenarios.",
              fileUploads: true
            },
            config: {
              linkage: { type: 'dropdown', label: 'Linkage Level', options: ['Cashflow', 'Sensitivity', 'Full'] },
              horizon: { type: 'dropdown', label: 'Horizon', options: ['1Y', '3Y', '5Y'] }
            },
            outputs: ['ALM Linkage Report', 'Sensitivity Alignment', 'Integration Notes']
          }
        ]
      },
      {
        id: "stm-pricing",
        name: "Team 2: Pricing and Product Development",
        mode: "Coordinate",
        agents: [
          {
            id: "product-pricing-models",
            name: "Agent 5: Product Pricing Models",
            description: "Builds pricing models and rate structures for new/existing products.",
            inputs: { text: "Provide product specs, assumptions, and historical experience.", fileUploads: true },
            config: {
              approach: { type: 'dropdown', label: 'Pricing Approach', options: ['Cost-Plus', 'Risk-Based', 'Market-Based'] },
              marginTarget: { type: 'numeric', label: 'Target Margin (%)', default: 15 }
            },
            outputs: ['Pricing Sheet', 'Rate Cards', 'Pricing Assumptions']
          },
          {
            id: "profitability-analysis",
            name: "Agent 6: Profitability Analysis",
            description: "Analyzes profitability by cohort, channel, and product variant.",
            inputs: { text: "Upload premium, claims, expenses, and allocation keys.", fileUploads: true },
            config: {
              perspective: { type: 'dropdown', label: 'View', options: ['Cohort', 'Channel', 'Product'] },
              threshold: { type: 'slider', label: 'Alert Threshold (%)', min: 0, max: 50, default: 10 }
            },
            outputs: ['Profitability Report', 'Variance Walk', 'Recommendations']
          },
          {
            id: "sensitivity-testing",
            name: "Agent 7: Sensitivity Testing",
            description: "Performs sensitivity tests on key assumptions and pricing levers.",
            inputs: { text: "Provide base assumptions and test ranges.", fileUploads: true },
            config: {
              dimension: { type: 'dropdown', label: 'Sensitivity Dimension', options: ['Mortality', 'Lapse', 'Expense', 'Yield'] },
              rigor: { type: 'slider', label: 'Rigor Level', min: 1, max: 5, default: 3 }
            },
            outputs: ['Sensitivity Matrix', 'Key Drivers', 'Actionable Insights']
          }
        ]
      },
      {
        id: "stm-reserving",
        name: "Team 3: Reserving and Liability Valuation",
        mode: "Coordinate",
        agents: [
          {
            id: "claims-triangle-analysis",
            name: "Agent 8: Claims Triangle Analysis Specialist",
            description: "Prepares and analyzes loss triangles (paid, incurred, claims counts).",
            inputs: { text: "Upload paid/incurred triangles and exposure.", fileUploads: true },
            config: {
              triangleType: { type: 'dropdown', label: 'Triangle Type', options: ['Paid', 'Incurred', 'Reported'] },
              smoothing: { type: 'dropdown', label: 'Smoothing', options: ['None', 'Moving Avg', 'Spline'] }
            },
            outputs: ['Prepared Triangles', 'Triangle Diagnostics', 'Data Quality Notes']
          },
          {
            id: "chain-ladder-reserving",
            name: "Agent 9: Chain-Ladder Reserving Specialist",
            description: "Performs chain-ladder reserving and diagnostics.",
            inputs: { text: "Upload triangles and exposure.", fileUploads: true },
            config: {
              tailFactor: { type: 'numeric', label: 'Tail Factor (%)', default: 5 },
              confidence: { type: 'slider', label: 'Confidence Level', min: 0.5, max: 0.99, default: 0.75 }
            },
            outputs: ['Reserve Estimates', 'Development Factors', 'Interval Estimates']
          },
          {
            id: "advanced-reserving-methods",
            name: "Agent 10: Advanced Reserving Methods Specialist",
            description: "Implements Bornhuetter–Ferguson, Mack, and other reserving methods.",
            inputs: { text: "Upload triangles, premium, and expected loss ratios.", fileUploads: true },
            config: {
              method: { type: 'dropdown', label: 'Method', options: ['Bornhuetter-Ferguson', 'Mack', 'Bootstrap'] }
            },
            outputs: ['Advanced Reserve Estimates', 'Method Comparison', 'Assumption Notes']
          },
          {
            id: "solvency2-valuation",
            name: "Agent 11: Solvency II Valuation Specialist",
            description: "Values technical provisions under Solvency II (Best Estimate + Risk Margin).",
            inputs: { text: "Upload cash flows, discount curves, and risk margin parameters.", fileUploads: true },
            config: {
              curve: { type: 'dropdown', label: 'Curve', options: ['EIOPA Risk-Free', 'Custom'] },
              riskMargin: { type: 'numeric', label: 'Risk Margin (%)', default: 6 }
            },
            outputs: ['Best Estimate Liabilities', 'Risk Margin', 'TP Reconciliation']
          },
          {
            id: "ifrs17-implementation",
            name: "Agent 12: IFRS 17 Implementation Specialist",
            description: "Performs IFRS 17 measurement (GMM/PAA/VFA) and disclosures.",
            inputs: { text: "Upload cohorts, cash flows, discounting and risk adjustment inputs.", fileUploads: true },
            config: {
              measurementModel: { type: 'dropdown', label: 'Measurement Model', options: ['GMM', 'PAA', 'VFA'] },
              riskAdjustment: { type: 'numeric', label: 'Risk Adjustment (%)', default: 4 }
            },
            outputs: ['CSM Rollforward', 'IFRS 17 Disclosures', 'Measurement Summary']
          },
          {
            id: "financial-reporting-integration",
            name: "Agent 13: Financial Reporting Integration Specialist",
            description: "Integrates reserving outputs into financial reporting frameworks.",
            inputs: { text: "Upload framework mapping and reporting structures.", fileUploads: true },
            config: {
              framework: { type: 'dropdown', label: 'Framework', options: ['IFRS', 'US GAAP', 'Local GAAP'] }
            },
            outputs: ['Valuation Report', 'Disclosure Tables', 'Audit Support']
          },
          {
            id: "mortality-experience",
            name: "Agent 14: Mortality Experience Analysis Specialist",
            description: "Analyzes mortality experience and proposes assumption updates.",
            inputs: { text: "Upload exposures, deaths, and policy data.", fileUploads: true },
            config: {
              table: { type: 'dropdown', label: 'Reference Table', options: ['Custom', 'Standard'] }
            },
            outputs: ['Mortality Experience', 'Selected Assumptions', 'Study Documentation']
          },
          {
            id: "lapse-persistency",
            name: "Agent 15: Lapse and Persistency Analysis Specialist",
            description: "Performs lapse and persistency studies and segmentation.",
            inputs: { text: "Upload policy status histories and segments.", fileUploads: true },
            config: {
              segmentation: { type: 'dropdown', label: 'Segmentation', options: ['Product', 'Channel', 'Cohort'] }
            },
            outputs: ['Lapse/Persistency Results', 'Drivers & Segments', 'Assumption Update']
          },
          {
            id: "credibility-blending",
            name: "Agent 16: Credibility and Blending Specialist",
            description: "Applies credibility theory to blend experience with external benchmarks.",
            inputs: { text: "Upload internal experience and external benchmarks.", fileUploads: true },
            config: {
              method: { type: 'dropdown', label: 'Credibility Method', options: ['Bühlmann', 'Empirical Bayes'] }
            },
            outputs: ['Credibility Weights', 'Blended Assumptions', 'Documentation']
          }
        ]
      },
      {
        id: "stm-risk",
        name: "Team 4: Risk Management and Scenario Testing",
        mode: "Collaborate",
        agents: [
          {
            id: "stress-testing",
            name: "Agent 17: Stress Testing & Scenario Analysis",
            description: "Executes stress and scenario analyses across portfolios.",
            inputs: { text: "Provide scenarios and portfolio exposures.", fileUploads: true },
            config: {
              severity: { type: 'dropdown', label: 'Severity', options: ['Mild', 'Moderate', 'Severe'] },
              horizon: { type: 'dropdown', label: 'Horizon', options: ['1Y', '3Y', '5Y'] }
            },
            outputs: ['Scenario Results', 'Vulnerabilities', 'Mitigation Plan']
          },
          {
            id: "stochastic-modeling",
            name: "Agent 18: Stochastic Modeling",
            description: "Runs stochastic simulations for capital and risk measures.",
            inputs: { text: "Upload distributions and dependency structures.", fileUploads: true },
            config: {
              trials: { type: 'numeric', label: 'Simulations', default: 10000 },
              metric: { type: 'dropdown', label: 'Metric', options: ['VaR', 'TVaR'] }
            },
            outputs: ['Distribution Outputs', 'Risk Metrics', 'Stability Diagnostics']
          },
          {
            id: "enterprise-risk",
            name: "Agent 19: Enterprise Risk Management",
            description: "Aggregates risks and evaluates enterprise-level impacts.",
            inputs: { text: "Provide risk registers and interdependencies.", fileUploads: true },
            config: {
              aggregation: { type: 'dropdown', label: 'Aggregation', options: ['Additive', 'Copula-Based', 'Scenario'] }
            },
            outputs: ['ERM Profile', 'Concentration Analysis', 'Capital Allocation']
          }
        ]
      },
      {
        id: "stm-validation",
        name: "Team 5: Model Validation and Governance",
        mode: "Route",
        agents: [
          {
            id: "model-validation",
            name: "Agent 20: Model Validation",
            description: "Validates model design, data, and performance.",
            inputs: { text: "Upload documentation and validation datasets.", fileUploads: true },
            config: {
              scope: { type: 'dropdown', label: 'Scope', options: ['Data', 'Methodology', 'Performance', 'All'] },
              backtest: { type: 'toggle', label: 'Backtesting', default: true }
            },
            outputs: ['Validation Report', 'Findings Log', 'Remediation Plan']
          },
          {
            id: "regulatory-compliance",
            name: "Agent 21: Regulatory Compliance",
            description: "Checks frameworks and regulatory adherence.",
            inputs: { text: "Upload frameworks and regulatory mappings.", fileUploads: true },
            config: {
              regime: { type: 'dropdown', label: 'Regime', options: ['IFRS', 'Solvency II', 'Local'] }
            },
            outputs: ['Compliance Checklist', 'Regulatory Notes', 'Deficiencies']
          },
          {
            id: "model-risk-management",
            name: "Agent 22: Model Risk Management",
            description: "Assesses model risk and governance controls.",
            inputs: { text: "Upload model inventory and risk ratings.", fileUploads: true },
            config: {
              policy: { type: 'dropdown', label: 'Policy Strictness', options: ['Basic', 'Standard', 'Strict'] }
            },
            outputs: ['Model Risk Assessment', 'Governance Checklist', 'Approval Recommendation']
          }
        ]
      }
    ]
  },
  {
    id: "risk-assessment",
    title: "Risk Assessment Module",
    description: "Comprehensive credit analysis, market risk evaluation, and compliance checking for informed financial decisions.",
    icon: Shield,
    colorClass: "module-card-risk",
    agents: [
      {
        id: "credit-analyzer",
        name: "Credit Analyzer Agent",
        description: "Analyzes credit reports, income verification, and employment history",
        inputs: {
          text: "Enter credit reports, income verification, debt-to-income ratios, employment history, collateral values",
          fileUploads: true
        },
        config: {
          scoringModel: {
            type: 'dropdown',
            label: 'Scoring Model',
            options: ['FICO Score 8', 'FICO Score 9', 'VantageScore 3.0', 'VantageScore 4.0']
          },
          riskTier: {
            type: 'dropdown',
            label: 'Risk Tier',
            options: ['Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk']
          },
          threshold: {
            type: 'slider',
            label: 'Decision Threshold',
            min: 0.1,
            max: 1.0,
            default: 0.7
          }
        },
        outputs: ['Risk Score', 'Risk Tier', 'Recommendation']
      },
      {
        id: "market-risk-bot",
        name: "Market Risk Bot",
        description: "Evaluates market conditions and portfolio risk exposure",
        inputs: {
          text: "Enter market data feeds, portfolio positions, volatility indices, correlation matrices, stress scenarios",
          fileUploads: true
        },
        config: {
          varModel: {
            type: 'dropdown',
            label: 'VaR Model',
            options: ['Parametric VaR', 'Historical VaR', 'Monte Carlo VaR']
          },
          riskLimits: {
            type: 'numeric',
            label: 'Risk Limits ($M)',
            default: 10
          },
          alertParameters: {
            type: 'slider',
            label: 'Alert Sensitivity',
            min: 0.1,
            max: 1.0,
            default: 0.5
          }
        },
        outputs: ['VaR Metrics', 'Stress Test Results', 'Market Risk Alerts']
      },
      {
        id: "compliance-checker",
        name: "Compliance Checker Agent",
        description: "Ensures regulatory compliance across all transactions",
        inputs: {
          text: "Enter transaction data, regulatory rules, customer profiles, jurisdiction requirements, audit trails",
          fileUploads: true
        },
        config: {
          complianceRules: {
            type: 'dropdown',
            label: 'Compliance Rules',
            options: ['SOX', 'GDPR', 'Basel III', 'MiFID II', 'CCAR']
          },
          reportingRequirements: {
            type: 'dropdown',
            label: 'Reporting Requirements',
            options: ['Daily', 'Weekly', 'Monthly', 'Quarterly']
          },
          violationThreshold: {
            type: 'numeric',
            label: 'Violation Threshold',
            default: 5
          }
        },
        outputs: ['Compliance Report', 'Flagged Violations']
      }
    ]
  },
  {
    id: "investment-analysis",
    title: "Investment Analysis Module",
    description: "Advanced market research, portfolio optimization, and intelligent investment recommendations powered by AI.",
    icon: TrendingUp,
    colorClass: "module-card-investment",
    agents: [
      {
        id: "market-research-bot",
        name: "Market Research Bot",
        description: "Analyzes market trends and generates investment signals",
        inputs: {
          text: "Enter market data feeds, economic indicators, news sentiment, analyst reports, sector performance",
          fileUploads: true
        },
        config: {
          analysisFramework: {
            type: 'dropdown',
            label: 'Analysis Framework',
            options: ['Technical Analysis', 'Fundamental Analysis', 'Quantitative Analysis', 'Hybrid Analysis']
          },
          signalGeneration: {
            type: 'toggle',
            label: 'Signal Generation',
            default: true
          },
          researchPriorities: {
            type: 'dropdown',
            label: 'Research Priorities',
            options: ['Growth Stocks', 'Value Stocks', 'Dividend Stocks', 'ESG Compliant']
          }
        },
        outputs: ['Market Trend Summary', 'Investment Signals', 'Supporting Charts']
      },
      {
        id: "portfolio-optimizer",
        name: "Portfolio Optimizer Agent",
        description: "Optimizes portfolio allocation based on risk tolerance",
        inputs: {
          text: "Enter current holdings, risk tolerance, return objectives, constraints, market forecasts",
          fileUploads: true
        },
        config: {
          optimizationAlgorithm: {
            type: 'dropdown',
            label: 'Optimization Algorithm',
            options: ['Equal Weight', 'Risk Parity', 'Mean Variance', 'Black-Litterman']
          },
          rebalancingTriggers: {
            type: 'numeric',
            label: 'Rebalancing Trigger (%)',
            default: 5
          },
          costConsiderations: {
            type: 'toggle',
            label: 'Include Transaction Costs',
            default: true
          }
        },
        outputs: ['Optimized Allocation', 'Performance Metrics', 'Trade Suggestions']
      },
      {
        id: "recommendation-engine",
        name: "Recommendation Engine Bot",
        description: "Provides personalized investment recommendations",
        inputs: {
          text: "Enter client profiles, risk assessments, market conditions, product universe, historical performance",
          fileUploads: true
        },
        config: {
          suitabilityRules: {
            type: 'dropdown',
            label: 'Suitability Rules',
            options: ['Conservative', 'Moderate', 'Aggressive', 'Speculative']
          },
          recommendationLogic: {
            type: 'dropdown',
            label: 'Recommendation Logic',
            options: ['Risk-Based', 'Goal-Based', 'Age-Based', 'Income-Based']
          },
          disclosureRequirements: {
            type: 'toggle',
            label: 'Include Disclosures',
            default: true
          }
        },
        outputs: ['Product Recommendations', 'Justification Notes']
      }
    ]
  },
  {
    id: "client-management",
    title: "Client Management Module",
    description: "Streamlined relationship management, upselling opportunities identification, and guided client onboarding processes.",
    icon: Users,
    colorClass: "module-card-client",
    agents: [
      {
        id: "relationship-manager",
        name: "Relationship Manager Agent",
        description: "Manages client relationships and engagement strategies",
        inputs: {
          text: "Enter client interactions, account history, life events, service requests, satisfaction scores",
          fileUploads: true
        },
        config: {
          engagementRules: {
            type: 'dropdown',
            label: 'Engagement Rules',
            options: ['High Touch', 'Medium Touch', 'Low Touch', 'Digital Only']
          },
          touchpointScheduling: {
            type: 'text',
            label: 'Touchpoint Schedule',
            default: 'Monthly'
          },
          personalizationParameters: {
            type: 'toggle',
            label: 'Enable Personalization',
            default: true
          }
        },
        outputs: ['Client Engagement Plan']
      },
      {
        id: "upsell-identifier",
        name: "Upsell Identifier Bot",
        description: "Identifies cross-selling and upselling opportunities",
        inputs: {
          text: "Enter account data, product usage, life stage indicators, peer comparisons, eligibility criteria",
          fileUploads: true
        },
        config: {
          opportunityScoring: {
            type: 'slider',
            label: 'Opportunity Score Threshold',
            min: 0.1,
            max: 1.0,
            default: 0.7
          },
          timingRules: {
            type: 'dropdown',
            label: 'Timing Rules',
            options: ['Immediate', 'Next Quarter', 'Next Year', 'Lifecycle Event']
          },
          offerParameters: {
            type: 'dropdown',
            label: 'Offer Type',
            options: ['Product Upgrade', 'New Product', 'Service Enhancement', 'Premium Tier']
          }
        },
        outputs: ['Upsell Opportunities List']
      },
      {
        id: "onboarding-guide",
        name: "Onboarding Guide Agent",
        description: "Guides clients through the onboarding process",
        inputs: {
          text: "Enter KYC documents, account applications, verification data, product selections, funding sources",
          fileUploads: true
        },
        config: {
          workflowSteps: {
            type: 'text',
            label: 'Workflow Steps',
            default: 'Standard'
          },
          validationRules: {
            type: 'dropdown',
            label: 'Validation Rules',
            options: ['Basic KYC', 'Enhanced KYC', 'Simplified KYC', 'Full KYC']
          },
          approvalRequirements: {
            type: 'dropdown',
            label: 'Approval Level',
            options: ['Auto-Approve', 'Manager Approval', 'Senior Manager', 'Executive Approval']
          }
        },
        outputs: ['Onboarding Progress Tracker']
      }
    ]
  },
  {
    id: "fraud-detection",
    title: "Fraud Detection Module",
    description: "Real-time transaction monitoring, pattern recognition, and coordinated investigation management for fraud prevention.",
    icon: AlertTriangle,
    colorClass: "module-card-fraud",
    agents: [
      {
        id: "transaction-monitor",
        name: "Transaction Monitor Bot",
        description: "Monitors transactions in real-time for suspicious activity",
        inputs: {
          text: "Enter transaction streams, account profiles, device fingerprints, location data, behavioral patterns",
          fileUploads: true
        },
        config: {
          anomalyThresholds: {
            type: 'slider',
            label: 'Anomaly Detection Threshold',
            min: 0.1,
            max: 1.0,
            default: 0.8
          },
          ruleSets: {
            type: 'text',
            label: 'Rule Sets',
            default: 'Standard Fraud Rules'
          },
          realTimeProcessing: {
            type: 'numeric',
            label: 'Processing Limit (TPS)',
            default: 1000
          }
        },
        outputs: ['Suspicious Transaction Alerts']
      },
      {
        id: "pattern-recognition",
        name: "Pattern Recognition Agent",
        description: "Identifies fraud patterns using machine learning",
        inputs: {
          text: "Enter historical fraud cases, transaction sequences, network analysis, feature engineering",
          fileUploads: true
        },
        config: {
          mlModelParameters: {
            type: 'text',
            label: 'ML Model Parameters',
            default: 'Random Forest'
          },
          detectionSensitivity: {
            type: 'slider',
            label: 'Detection Sensitivity',
            min: 0.1,
            max: 1.0,
            default: 0.7
          },
          falsePositiveTolerance: {
            type: 'slider',
            label: 'False Positive Tolerance',
            min: 0.01,
            max: 0.5,
            default: 0.1
          }
        },
        outputs: ['Fraud Pattern Report']
      },
      {
        id: "investigation-coordinator",
        name: "Investigation Coordinator Bot",
        description: "Coordinates fraud investigation workflows",
        inputs: {
          text: "Enter alert queues, case priorities, investigator availability, evidence requirements, decision deadlines",
          fileUploads: true
        },
        config: {
          caseRouting: {
            type: 'dropdown',
            label: 'Case Routing',
            options: ['Auto-Route', 'Manual Route', 'Skill-Based Route', 'Load-Based Route']
          },
          escalationRules: {
            type: 'dropdown',
            label: 'Escalation Rules',
            options: ['Time-Based', 'Severity-Based', 'Amount-Based', 'Manual']
          },
          resolutionTracking: {
            type: 'toggle',
            label: 'Enable Resolution Tracking',
            default: true
          }
        },
        outputs: ['Investigation Dashboard']
      }
    ]
  },
  {
    id: "regulatory-compliance",
    title: "Regulatory Compliance Module",
    description: "Automated compliance monitoring, regulatory report generation, and comprehensive audit preparation tools.",
    icon: FileCheck,
    colorClass: "module-card-compliance",
    agents: [
      {
        id: "compliance-officer",
        name: "Compliance Officer Agent",
        description: "Monitors regulatory compliance across all operations",
        inputs: {
          text: "Enter regulatory updates, internal policies, audit findings, control assessments, incident reports",
          fileUploads: true
        },
        config: {
          monitoringSchedules: {
            type: 'text',
            label: 'Monitoring Schedule',
            default: 'Daily'
          },
          reportingFormats: {
            type: 'dropdown',
            label: 'Reporting Format',
            options: ['PDF', 'Excel', 'XML', 'JSON', 'Custom']
          },
          remediationTracking: {
            type: 'toggle',
            label: 'Track Remediations',
            default: true
          }
        },
        outputs: ['Compliance Monitoring Dashboard']
      },
      {
        id: "report-generator",
        name: "Report Generator Bot",
        description: "Generates regulatory reports and filings",
        inputs: {
          text: "Enter transaction data, regulatory templates, reporting periods, data validations, submission deadlines",
          fileUploads: true
        },
        config: {
          reportSpecifications: {
            type: 'dropdown',
            label: 'Report Type',
            options: ['SEC Form 10-K', 'SEC Form 10-Q', 'CCAR', 'Basel III', 'GDPR Report']
          },
          aggregationRules: {
            type: 'dropdown',
            label: 'Data Aggregation',
            options: ['Sum', 'Average', 'Count', 'Max', 'Min']
          },
          qualityChecks: {
            type: 'toggle',
            label: 'Enable Quality Checks',
            default: true
          }
        },
        outputs: ['Regulatory Report File']
      },
      {
        id: "audit-preparation",
        name: "Audit Preparation Agent",
        description: "Prepares documentation and evidence for audits",
        inputs: {
          text: "Enter audit requests, documentation requirements, control evidence, testing samples, findings history",
          fileUploads: true
        },
        config: {
          preparationChecklists: {
            type: 'dropdown',
            label: 'Preparation Checklist',
            options: ['SOX Audit', 'External Audit', 'Internal Audit', 'Regulatory Exam']
          },
          responseTemplates: {
            type: 'text',
            label: 'Response Templates',
            default: 'Standard Templates'
          },
          trackingSystems: {
            type: 'toggle',
            label: 'Enable Progress Tracking',
            default: true
          }
        },
        outputs: ['Audit Readiness Summary']
      }
    ]
  },
  {
    id: "customer-support",
    title: "Customer Support Module",
    description: "Intelligent account inquiries, transaction processing assistance, and personalized financial education services.",
    icon: Headphones,
    colorClass: "module-card-support",
    agents: [
      {
        id: "account-inquiry",
        name: "Account Inquiry Bot",
        description: "Handles customer account inquiries and questions",
        inputs: {
          text: "Enter customer queries, account data, transaction history, FAQ database, authentication data",
          fileUploads: true
        },
        config: {
          responseTemplates: {
            type: 'dropdown',
            label: 'Response Templates',
            options: ['Formal', 'Casual', 'Technical', 'Simple Language']
          },
          escalationTriggers: {
            type: 'toggle',
            label: 'Auto-Escalation',
            default: true
          },
          securityProtocols: {
            type: 'dropdown',
            label: 'Security Level',
            options: ['Basic Auth', 'Multi-Factor', 'Biometric', 'Enhanced Verification']
          }
        },
        outputs: ['Customer Response Text']
      },
      {
        id: "transaction-processor",
        name: "Transaction Processor Agent",
        description: "Processes customer transaction requests",
        inputs: {
          text: "Enter transaction requests, account balances, limits/restrictions, approval requirements, confirmation needs",
          fileUploads: true
        },
        config: {
          processingRules: {
            type: 'dropdown',
            label: 'Processing Rules',
            options: ['Same Day', 'Next Day', 'Standard', 'Express']
          },
          validationChecks: {
            type: 'toggle',
            label: 'Enable Validation',
            default: true
          },
          notificationTriggers: {
            type: 'toggle',
            label: 'Send Notifications',
            default: true
          }
        },
        outputs: ['Transaction Confirmation']
      },
      {
        id: "financial-educator",
        name: "Financial Educator Bot",
        description: "Provides financial education and guidance",
        inputs: {
          text: "Enter customer profiles, financial goals, knowledge assessments, educational content, progress tracking",
          fileUploads: true
        },
        config: {
          learningPaths: {
            type: 'dropdown',
            label: 'Learning Path',
            options: ['Beginner', 'Intermediate', 'Advanced', 'Specialized']
          },
          contentRecommendations: {
            type: 'toggle',
            label: 'Personalized Content',
            default: true
          },
          engagementMetrics: {
            type: 'numeric',
            label: 'Engagement Goal (%)',
            default: 80
          }
        },
        outputs: ['Personalized Education Plan']
      }
    ]
  },
  {
  id: "accounting-finance",
  title: "Accounting & Finance Module",
  description: "Comprehensive accounting, audit support, transaction services, credit management, and taxation assistance.",
  icon: FileText,
  colorClass: "module-card-accounting",
  agents: [
    {
      id: "accountant-agent-1",
      name: "Accountant Agent 1",
      description: "Supports daily operations, closures, tax declarations, and financial analysis.",
      inputs: {
        text: "Upload general ledgers, trial balances, income statements, and budgets",
        fileUploads: true
      },
      config: {
        reportingPeriod: {
          type: 'dropdown',
          label: 'Reporting Period',
          options: ['Monthly', 'Quarterly', 'Annually']
        },
        complianceStandard: {
          type: 'dropdown',
          label: 'Compliance Standard',
          options: ['IFRS', 'GAAP', 'Local Standards']
        },
        auditReadiness: {
          type: 'toggle',
          label: 'Prepare for Audit',
          default: true
        }
      },
      outputs: ['Reconciled Accounts', 'Tax Declarations', 'Financial Reports', 'Budget Analysis']
    },
    {
      id: "transaction-services",
      name: "Transaction Services Agent",
      description: "Handles acquisition audits, disposals, valuations, and transaction risk assessment.",
      inputs: {
        text: "Enter financial statements, contracts, and historical transaction data",
        fileUploads: true
      },
      config: {
        valuationMethod: {
          type: 'dropdown',
          label: 'Valuation Method',
          options: ['DCF', 'Comparable Companies', 'Precedent Transactions']
        },
        riskSensitivity: {
          type: 'slider',
          label: 'Risk Sensitivity',
          min: 0.1,
          max: 1.0,
          default: 0.6
        },
        dealType: {
          type: 'dropdown',
          label: 'Deal Type',
          options: ['Acquisition', 'Divestiture', 'Merger']
        }
      },
      outputs: ['Audit Report', 'Valuation Summary', 'Transaction Risks']
    },
    {
      id: "internal-control",
      name: "Internal Control Agent",
      description: "Strengthens internal controls, risk management, and audit support.",
      inputs: {
        text: "Provide risk registers, audit reports, compliance documentation, and project plans",
        fileUploads: true
      },
      config: {
        controlFramework: {
          type: 'dropdown',
          label: 'Control Framework',
          options: ['COSO', 'COBIT', 'ISO 31000']
        },
        riskLevel: {
          type: 'dropdown',
          label: 'Risk Level',
          options: ['Low', 'Medium', 'High', 'Critical']
        },
        dashboardOutput: {
          type: 'toggle',
          label: 'Generate Risk Dashboard',
          default: true
        }
      },
      outputs: ['Internal Control Report', 'Risk Dashboard', 'Compliance Notes']
    },
    {
      id: "credit-cash",
      name: "Credit & Cash Management Agent",
      description: "Monitors payments, clears suspense accounts, and manages cash flow forecasts.",
      inputs: {
        text: "Upload invoices, receivables aging, suspense accounts, and bank statements",
        fileUploads: true
      },
      config: {
        reminderPolicy: {
          type: 'dropdown',
          label: 'Reminder Policy',
          options: ['Soft Reminder', 'Firm Reminder', 'Legal Notice']
        },
        riskFlagging: {
          type: 'toggle',
          label: 'Auto-Flag Risky Accounts',
          default: true
        },
        forecastHorizon: {
          type: 'numeric',
          label: 'Forecast Horizon (days)',
          default: 90
        }
      },
      outputs: ['Reminder Schedule', 'Cleared Suspense Accounts', 'Cash Flow Forecast']
    },
    {
      id: "accounting-taxation",
      name: "Accounting & Taxation Agent",
      description: "Provides tax compliance, reporting optimization, and financial performance tracking.",
      inputs: {
        text: "Upload tax data, trial balances, management reports, and budgets",
        fileUploads: true
      },
      config: {
        taxRegime: {
          type: 'dropdown',
          label: 'Tax Regime',
          options: ['Corporate Tax', 'VAT/GST', 'Payroll Tax', 'Local Tax']
        },
        performanceTracking: {
          type: 'toggle',
          label: 'Enable KPI Tracking',
          default: true
        },
        reportingOptimization: {
          type: 'dropdown',
          label: 'Reporting Optimization Level',
          options: ['Basic', 'Intermediate', 'Advanced']
        }
      },
      outputs: ['Tax Compliance Report', 'Performance Dashboard', 'Optimization Recommendations']
    },
    {
      id: "accounting-manager",
      name: "Accounting Manager Agent",
      description: "Acts as a team leader, routes queries to the appropriate accounting agent, and ensures professional outputs.",
      inputs: {
        text: "Enter any accounting or finance-related query",
        fileUploads: false
      },
      config: {
        routingLogic: {
          type: 'dropdown',
          label: 'Routing Logic',
          options: ['Keyword-Based', 'Semantic Routing', 'Manual Selection']
        },
        clarificationPrompts: {
          type: 'toggle',
          label: 'Ask Clarifying Questions',
          default: true
        }
      },
      outputs: ['Directed Query', 'Clarification Request', 'Final Response']
    }
  ]
  },
{
  id: "account-controller",
  title: "Account Controller Module",
  description: "Monitors and manages account activities to detect anomalies, prevent fraud, and ensure account integrity.",
  icon: Shield,
  colorClass: "module-card-account",
  agents: [
    {
      id: "transaction-monitor",
      name: "Transaction Monitor Agent",
      description: "Analyzes transactions in real time to detect suspicious patterns and unusual spending behaviors.",
      inputs: {
        text: "Enter transaction logs, timestamps, amounts, geolocation data, device fingerprints, merchant details",
        fileUploads: true
      },
      config: {
        anomalyDetection: {
          type: 'dropdown',
          label: 'Anomaly Detection Method',
          options: ['Rule-based', 'Machine Learning', 'Hybrid']
        },
        sensitivity: {
          type: 'slider',
          label: 'Sensitivity Level',
          min: 0.1,
          max: 1.0,
          default: 0.6
        },
        alertChannels: {
          type: 'dropdown',
          label: 'Alert Channels',
          options: ['Email', 'SMS', 'Push Notification', 'Dashboard']
        }
      },
      outputs: ['Suspicious Transaction Alerts', 'Anomaly Scores', 'Recommended Actions']
    },
    {
      id: "account-integrity-bot",
      name: "Account Integrity Bot",
      description: "Checks account behavior, login attempts, and device usage to detect possible account takeovers.",
      inputs: {
        text: "Enter login history, IP addresses, device details, session durations, failed attempts",
        fileUploads: false
      },
      config: {
        loginPatternAnalysis: {
          type: 'dropdown',
          label: 'Login Pattern Model',
          options: ['Geolocation Check', 'Device Fingerprint', 'Time-based Pattern']
        },
        threshold: {
          type: 'slider',
          label: 'Risk Threshold',
          min: 0.1,
          max: 1.0,
          default: 0.7
        },
        autoLock: {
          type: 'dropdown',
          label: 'Auto Lock Policy',
          options: ['Disabled', 'After 3 Failed Attempts', 'After 5 Failed Attempts']
        }
      },
      outputs: ['Account Risk Score', 'Suspicious Login Alerts', 'Lock/Unlock Recommendation']
    },
    {
      id: "identity-verifier",
      name: "Identity Verifier Agent",
      description: "Validates customer identity using multi-factor checks and verification methods.",
      inputs: {
        text: "Enter user-provided IDs, biometric data, email verification, phone verification codes",
        fileUploads: true
      },
      config: {
        verificationMethods: {
          type: 'dropdown',
          label: 'Verification Methods',
          options: ['KYC Document Check', 'OTP Verification', 'Biometric Verification', 'Email & Phone Verification']
        },
        retryLimit: {
          type: 'numeric',
          label: 'Max Retry Attempts',
          default: 3
        },
        verificationStrictness: {
          type: 'slider',
          label: 'Strictness Level',
          min: 0.1,
          max: 1.0,
          default: 0.8
        }
      },
      outputs: ['Verification Status', 'Identity Confidence Score', 'Failure Report']
    }
  ]
},
{
  id: "tax-specialist",
  title: "Tax Specialist Module",
  description: "Comprehensive tax advisory, optimization, and compliance solutions tailored for banking and insurance companies.",
  icon: FileText,
  colorClass: "module-card-tax",
  agents: [
    {
      id: "tax-advisor",
      name: "Tax Advisor Agent",
      description: "Provides strategic tax guidance, analyzes tax implications, and identifies tax-saving opportunities while ensuring compliance.",
      inputs: {
        text: "Enter business decisions, transactions, financial structures, and international operations",
        fileUploads: true
      },
      config: {
        advisoryFocus: {
          type: 'dropdown',
          label: 'Advisory Focus',
          options: ['Corporate Tax Planning', 'Cross-Border Transactions', 'Transfer Pricing', 'Tax-Efficient Structures']
        },
        complianceCheck: {
          type: 'dropdown',
          label: 'Compliance Reference',
          options: ['IRS Regulations', 'OECD Guidelines', 'Local Tax Laws', 'International Treaties']
        },
        documentation: {
          type: 'slider',
          label: 'Documentation Depth',
          min: 1,
          max: 5,
          default: 3
        }
      },
      outputs: ['Tax Analysis', 'Strategic Recommendations', 'Compliance Notes']
    },
    {
      id: "tax-optimization",
      name: "Tax Optimization Agent",
      description: "Optimizes tax burden through strategic planning, deductions, credits, and timing strategies while maintaining compliance.",
      inputs: {
        text: "Enter financial statements, tax position details, investment portfolio, and business structure",
        fileUploads: true
      },
      config: {
        optimizationType: {
          type: 'dropdown',
          label: 'Optimization Strategy',
          options: ['Deductions & Credits', 'Entity Structuring', 'Income Timing', 'Capital Allocation']
        },
        savingsTarget: {
          type: 'numeric',
          label: 'Target Savings ($M)',
          default: 5
        },
        riskTolerance: {
          type: 'slider',
          label: 'Risk Tolerance',
          min: 0.1,
          max: 1.0,
          default: 0.6
        }
      },
      outputs: ['Optimization Plan', 'Estimated Tax Savings', 'Implementation Steps']
    },
    {
      id: "tax-compliance",
      name: "Tax Compliance Agent",
      description: "Monitors regulatory changes, ensures tax filings accuracy, maintains proper documentation, and identifies compliance risks.",
      inputs: {
        text: "Enter operational data, filing history, regulatory requirements, and jurisdictional details",
        fileUploads: true
      },
      config: {
        complianceScope: {
          type: 'dropdown',
          label: 'Compliance Scope',
          options: ['Federal', 'State', 'International', 'Multi-Jurisdiction']
        },
        monitoringFrequency: {
          type: 'dropdown',
          label: 'Monitoring Frequency',
          options: ['Daily', 'Weekly', 'Monthly', 'Quarterly']
        },
        auditSensitivity: {
          type: 'slider',
          label: 'Audit Risk Sensitivity',
          min: 0.1,
          max: 1.0,
          default: 0.5
        }
      },
      outputs: ['Compliance Report', 'Risk Assessment', 'Mitigation Strategies']
    }
  ]
},
{
  id: "accounting-compliance",
  title: "Accounting Compliance Module",
  description: "End-to-end validation and compliance auditing of accounting transactions to ensure integrity, consistency, and adherence to regulatory standards.",
  icon: FileText,
  colorClass: "module-card-accounting",
  agents: [
    {
      id: "entry-validator",
      name: "Accounting Entry Validator",
      description: "Performs first-level verification on accounting transactions by detecting errors, validating data integrity, applying corrections, and enforcing business rules before compliance checks.",
      inputs: {
        text: "Enter raw accounting transactions (CSV, JSON, or dicts with fields like date, amount, account_code, description, type)",
        fileUploads: true
      },
      config: {
        validationDepth: {
          type: 'slider',
          label: 'Validation Depth',
          min: 1,
          max: 5,
          default: 3
        },
        duplicateCheck: {
          type: 'dropdown',
          label: 'Duplicate Detection Level',
          options: ['Exact Match', 'Near Match', 'Both'],
          default: 'Both'
        },
        businessRules: {
          type: 'dropdown',
          label: 'Business Rule Set',
          options: ['Default Standards', 'Custom Ruleset']
        }
      },
      outputs: [
        'Validated Transactions File (validated_transactions.json)',
        'Error Report',
        'Duplicate Alerts',
        'Business Rule Violations'
      ]
    },
    {
      id: "compliance-audit",
      name: "Compliance Audit Agent",
      description: "Performs in-depth compliance checks, anomaly detection, regulatory cross-references, and generates comprehensive audit reports after validation.",
      inputs: {
        text: "Enter validated transactions or provide 'validated_transactions.json'",
        fileUploads: true
      },
      config: {
        anomalySensitivity: {
          type: 'slider',
          label: 'Anomaly Detection Sensitivity',
          min: 0.1,
          max: 1.0,
          default: 0.5
        },
        regulatoryScope: {
          type: 'dropdown',
          label: 'Regulatory Reference',
          options: ['IFRS', 'GAAP', 'Custom Ruleset']
        },
        historicalAnalysis: {
          type: 'dropdown',
          label: 'Historical Trend Depth',
          options: ['6 Months', '12 Months', '24 Months'],
          default: '12 Months'
        }
      },
      outputs: [
        'Compliance Audit Report (compliance_audit_report.json)',
        'Compliance Summary (compliance_summary.md)',
        'Regulatory Findings',
        'Risk Assessment'
      ]
    }
  ]
},
{
  id: "reporting",
  title: "Group Reporting Module",
  description: "Centralized reporting framework for subsidiaries, ensuring compliance, consolidation, validation, and continuous optimization of the group's financial closing process.",
  icon: FileText,
  colorClass: "module-card-reporting",
  agents: [
    {
      id: "assistance-to-subsidiaries",
      name: "Assistance to Subsidiaries Agent",
      description: "Provides guidance and troubleshooting support to subsidiaries on reporting templates, accounting treatments, and discrepancies during the consolidation process.",
      inputs: {
        text: "Enter subsidiary queries or describe reporting issues",
        fileUploads: true
      },
      config: {
        supportLevel: {
          type: 'slider',
          label: 'Support Detail Level',
          min: 1,
          max: 5,
          default: 3
        }
      },
      outputs: [
        "Step-by-step guidance",
        "Corrective recommendations",
        "Reporting templates"
      ]
    },
    {
      id: "group-instructions",
      name: "Production of Group Instructions Agent",
      description: "Prepares and distributes standardized reporting instructions, calendars, templates, and memos to subsidiaries before closing periods.",
      inputs: {
        text: "Enter request for reporting instructions or deadlines",
        fileUploads: true
      },
      config: {
        reportingPeriod: {
          type: 'dropdown',
          label: 'Reporting Period',
          options: ['Month-End', 'Quarter-End', 'Year-End'],
          default: 'Month-End'
        }
      },
      outputs: [
        "Reporting calendar",
        "Guidance memos",
        "Standardized templates"
      ]
    },
    {
      id: "compliance-validation",
      name: "Validation of Compliance Agent",
      description: "Validates subsidiary financial submissions against group accounting policies, IFRS/GAAP standards, FX translation rules, and intercompany eliminations.",
      inputs: {
        text: "Enter subsidiary financial submissions",
        fileUploads: true
      },
      config: {
        complianceScope: {
          type: 'dropdown',
          label: 'Compliance Reference',
          options: ['IFRS', 'GAAP', 'Group Policies'],
          default: 'Group Policies'
        },
        autoCorrect: {
          type: 'dropdown',
          label: 'Auto-Correction Mode',
          options: ['None', 'Suggest Fixes', 'Apply Fixes'],
          default: 'Suggest Fixes'
        }
      },
      outputs: [
        "Compliance validation report",
        "Deviation flags",
        "Corrective action plan"
      ]
    },
    {
      id: "consolidation",
      name: "Collection and Consolidation Agent",
      description: "Collects, validates, reconciles, and consolidates subsidiary submissions while applying FX conversion and intercompany eliminations.",
      inputs: {
        text: "Enter or upload subsidiary submissions",
        fileUploads: true
      },
      config: {
        fxRateSource: {
          type: 'dropdown',
          label: 'FX Rate Source',
          options: ['Approved FX Rates', 'Market Rates', 'Custom Rates'],
          default: 'Approved FX Rates'
        }
      },
      outputs: [
        "Consolidated group results",
        "Intercompany reconciliation report",
        "Missing submission alerts"
      ]
    },
    {
      id: "consolidated-validation",
      name: "Control and Validation of Consolidated Accounts Agent",
      description: "Performs final review of consolidated accounts, including variance analysis, compliance checks, and audit preparation.",
      inputs: {
        text: "Enter consolidated accounts data",
        fileUploads: true
      },
      config: {
        varianceThreshold: {
          type: 'slider',
          label: 'Variance Sensitivity',
          min: 1,
          max: 20,
          default: 5
        }
      },
      outputs: [
        "Variance analysis report",
        "Audit support schedules",
        "IFRS/GAAP compliance summary"
      ]
    },
    {
      id: "closing-optimization",
      name: "Optimization of Closing Process Agent",
      description: "Analyzes closing cycle bottlenecks, recommends automation, and proposes continuous improvements for faster and more accurate reporting.",
      inputs: {
        text: "Enter historical closing data or describe bottlenecks",
        fileUploads: true
      },
      config: {
        analysisDepth: {
          type: 'dropdown',
          label: 'Analysis Depth',
          options: ['Last 3 months', 'Last 6 months', 'Last 12 months'],
          default: 'Last 6 months'
        }
      },
      outputs: [
        "Closing cycle optimization report",
        "Automation recommendations",
        "Efficiency improvement plan"
      ]
    }
  ]
},
{
  id: "consolidation",
  title: "Accounting Consolidation Module",
  description: "End-to-end consolidation of subsidiary financial data into accurate, compliant, and auditable group financial statements, covering data integration, eliminations, compliance, and final filing.",
  icon: FolderArchive,
  colorClass: "module-card-consolidation",
  agents: [
    {
      id: "data-consolidation",
      name: "Accounting Data Consolidation Agent",
      description: "Collects and integrates subsidiary trial balances, applies group mappings, currency conversion, and eliminates intercompany transactions for accurate group-level data.",
      inputs: {
        text: "Upload subsidiary trial balances, reporting packages, and exchange rates.",
        fileUploads: true
      },
      config: {
        currencyConversion: {
          type: 'dropdown',
          label: 'Currency Conversion Method',
          options: ['Group Exchange Rates', 'Subsidiary Reported Rates'],
          default: 'Group Exchange Rates'
        },
        mappingFramework: {
          type: 'dropdown',
          label: 'GAAP Mapping Framework',
          options: ['IFRS', 'US GAAP', 'Custom Mapping']
        },
        intercompanyHandling: {
          type: 'dropdown',
          label: 'Intercompany Matching Rule',
          options: ['Strict Match', 'Flexible Match'],
          default: 'Strict Match'
        }
      },
      outputs: [
        'Consolidated Trial Balance (consolidated_tb.json)',
        'Intercompany Eliminations Report',
        'Mapping Adjustments Report',
        'Audit Trail Logs'
      ]
    },
    {
      id: "financial-statements",
      name: "Consolidated Financial Statements Agent",
      description: "Prepares consolidated balance sheet, income statement, cash flow statement, equity statement, and disclosures based on consolidated trial balance.",
      inputs: {
        text: "Provide consolidated trial balance file (consolidated_tb.json).",
        fileUploads: true
      },
      config: {
        accountingFramework: {
          type: 'dropdown',
          label: 'Accounting Framework',
          options: ['IFRS', 'US GAAP', 'Custom Framework'],
          default: 'IFRS'
        },
        disclosureLevel: {
          type: 'slider',
          label: 'Disclosure Depth',
          min: 1,
          max: 5,
          default: 3
        }
      },
      outputs: [
        'Consolidated Financial Statements (consolidated_statements.xlsx)',
        'Notes & Disclosures (notes.md)',
        'Supporting Working Papers',
        'Audit Support Package'
      ]
    },
    {
      id: "scope-analysis",
      name: "Variations in Scope Analysis Agent",
      description: "Handles consolidation scope changes due to M&A, disposals, restructurings, and performs purchase price allocations where required.",
      inputs: {
        text: "Provide details of scope changes (M&A, divestitures, restructurings).",
        fileUploads: true
      },
      config: {
        consolidationMethod: {
          type: 'dropdown',
          label: 'Default Consolidation Method',
          options: ['Full', 'Proportionate', 'Equity Method'],
          default: 'Full'
        },
        ppaTreatment: {
          type: 'dropdown',
          label: 'Purchase Price Allocation Handling',
          options: ['Automatic Allocation', 'Manual Input Required'],
          default: 'Automatic Allocation'
        }
      },
      outputs: [
        'Scope Change Report',
        'Purchase Price Allocation Summary',
        'Goodwill & Intangibles Report',
        'Adjusted Consolidation Outputs'
      ]
    },
    {
      id: "subsidiary-reports",
      name: "Production Subsidiary Reports Agent",
      description: "Prepares subsidiary-level reporting packages aligned with group policies, including disclosures and required notes for consolidation.",
      inputs: {
        text: "Upload subsidiary financials for group reporting conversion.",
        fileUploads: true
      },
      config: {
        reportingFormat: {
          type: 'dropdown',
          label: 'Reporting Format',
          options: ['Excel Template', 'JSON Standardized Package'],
          default: 'Excel Template'
        },
        disclosureCollection: {
          type: 'dropdown',
          label: 'Disclosure Data Collection',
          options: ['Manual Upload', 'Automated Pull'],
          default: 'Manual Upload'
        }
      },
      outputs: [
        'Subsidiary Reporting Packages',
        'Disclosure Data Sheets',
        'Alignment Report with Group Policies'
      ]
    },
    {
      id: "compliance-validation",
      name: "Compliance Validation Agent",
      description: "Validates compliance of both subsidiary and consolidated reports with group policies, accounting standards, and regulatory requirements.",
      inputs: {
        text: "Provide consolidated and subsidiary reports for compliance validation.",
        fileUploads: true
      },
      config: {
        complianceFramework: {
          type: 'dropdown',
          label: 'Compliance Framework',
          options: ['IFRS', 'US GAAP', 'Local GAAP', 'Custom Framework'],
          default: 'IFRS'
        },
        updateCheck: {
          type: 'toggle',
          label: 'Check for Regulatory Updates',
          default: true
        }
      },
      outputs: [
        'Compliance Validation Report',
        'Policy Alignment Report',
        'Regulatory Update Notes'
      ]
    },
    {
      id: "final-statements",
      name: "Final Consolidated Statements Agent",
      description: "Performs final review, variance analysis, board sign-off preparation, and regulatory filing of the consolidated financial statements.",
      inputs: {
        text: "Provide prepared consolidated financial statements for review and finalization.",
        fileUploads: true
      },
      config: {
        varianceAnalysis: {
          type: 'dropdown',
          label: 'Variance Analysis Scope',
          options: ['vs. Prior Period', 'vs. Budget', 'vs. Forecast', 'All'],
          default: 'All'
        },
        filingDestination: {
          type: 'dropdown',
          label: 'Regulatory Filing Destination',
          options: ['Tax Authority', 'Stock Exchange', 'Securities Regulator', 'All'],
          default: 'All'
        }
      },
      outputs: [
        'Final Reviewed Consolidated Financial Statements',
        'Variance Analysis Report',
        'Management Commentary',
        'Regulatory Filing Package',
        'Executive Summary'
      ]
    }
  ]
},
{
  id: "structural-risk-analyst",
  title: "Structural Risk Analyst Module",
  description: "Comprehensive structural risk management and regulatory reporting. Covers solvency, liquidity, interest rate risk, FX exposures, and regulatory reporting corrections with deep analytical insights.",
  icon: ShieldAlert,
  colorClass: "module-card-risk",
  agents: [
    {
      id: "solvency-indicator",
      name: "Regulatory Reporting Solvency Agent",
      description: "Focuses on solvency metrics for regulators: Risk-Weighted Assets, Capital Adequacy Ratios, and data quality controls.",
      inputs: {
        text: "Upload balance sheets, capital structure data, and exposure files.",
        fileUploads: true
      },
      config: {
        rwaCalculation: {
          type: 'dropdown',
          label: 'RWA Calculation Approach',
          options: ['Standardized', 'IRB (Internal Ratings-Based)'],
          default: 'Standardized'
        },
        capitalRatios: {
          type: 'toggle',
          label: 'Calculate CET1/Tier 1/Total Capital Ratios',
          default: true
        }
      },
      outputs: [
        'Risk-Weighted Assets Report',
        'Capital Adequacy Ratios Summary',
        'Data Quality Reconciliation Report'
      ]
    },
    {
      id: "liquidity-indicator",
      name: "Structural Risks Liquidity Indicators Agent",
      description: "Specialized in Basel III liquidity metrics such as LCR, NSFR, and liquidity stress testing.",
      inputs: {
        text: "Upload liquidity cash flows, funding maturity schedules, and stress scenarios.",
        fileUploads: true
      },
      config: {
        liquidityMetric: {
          type: 'dropdown',
          label: 'Liquidity Metric',
          options: ['LCR', 'NSFR', 'Both'],
          default: 'Both'
        },
        stressTesting: {
          type: 'toggle',
          label: 'Enable Liquidity Stress Testing',
          default: true
        }
      },
      outputs: [
        'Liquidity Coverage Ratio Report',
        'Net Stable Funding Ratio Report',
        'Liquidity Stress Test Results'
      ]
    },
    {
      id: "interest-rate-risk",
      name: "Interest Rate Risk & Related Metrics Agent",
      description: "Handles IRRBB, CSRBB, ITS reporting, and sensitivity analysis of interest rate and spread risks.",
      inputs: {
        text: "Provide interest rate gaps, repricing schedules, and portfolio sensitivities.",
        fileUploads: true
      },
      config: {
        riskType: {
          type: 'dropdown',
          label: 'Risk Type',
          options: ['IRRBB', 'CSRBB', 'Both'],
          default: 'IRRBB'
        },
        sensitivityLevel: {
          type: 'slider',
          label: 'Sensitivity Analysis Depth',
          min: 1,
          max: 5,
          default: 3
        }
      },
      outputs: [
        'Interest Rate Risk Sensitivity Report',
        'Earnings-at-Risk Model',
        'IRRBB/CSRBB Compliance Report'
      ]
    },
    {
      id: "fx-risk",
      name: "Foreign Exchange (FX) Risk Agent",
      description: "Monitors currency exposures, Net Open Position, sensitivity analysis, and hedge effectiveness.",
      inputs: {
        text: "Upload FX positions, derivatives, and hedging instruments data.",
        fileUploads: true
      },
      config: {
        exposureCalculation: {
          type: 'dropdown',
          label: 'Exposure Calculation Method',
          options: ['Gross', 'Net', 'Hedged'],
          default: 'Net'
        },
        sensitivityTesting: {
          type: 'toggle',
          label: 'Enable FX Sensitivity Testing',
          default: true
        }
      },
      outputs: [
        'FX Exposure Report',
        'Net Open Position Analysis',
        'Hedge Effectiveness Report'
      ]
    },
    {
      id: "regulatory-corrections",
      name: "Regulatory Reporting Correction Agent",
      description: "Ensures compliance across regimes (MiFID II, EMIR, DFA, IFRS, Basel/CRR3) through error detection and corrections.",
      inputs: {
        text: "Upload regulatory reporting files (MiFID II, EMIR, DFA, Basel reports).",
        fileUploads: true
      },
      config: {
        regulation: {
          type: 'dropdown',
          label: 'Target Regulation',
          options: ['MiFID II', 'EMIR', 'DFA', 'IFRS', 'Basel/CRR3'],
          default: 'Basel/CRR3'
        },
        autoCorrection: {
          type: 'toggle',
          label: 'Enable Auto-Corrections',
          default: true
        }
      },
      outputs: [
        'Corrected Regulatory Reports',
        'Compliance Audit Trail',
        'Error & Correction Summary'
      ]
    }
  ]
},
{
  id: "treasurer",
  title: "Treasury & Finance Module",
  description: "Manages liquidity, financing, and investments to optimize cash flow, ensure policy compliance, and safeguard financial stability.",
  icon: Banknote,
  colorClass: "module-card-treasurer",
  agents: [
    {
      id: "cashflow-management",
      name: "Cash Flow Management Agent",
      description: "Monitors balances, forecasts inflows/outflows, optimizes liquidity buffers, and identifies risks in cash flow operations.",
      inputs: {
        text: "Provide transaction history details or queries about liquidity, forecasting, or cash positions.",
        fileUploads: true
      },
      config: {
        forecastHorizon: {
          type: 'slider',
          label: 'Forecast Horizon (days)',
          min: 7,
          max: 90,
          default: 30
        },
        scenarioAnalysis: {
          type: 'dropdown',
          label: 'Scenario',
          options: ['Base Case', 'Optimistic', 'Stress Test'],
          default: 'Base Case'
        },
        liquidityBuffer: {
          type: 'dropdown',
          label: 'Liquidity Policy',
          options: ['2 Months Payroll', '$50,000 Minimum', 'Custom Threshold']
        }
      },
      outputs: [
        'Liquidity Position Report',
        '30-90 Day Cash Flow Forecast',
        'Buffer Analysis (surplus/shortfall)',
        'Risk Alerts (FX exposure, timing mismatches, anomalies)',
        'Treasury Recommendations'
      ]
    },
    {
      id: "overseeing-financing",
      name: "Overseeing Financing Agent",
      description: "Manages capital structure, debt, and funding strategy, ensuring compliance with policies and optimizing financing costs.",
      inputs: {
        text: "Provide financing schedules, leverage details, or queries about debt and funding.",
        fileUploads: true
      },
      config: {
        leverageThreshold: {
          type: 'slider',
          label: 'Max Debt/EBITDA',
          min: 1,
          max: 6,
          default: 3
        },
        refinancingWindow: {
          type: 'dropdown',
          label: 'Refinancing Horizon',
          options: ['6 Months', '12 Months', '24 Months'],
          default: '12 Months'
        },
        fundingPreference: {
          type: 'dropdown',
          label: 'Preferred Funding Source',
          options: ['Retained Earnings', 'Debt', 'Equity Issuance']
        }
      },
      outputs: [
        'Capital Structure Report',
        'Debt Maturity Schedule',
        'Refinancing Recommendations',
        'Covenant Risk Alerts',
        'Funding Strategy Guidance'
      ]
    },
    {
      id: "overseeing-investment",
      name: "Overseeing Investment Agent",
      description: "Oversees investment portfolio compliance, allocation, performance, and risk monitoring for treasury operations.",
      inputs: {
        text: "Provide investment portfolio details or queries about allocations, compliance, or performance.",
        fileUploads: true
      },
      config: {
        complianceCheck: {
          type: 'dropdown',
          label: 'Policy Compliance Focus',
          options: ['Asset Classes', 'Credit Quality', 'Duration Limits'],
          default: 'Asset Classes'
        },
        allocationStrategy: {
          type: 'dropdown',
          label: 'Liquidity Allocation Strategy',
          options: ['Operational Liquidity', 'Reserve Liquidity', 'Strategic Surplus'],
          default: 'Operational Liquidity'
        },
        benchmark: {
          type: 'dropdown',
          label: 'Performance Benchmark',
          options: ['LIBOR', 'Treasury Yield', 'Corporate Bond Index']
        }
      },
      outputs: [
        'Portfolio Allocation Report',
        'Policy Compliance Results',
        'Performance vs. Benchmarks',
        'Risk Alerts (credit, liquidity, mark-to-market)',
        'Investment Recommendations'
      ]
    }
  ]
},


// # Tuesday
{
  id: "analyst-reporting-manager",
  title: "Analyst Reporting & Financial Management Module",
  description: "Supports financial reporting, performance analysis, strategic alignment, and presentation of insights for executive decision-making.",
  icon: BarChart3,
  colorClass: "module-card-analyst",
  agents: [
    {
      id: "fin-data-strategy",
      name: "Financial Data for Strategic Decision-Making",
      description: "Compiles, validates, and consolidates financial data (Actual, Budget, Forecast) into standardized reporting packages for executives, ensuring compliance with policies and consistency across reporting periods.",
      inputs: {
        text: "Upload financial data files (CSV, Excel) with Actual, Budget, and Forecast figures.",
        fileUploads: true
      },
      config: {
        reportingFrequency: {
          type: 'dropdown',
          label: 'Reporting Frequency',
          options: ['Monthly', 'Quarterly', 'Yearly'],
          default: 'Monthly'
        },
        validationLevel: {
          type: 'slider',
          label: 'Validation Rigor',
          min: 1,
          max: 5,
          default: 3
        },
        varianceThreshold: {
          type: 'slider',
          label: 'Variance Alert (%)',
          min: 5,
          max: 25,
          default: 10
        }
      },
      outputs: [
        'Validated Consolidated Dataset',
        'Compliance & Anomaly Report',
        'Standardized Reporting Package (PDF/Excel)',
        'Variance Analysis (Actual vs Budget vs Forecast)',
        'Executive Summary Report'
      ]
    },
    {
      id: "fin-performance-analysis",
      name: "Analyzing Financial Performance",
      description: "Calculates KPIs, evaluates portfolio and activity-level profitability, performs variance analysis, and provides management commentary for performance evaluation.",
      inputs: {
        text: "Upload performance datasets (CSV, Excel) containing financial results.",
        fileUploads: true
      },
      config: {
        kpiSelection: {
          type: 'dropdown',
          label: 'KPI Focus',
          options: ['ROI', 'ROE', 'Cost-to-Income Ratio', 'Net Interest Margin', 'All'],
          default: 'All'
        },
        varianceThreshold: {
          type: 'slider',
          label: 'Variance Alert (%)',
          min: 5,
          max: 25,
          default: 10
        },
        activityCosting: {
          type: 'dropdown',
          label: 'Activity-Based Costing',
          options: ['Enabled', 'Disabled'],
          default: 'Enabled'
        }
      },
      outputs: [
        'KPI Dashboard',
        'Portfolio Performance Report',
        'Activity-Level Profitability Analysis',
        'Variance Analysis with Commentary',
        'Management Recommendations'
      ]
    },
    {
      id: "strategic-alignment",
      name: "Strategic Alignment Assessment",
      description: "Assesses alignment of business units and portfolios with corporate strategy, recommends resource allocation, and measures risk-adjusted performance metrics.",
      inputs: {
        text: "Upload portfolio performance datasets (CSV, Excel) with strategic targets.",
        fileUploads: true
      },
      config: {
        alignmentCriteria: {
          type: 'dropdown',
          label: 'Strategic Fit Criteria',
          options: ['Revenue Growth', 'Profitability', 'Risk-Adjusted Return', 'Market Position'],
          default: 'Profitability'
        },
        riskMetric: {
          type: 'dropdown',
          label: 'Risk-Adjusted Metric',
          options: ['RAROC', 'EVA', 'Sharpe Ratio'],
          default: 'RAROC'
        },
        resourceAllocation: {
          type: 'dropdown',
          label: 'Resource Allocation Priority',
          options: ['High-Return Activities', 'Strategic Fit Units', 'Balanced Approach'],
          default: 'Balanced Approach'
        }
      },
      outputs: [
        'Strategic Fit Assessment',
        'Risk-Adjusted Performance Analysis',
        'Resource Allocation Recommendations',
        'Strategic Alignment Report',
        'Executive Commentary'
      ]
    },
    {
      id: "financial-insights",
      name: "Presenting Financial Insights",
      description: "Transforms financial data and analyses into dashboards, presentations, and narratives for executives and stakeholders with scenario and sensitivity modeling.",
      inputs: {
        text: "Provide financial analysis outputs, datasets, or executive reporting needs.",
        fileUploads: true
      },
      config: {
        dashboardType: {
          type: 'dropdown',
          label: 'Dashboard Format',
          options: ['KPI Overview', 'Variance Analysis', 'Scenario Planning'],
          default: 'KPI Overview'
        },
        scenarioAnalysis: {
          type: 'dropdown',
          label: 'Scenario Type',
          options: ['Base Case', 'Optimistic', 'Stress Test'],
          default: 'Base Case'
        },
        reportingStyle: {
          type: 'dropdown',
          label: 'Reporting Style',
          options: ['Data-Heavy', 'Visual & Narrative', 'Balanced'],
          default: 'Balanced'
        }
      },
      outputs: [
        'Executive Dashboards (interactive/static)',
        'Board & Management Reports',
        'Scenario & Sensitivity Analysis',
        'Narrative Storytelling with Data',
        'Decision-Ready Insights Package'
      ]
    }
  ]
},
{
  id: "esg-module",
  title: "ESG Compliance & Reporting Module",
  description: "Helps financial institutions and corporates manage ESG compliance, align with global frameworks, produce CSRD/ESRS-compliant reports, and monitor regulatory updates.",
  icon: FileText,
  colorClass: "module-card-esg",
  agents: [
    {
      id: "framework-analysis",
      name: "Framework Analysis",
      description: "Interprets CSRD and ESRS requirements, maps to ESG frameworks (EU Taxonomy, SFDR, TCFD, GRI, ISSB), and provides gap analyses and implementation roadmaps.",
      inputs: {
        text: "Upload ESG or sustainability data (CSV, Excel) and policy/report documents.",
        fileUploads: true
      },
      config: {
        frameworkFocus: {
          type: "dropdown",
          label: "Framework Focus",
          options: ["CSRD", "ESRS", "EU Taxonomy", "GRI", "ISSB", "All"],
          default: "CSRD"
        },
        analysisDepth: {
          type: "slider",
          label: "Gap Analysis Depth",
          min: 1,
          max: 5,
          default: 3
        },
        roadmapHorizon: {
          type: "dropdown",
          label: "Roadmap Horizon",
          options: ["Short-Term", "Medium-Term", "Long-Term"],
          default: "Medium-Term"
        }
      },
      outputs: [
        "CSRD/ESRS Gap Analysis",
        "Compliance Readiness Report",
        "Framework Mapping Summary",
        "Phased Implementation Roadmap",
        "Executive Recommendations"
      ]
    },
    {
      id: "new-regulations-compliance",
      name: "New Regulations Compliance",
      description: "Supports materiality assessments, defines ESG data requirements, and ensures audit readiness for CSRD/ESRS compliance.",
      inputs: {
        text: "Upload ESG datasets (CSV, Excel) and internal compliance documents.",
        fileUploads: true
      },
      config: {
        materialityScope: {
          type: "dropdown",
          label: "Materiality Scope",
          options: ["Financial Materiality", "Impact Materiality", "Double Materiality"],
          default: "Double Materiality"
        },
        auditReadinessLevel: {
          type: "slider",
          label: "Audit Readiness Level",
          min: 1,
          max: 5,
          default: 3
        },
        dataCoverage: {
          type: "dropdown",
          label: "Data Coverage Focus",
          options: ["Environmental", "Social", "Governance", "Full ESG"],
          default: "Full ESG"
        }
      },
      outputs: [
        "Materiality Assessment Report",
        "Data Requirement Mapping",
        "Audit Readiness Evaluation",
        "Compliance Action Plan",
        "Gap Closure Recommendations"
      ]
    },
    {
      id: "reporting-process-design",
      name: "Designing Reporting Processes",
      description: "Designs ESG reporting workflows, standardizes data collection, integrates systems, and strengthens governance for CSRD/ESRS compliance.",
      inputs: {
        text: "Upload ESG reporting data (CSV, Excel) and governance/policy documentation.",
        fileUploads: true
      },
      config: {
        workflowFocus: {
          type: "dropdown",
          label: "Workflow Focus",
          options: ["Data Collection", "Validation Controls", "Governance", "Integration"],
          default: "Integration"
        },
        automationLevel: {
          type: "slider",
          label: "Automation Level",
          min: 1,
          max: 5,
          default: 2
        },
        governanceStrength: {
          type: "slider",
          label: "Governance Maturity Level",
          min: 1,
          max: 5,
          default: 3
        }
      },
      outputs: [
        "Process Workflow Blueprint",
        "Data Collection & Validation Framework",
        "Governance & Control Recommendations",
        "System Integration Map",
        "Process Optimization Report"
      ]
    },
    {
      id: "compliant-report-production",
      name: "Producing Compliant Reports",
      description: "Structures CSRD-compliant reports with narrative and quantitative disclosures, reconciles ESG metrics with financials, and ensures audit-ready machine-readable outputs.",
      inputs: {
        text: "Upload ESG data (CSV, Excel) and financial statements or narratives.",
        fileUploads: true
      },
      config: {
        disclosureFormat: {
          type: "dropdown",
          label: "Disclosure Format",
          options: ["Narrative", "Quantitative", "Combined"],
          default: "Combined"
        },
        reconciliationFocus: {
          type: "dropdown",
          label: "Reconciliation Focus",
          options: ["ESG with Financials", "KPIs Only", "Full Integration"],
          default: "Full Integration"
        },
        outputFormat: {
          type: "dropdown",
          label: "Report Format",
          options: ["PDF", "Excel", "XHTML/ESEF"],
          default: "XHTML/ESEF"
        }
      },
      outputs: [
        "CSRD-Compliant Draft Report",
        "Narrative & KPI Disclosures",
        "Financial Reconciliation Summary",
        "Audit-Ready Report Package",
        "Regulatory Submission File (ESEF/XHTML)"
      ]
    },
    {
      id: "continuous-monitoring",
      name: "Continuous Monitoring",
      description: "Tracks ESG regulatory updates, classifies impact, and recommends actions with compliance logs and training recommendations.",
      inputs: {
        text: "Upload regulatory update logs (CSV, Excel) or compliance notes.",
        fileUploads: true
      },
      config: {
        updateScope: {
          type: "dropdown",
          label: "Update Scope",
          options: ["CSRD", "ESRS", "ISSB", "SEC", "All"],
          default: "All"
        },
        urgencyThreshold: {
          type: "slider",
          label: "Urgency Threshold (days)",
          min: 7,
          max: 90,
          default: 30
        },
        trainingFocus: {
          type: "dropdown",
          label: "Training Focus",
          options: ["Regulation Awareness", "Process Adoption", "Audit Preparation"],
          default: "Regulation Awareness"
        }
      },
      outputs: [
        "Regulatory Update Tracker",
        "Compliance Impact Assessment",
        "Action & Deadline Log",
        "Training Recommendation Summary",
        "Executive Monitoring Report"
      ]
    }
  ]
},
{
  id: "isr-module",
  title: "ISR Consulting Module",
  description: "Supports institutions and investors with socially responsible investment strategies, ESG integration, portfolio optimization, regulatory compliance, and continuous monitoring of ethical standards.",
  icon: FileText,
  colorClass: "module-card-isr",
  agents: [
    {
      id: "ethical-investment-strategy",
      name: "Ethical & Sustainable Investment Strategy",
      description: "Advises on ethical and sustainable investment strategies, develops SRI policies, defines ESG exclusion/inclusion criteria, and aligns portfolios with client values.",
      inputs: {
        text: "Upload investment guidelines, ESG preferences, or sustainability policies.",
        fileUploads: true
      },
      config: {
        policyFocus: {
          type: "dropdown",
          label: "Policy Focus",
          options: ["Exclusionary", "Best-in-Class", "Thematic", "Impact Investing", "Blended"],
          default: "Exclusionary"
        },
        alignmentLevel: {
          type: "slider",
          label: "Client Value Alignment Level",
          min: 1,
          max: 5,
          default: 3
        },
        esgCriteria: {
          type: "dropdown",
          label: "Primary ESG Criteria",
          options: ["Environmental", "Social", "Governance", "Full ESG"],
          default: "Full ESG"
        }
      },
      outputs: [
        "SRI Policy Framework",
        "Ethical Investment Guidelines",
        "Exclusion/Inclusion Criteria Map",
        "Values Alignment Assessment",
        "Strategic Investment Roadmap"
      ]
    },
    {
      id: "esg-integration",
      name: "ESG Integration",
      description: "Applies ESG screening, impact measurement frameworks, and risk management into investment decisions.",
      inputs: {
        text: "Upload ESG scoring data, investment universe, or risk reports.",
        fileUploads: true
      },
      config: {
        screeningMethod: {
          type: "dropdown",
          label: "Screening Method",
          options: ["Negative Screening", "Positive Screening", "Best-in-Class", "Thematic"],
          default: "Negative Screening"
        },
        impactDepth: {
          type: "slider",
          label: "Impact Measurement Depth",
          min: 1,
          max: 5,
          default: 3
        },
        riskFocus: {
          type: "dropdown",
          label: "Risk Management Focus",
          options: ["Climate Risk", "Governance Risk", "Social Risk", "Comprehensive ESG"],
          default: "Comprehensive ESG"
        }
      },
      outputs: [
        "ESG Screening Results",
        "Impact Measurement Framework",
        "Risk Exposure Report",
        "Portfolio ESG Scorecard",
        "Integration Recommendations"
      ]
    },
    {
      id: "portfolio-optimization",
      name: "Portfolio Construction & Optimization",
      description: "Designs optimized portfolios balancing financial performance and ESG alignment.",
      inputs: {
        text: "Upload portfolio holdings (CSV, Excel) and ESG target metrics.",
        fileUploads: true
      },
      config: {
        optimizationGoal: {
          type: "dropdown",
          label: "Optimization Goal",
          options: ["Maximize Returns", "Minimize Risk", "Balance ESG & Returns", "Impact Priority"],
          default: "Balance ESG & Returns"
        },
        diversificationLevel: {
          type: "slider",
          label: "Diversification Level",
          min: 1,
          max: 5,
          default: 3
        },
        esgWeighting: {
          type: "slider",
          label: "ESG Weighting (%)",
          min: 0,
          max: 100,
          default: 50
        }
      },
      outputs: [
        "Optimized Portfolio Allocation",
        "Risk/Return Analysis",
        "ESG Alignment Report",
        "Diversification Assessment",
        "Strategic Optimization Roadmap"
      ]
    },
    {
      id: "regulatory-compliance",
      name: "ISR Regulatory Compliance",
      description: "Ensures compliance with SRI/ESG investment regulations, reporting standards, and audit requirements.",
      inputs: {
        text: "Upload compliance policies, audit reports, or regulatory documentation.",
        fileUploads: true
      },
      config: {
        regulationFocus: {
          type: "dropdown",
          label: "Regulation Focus",
          options: ["EU SFDR", "EU Taxonomy", "CSRD", "UN PRI", "All"],
          default: "All"
        },
        auditLevel: {
          type: "slider",
          label: "Audit Readiness Level",
          min: 1,
          max: 5,
          default: 3
        },
        reportingFormat: {
          type: "dropdown",
          label: "Reporting Format",
          options: ["PDF", "Excel", "XHTML/ESEF"],
          default: "PDF"
        }
      },
      outputs: [
        "Regulatory Compliance Report",
        "Audit Readiness Evaluation",
        "Data Requirement Checklist",
        "Compliance Action Plan",
        "Submission-Ready Documentation"
      ]
    },
    {
      id: "continuous-ethical-monitoring",
      name: "Continuous Ethical Monitoring",
      description: "Monitors ongoing regulatory, ethical, and sustainability updates with alerts and training recommendations.",
      inputs: {
        text: "Upload monitoring logs, regulatory updates, or ESG alerts.",
        fileUploads: true
      },
      config: {
        monitoringScope: {
          type: "dropdown",
          label: "Monitoring Scope",
          options: ["ESG Updates", "Regulatory Changes", "Market News", "All"],
          default: "All"
        },
        alertThreshold: {
          type: "slider",
          label: "Alert Urgency Threshold (days)",
          min: 7,
          max: 90,
          default: 30
        },
        trainingType: {
          type: "dropdown",
          label: "Training Focus",
          options: ["Ethical Investing Awareness", "Regulatory Compliance", "Portfolio Management Best Practices"],
          default: "Ethical Investing Awareness"
        }
      },
      outputs: [
        "Ethical Update Tracker",
        "Compliance Impact Log",
        "Urgency-Based Action Plan",
        "Training Recommendation Report",
        "Executive Monitoring Dashboard"
      ]
    }
  ]
},
{
  id: "alm-module",
  title: "Asset Liability Management Module",
  description: "Comprehensive ALM solution for liquidity risk assessment, interest rate risk management, capital optimization, profitability enhancement, risk modeling, and treasury operations control.",
  icon: BarChart3,
  colorClass: "module-card-alm",
  agents: [
    {
      id: "liquidity-interest-rate-risk",
      name: "Liquidity & Interest Rate Risk Assessor",
      description: "Evaluates institution's liquidity position and interest rate risk exposure, monitors short-term and long-term liquidity, identifies cash flow maturity gaps, and measures balance sheet sensitivity to interest rate shocks.",
      inputs: {
        text: "Upload balance sheet data, asset/liability cash flows, maturity schedules, and rate shock scenarios.",
        fileUploads: true
      },
      config: {
        timeBuckets: {
          type: "text",
          label: "Time Buckets (days)",
          placeholder: "0,30,90,180,360,730",
          default: "0,30,180,365"
        },
        rateShocks: {
          type: "text",
          label: "Rate Shock Scenarios (%)",
          placeholder: "0.01,-0.01,0.02",
          default: "0.01,-0.01"
        },
        riskTolerance: {
          type: "slider",
          label: "Risk Tolerance Level",
          min: 1,
          max: 5,
          default: 3
        }
      },
      outputs: [
        "Liquidity Gap Analysis Report",
        "EVE Sensitivity Analysis",
        "NII Sensitivity Projections",
        "Risk Exposure Assessment",
        "Mitigation Recommendations"
      ]
    },
    {
      id: "solvency-capital-strategist",
      name: "Solvency & Capital Strategist",
      description: "Ensures institution maintains adequate capital buffers and liquidity reserves to remain solvent under normal and stress conditions, optimizing asset-liability mix.",
      inputs: {
        text: "Upload capital levels, cash flow projections, asset/liability mix with yields and costs.",
        fileUploads: true
      },
      config: {
        liquidityBuffer: {
          type: "numeric",
          label: "Liquidity Buffer Amount",
          placeholder: "200",
          default: 200
        },
        maxAssetShare: {
          type: "slider",
          label: "Max Asset Share (%)",
          min: 10,
          max: 50,
          default: 25
        },
        fundingThreshold: {
          type: "slider",
          label: "Contingency Funding Threshold (%)",
          min: 5,
          max: 20,
          default: 10
        }
      },
      outputs: [
        "Capital Adequacy Assessment",
        "Contingency Funding Analysis",
        "Balance Sheet Optimization Plan",
        "Regulatory Compliance Check",
        "Capital Management Strategy"
      ]
    },
    {
      id: "profitability-optimizer",
      name: "Profitability Optimizer",
      description: "Maximizes institution's return on assets and minimizes funding costs while staying compliant with regulatory and internal ALM rules.",
      inputs: {
        text: "Upload asset allocation, liability mix, investment options with yields and risks.",
        fileUploads: true
      },
      config: {
        liquidityBufferPct: {
          type: "slider",
          label: "Minimum Liquidity Buffer (%)",
          min: 5,
          max: 20,
          default: 10
        },
        shortTermThreshold: {
          type: "slider",
          label: "Short-term Funding Limit (%)",
          min: 10,
          max: 30,
          default: 15
        },
        riskLimit: {
          type: "slider",
          label: "Investment Risk Limit (%)",
          min: 10,
          max: 40,
          default: 25
        }
      },
      outputs: [
        "Yield Optimization Strategy",
        "Funding Cost Reduction Plan",
        "ALM Investment Allocation",
        "Profitability Improvement Forecast",
        "Risk-Adjusted Return Analysis"
      ]
    },
    {
      id: "risk-model-builder",
      name: "Risk Model Builder",
      description: "Creates analytical tools for measuring and monitoring financial risks including liquidity projections and interest rate risk in the banking book.",
      inputs: {
        text: "Upload cash flows, portfolio data with rates/durations, off-balance-sheet commitments.",
        fileUploads: true
      },
      config: {
        stressFactor: {
          type: "slider",
          label: "Stress Factor Multiplier",
          min: 1.0,
          max: 2.0,
          default: 1.2
        },
        rateShiftRange: {
          type: "text",
          label: "Rate Shift Range (%)",
          placeholder: "0.01,-0.01,0.02",
          default: "0.01,-0.01"
        },
        projectionPeriod: {
          type: "dropdown",
          label: "Projection Period",
          options: ["7 days", "30 days", "90 days", "1 year"],
          default: "30 days"
        }
      },
      outputs: [
        "Liquidity Projection Model",
        "Interest Rate Sensitivity Analysis",
        "Risk Exposure Dashboard",
        "Stress Testing Results",
        "Model Validation Report"
      ]
    },
    {
      id: "liquidity-operations-manager",
      name: "Liquidity Operations Manager",
      description: "Oversees daily liquidity management, funding strategy execution, and activation of contingency measures during stress events.",
      inputs: {
        text: "Upload daily cash positions, funding options with costs, currency allocations.",
        fileUploads: true
      },
      config: {
        currencyFocus: {
          type: "dropdown",
          label: "Primary Currency",
          options: ["USD", "EUR", "GBP", "JPY", "Multi-currency"],
          default: "USD"
        },
        fundingPriority: {
          type: "dropdown",
          label: "Funding Priority",
          options: ["Cost Minimization", "Risk Diversification", "Speed of Access", "Regulatory Compliance"],
          default: "Cost Minimization"
        },
        reportingFrequency: {
          type: "dropdown",
          label: "Reporting Frequency",
          options: ["Daily", "Weekly", "Monthly", "Real-time"],
          default: "Daily"
        }
      },
      outputs: [
        "Daily Liquidity Dashboard",
        "Optimal Funding Allocation",
        "Contingency Plan Activation",
        "Operational Compliance Report",
        "Management Action Recommendations"
      ]
    },
    {
      id: "treasury-alm-controller",
      name: "Treasury & ALM Risk Controller",
      description: "Oversees treasury operations and asset-liability management to maintain financial stability, assessing FX and counterparty risks.",
      inputs: {
        text: "Upload cash positions, FX rates, counterparty limits, balance sheet data.",
        fileUploads: true
      },
      config: {
        baseCurrency: {
          type: "dropdown",
          label: "Base Currency",
          options: ["USD", "EUR", "GBP", "JPY"],
          default: "USD"
        },
        counterpartyRiskTolerance: {
          type: "slider",
          label: "Counterparty Risk Tolerance",
          min: 1,
          max: 5,
          default: 3
        },
        almPolicyStrictness: {
          type: "slider",
          label: "ALM Policy Strictness",
          min: 1,
          max: 5,
          default: 4
        }
      },
      outputs: [
        "FX & Counterparty Risk Assessment",
        "ALM Metrics Dashboard",
        "Policy Compliance Evaluation",
        "Risk Concentration Analysis",
        "Financial Equilibrium Recommendations"
      ]
    }
  ]
},


// ## wednesday
{
  id: "csrd-consultant",
  title: "CSRD & ESG Compliance Module",
  description: "Guides banks, insurers, and large corporations through CSRD/ESRS compliance, ESG reporting processes, report production, and continuous monitoring of regulatory developments.",
  icon: FileText,
  colorClass: "module-card-csrd",
  agents: [
    {
      id: "framework-analysis",
      name: "Framework Analysis",
      description: "Interprets CSRD and ESRS requirements, maps to ESG frameworks (EU Taxonomy, SFDR, TCFD, GRI, ISSB), and provides gap analyses and implementation roadmaps.",
      inputs: {
        text: "Upload ESG or sustainability data (CSV, Excel) and policy/report documents.",
        fileUploads: true
      },
      config: {
        frameworkFocus: {
          type: 'dropdown',
          label: 'Framework Focus',
          options: ['CSRD', 'ESRS', 'EU Taxonomy', 'GRI', 'ISSB', 'All'],
          default: 'CSRD'
        },
        analysisDepth: {
          type: 'slider',
          label: 'Gap Analysis Depth',
          min: 1,
          max: 5,
          default: 3
        },
        roadmapHorizon: {
          type: 'dropdown',
          label: 'Roadmap Horizon',
          options: ['Short-Term', 'Medium-Term', 'Long-Term'],
          default: 'Medium-Term'
        }
      },
      outputs: [
        'CSRD/ESRS Gap Analysis',
        'Compliance Readiness Report',
        'Framework Mapping Summary',
        'Phased Implementation Roadmap',
        'Executive Recommendations'
      ]
    },
    {
      id: "new-regulations-compliance",
      name: "New Regulations Compliance",
      description: "Supports materiality assessments, defines ESG data requirements, and ensures audit readiness for CSRD/ESRS compliance.",
      inputs: {
        text: "Upload ESG datasets (CSV, Excel) and internal compliance documents.",
        fileUploads: true
      },
      config: {
        materialityScope: {
          type: 'dropdown',
          label: 'Materiality Scope',
          options: ['Financial Materiality', 'Impact Materiality', 'Double Materiality'],
          default: 'Double Materiality'
        },
        auditReadinessLevel: {
          type: 'slider',
          label: 'Audit Readiness Level',
          min: 1,
          max: 5,
          default: 3
        },
        dataCoverage: {
          type: 'dropdown',
          label: 'Data Coverage Focus',
          options: ['Environmental', 'Social', 'Governance', 'Full ESG'],
          default: 'Full ESG'
        }
      },
      outputs: [
        'Materiality Assessment Report',
        'Data Requirement Mapping',
        'Audit Readiness Evaluation',
        'Compliance Action Plan',
        'Gap Closure Recommendations'
      ]
    },
    {
      id: "reporting-process-design",
      name: "Designing Reporting Processes",
      description: "Designs ESG reporting workflows, standardizes data collection, integrates systems, and strengthens governance for CSRD/ESRS compliance.",
      inputs: {
        text: "Upload ESG reporting data (CSV, Excel) and governance/policy documentation.",
        fileUploads: true
      },
      config: {
        workflowFocus: {
          type: 'dropdown',
          label: 'Workflow Focus',
          options: ['Data Collection', 'Validation Controls', 'Governance', 'Integration'],
          default: 'Integration'
        },
        automationLevel: {
          type: 'slider',
          label: 'Automation Level',
          min: 1,
          max: 5,
          default: 2
        },
        governanceStrength: {
          type: 'slider',
          label: 'Governance Maturity Level',
          min: 1,
          max: 5,
          default: 3
        }
      },
      outputs: [
        'Process Workflow Blueprint',
        'Data Collection & Validation Framework',
        'Governance & Control Recommendations',
        'System Integration Map',
        'Process Optimization Report'
      ]
    },
    {
      id: "compliant-report-production",
      name: "Producing Compliant Reports",
      description: "Structures CSRD-compliant reports with narrative and quantitative disclosures, reconciles ESG metrics with financials, and ensures audit-ready machine-readable outputs.",
      inputs: {
        text: "Upload ESG data (CSV, Excel) and financial statements or narratives.",
        fileUploads: true
      },
      config: {
        disclosureFormat: {
          type: 'dropdown',
          label: 'Disclosure Format',
          options: ['Narrative', 'Quantitative', 'Combined'],
          default: 'Combined'
        },
        reconciliationFocus: {
          type: 'dropdown',
          label: 'Reconciliation Focus',
          options: ['ESG with Financials', 'KPIs Only', 'Full Integration'],
          default: 'Full Integration'
        },
        outputFormat: {
          type: 'dropdown',
          label: 'Report Format',
          options: ['PDF', 'Excel', 'XHTML/ESEF'],
          default: 'XHTML/ESEF'
        }
      },
      outputs: [
        'CSRD-Compliant Draft Report',
        'Narrative & KPI Disclosures',
        'Financial Reconciliation Summary',
        'Audit-Ready Report Package',
        'Regulatory Submission File (ESEF/XHTML)'
      ]
    },
    {
      id: "continuous-monitoring",
      name: "Continuous Monitoring",
      description: "Tracks ESG regulatory updates, classifies impact, and recommends actions with compliance logs and training recommendations.",
      inputs: {
        text: "Upload regulatory update logs (CSV, Excel) or compliance notes.",
        fileUploads: true
      },
      config: {
        updateScope: {
          type: 'dropdown',
          label: 'Update Scope',
          options: ['CSRD', 'ESRS', 'ISSB', 'SEC', 'All'],
          default: 'All'
        },
        urgencyThreshold: {
          type: 'slider',
          label: 'Urgency Threshold (days)',
          min: 7,
          max: 90,
          default: 30
        },
        trainingFocus: {
          type: 'dropdown',
          label: 'Training Focus',
          options: ['Regulation Awareness', 'Process Adoption', 'Audit Preparation'],
          default: 'Regulation Awareness'
        }
      },
      outputs: [
        'Regulatory Update Tracker',
        'Compliance Impact Assessment',
        'Action & Deadline Log',
        'Training Recommendation Summary',
        'Executive Monitoring Report'
      ]
    }
  ]
},
];
