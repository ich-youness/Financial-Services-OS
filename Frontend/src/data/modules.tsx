import { 
  Shield, 
  TrendingUp, 
  Users, 
  AlertTriangle, 
  FileCheck, 
  Headphones,
  LucideIcon 
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
  }
];