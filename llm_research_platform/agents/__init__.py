"""
Agent implementations for LLM Research Platform enhancements.
"""

from .semantic_search import SemanticSearchAgent
from .hypothesis_generation import HypothesisAgent
from .gap_finder import GapFinderAgent
from .recommendations import RecommendationAgent
from .report_generation import ReportGenerationAgent
from .alerts import AlertAgent
from .cross_domain import CrossDomainAgent
from .forecasting import ForecastingAgent
from .peer_review import PeerReviewAgent
from .visualization import VisualizationAgent
from .report_automation import ReportAutomationAgent
from .experimentation import ExperimentationAgent
from .sentiment_analysis import SentimentAnalysisAgent
from .comparative_analysis import ComparativeAnalysisAgent

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
