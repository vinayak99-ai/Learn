"""
LLM Research Platform - Enhanced Features Package

This package provides 14 innovative LLM-powered features for the Digital Asset Research Platform:
1. Semantic Search
2. Hypothesis Generation
3. Automatic Gaps Finder
4. Personalized Recommendations
5. Audience-Specific Reports
6. Contextual Alerts
7. Cross-Domain Insights
8. Forecasting Assistant
9. AI-Assisted Peer Review
10. Context-Aware Visualizations
11. Comprehensive Report Automation
12. Smart Experimentation Reusability
13. Integrated Sentiment Analysis
14. Comparative Analysis Assistant
"""

__version__ = "1.0.0"
__author__ = "Digital Asset Research Platform Team"

from .agents import (
    SemanticSearchAgent,
    HypothesisAgent,
    GapFinderAgent,
    RecommendationAgent,
    ReportGenerationAgent,
    AlertAgent,
    CrossDomainAgent,
    ForecastingAgent,
    PeerReviewAgent,
    VisualizationAgent,
    ReportAutomationAgent,
    ExperimentationAgent,
    SentimentAnalysisAgent,
    ComparativeAnalysisAgent,
)

__all__ = [
    "SemanticSearchAgent",
    "HypothesisAgent",
    "GapFinderAgent",
    "RecommendationAgent",
    "ReportGenerationAgent",
    "AlertAgent",
    "CrossDomainAgent",
    "ForecastingAgent",
    "PeerReviewAgent",
    "VisualizationAgent",
    "ReportAutomationAgent",
    "ExperimentationAgent",
    "SentimentAnalysisAgent",
    "ComparativeAnalysisAgent",
]
