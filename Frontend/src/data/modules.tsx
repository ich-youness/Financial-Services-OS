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
  Banknote
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
    };
  };
  outputs: string[];
}

export interface Module {
  id: string;
  title: string;
  description: string;
  icon: LucideIcon;
  colorClass: string;
  agents?: Agent[];
}

export const modules: Module[] = [
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
  description: "Centralized reporting framework for subsidiaries, ensuring compliance, consolidation, validation, and continuous optimization of the group’s financial closing process.",
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
}





];