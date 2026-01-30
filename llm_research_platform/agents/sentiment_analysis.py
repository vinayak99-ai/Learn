"""
Integrated Sentiment Analysis Agent

Analyzes sentiment trends within feedback reports or external datasets.
Provides actionable insights for user satisfaction and risk prevention.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class SentimentLabel(Enum):
    """Sentiment classification labels."""
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"


@dataclass
class SentimentResult:
    """Represents sentiment analysis result."""
    entity: str  # Entity being analyzed (e.g., "Ethereum", "DeFi")
    overall_score: float  # -1 to +1
    sentiment_label: SentimentLabel
    volume: int  # Number of mentions
    trend: str  # "improving", "declining", "stable"
    breakdown: Dict[str, float]  # Aspect-level sentiments
    risk_signals: List[str]
    opportunities: List[str]


@dataclass
class SentimentTrend:
    """Represents sentiment trend over time."""
    entity: str
    time_series: List[Tuple[datetime, float]]
    change_pct: float
    volatility: float


class SentimentAnalysisAgent:
    """
    Agent for analyzing sentiment across multiple sources.
    
    Features:
    - Multi-source sentiment extraction (Twitter, Discord, Reddit, News)
    - Trend analysis over time
    - Entity-level sentiment tracking
    - Aspect-based sentiment analysis
    - Risk signal identification
    
    Example:
        >>> agent = SentimentAnalysisAgent()
        >>> result = agent.analyze_sentiment(
        ...     entity="Ethereum",
        ...     sources=["twitter", "reddit"],
        ...     timeframe="7d"
        ... )
        >>> print(f"{result.entity}: {result.sentiment_label.value} ({result.overall_score:.2f})")
    """
    
    def __init__(
        self,
        llm_provider: str = "openai",
        sentiment_model: str = "default"
    ):
        """
        Initialize Sentiment Analysis Agent.
        
        Args:
            llm_provider: LLM provider
            sentiment_model: Sentiment classification model
        """
        self.llm_provider = llm_provider
        self.sentiment_model = sentiment_model
        self.sentiment_history = []
    
    def analyze_sentiment(
        self,
        entity: str,
        sources: List[str],
        timeframe: str = "7d",
        aspects: Optional[List[str]] = None
    ) -> SentimentResult:
        """
        Analyze sentiment for an entity across sources.
        
        Args:
            entity: Entity to analyze (e.g., "Ethereum", "DeFi")
            sources: Data sources to analyze
            timeframe: Time period to analyze
            aspects: Specific aspects to analyze
            
        Returns:
            SentimentResult with comprehensive analysis
        """
        # Collect data from sources
        data = self._collect_data(entity, sources, timeframe)
        
        # Perform sentiment analysis
        overall_score = self._calculate_overall_sentiment(data)
        sentiment_label = self._score_to_label(overall_score)
        
        # Analyze aspects
        aspect_breakdown = self._analyze_aspects(data, aspects)
        
        # Identify trends
        trend = self._identify_trend(entity, overall_score)
        
        # Detect risk signals
        risk_signals = self._detect_risk_signals(data, overall_score)
        
        # Identify opportunities
        opportunities = self._identify_opportunities(data, overall_score)
        
        result = SentimentResult(
            entity=entity,
            overall_score=overall_score,
            sentiment_label=sentiment_label,
            volume=len(data),
            trend=trend,
            breakdown=aspect_breakdown,
            risk_signals=risk_signals,
            opportunities=opportunities
        )
        
        # Store in history
        self.sentiment_history.append({
            'entity': entity,
            'score': overall_score,
            'timestamp': datetime.now()
        })
        
        return result
    
    def analyze_sentiment_trend(
        self,
        entity: str,
        period_days: int = 30
    ) -> SentimentTrend:
        """
        Analyze sentiment trend over time.
        
        Args:
            entity: Entity to analyze
            period_days: Number of days to analyze
            
        Returns:
            SentimentTrend object
        """
        # Get historical sentiment data
        cutoff_date = datetime.now() - timedelta(days=period_days)
        historical_data = [
            (entry['timestamp'], entry['score'])
            for entry in self.sentiment_history
            if entry['entity'] == entity and entry['timestamp'] >= cutoff_date
        ]
        
        if len(historical_data) < 2:
            # Not enough historical data
            return SentimentTrend(
                entity=entity,
                time_series=[],
                change_pct=0.0,
                volatility=0.0
            )
        
        # Calculate change percentage
        first_score = historical_data[0][1]
        last_score = historical_data[-1][1]
        change_pct = ((last_score - first_score) / abs(first_score)) * 100 if first_score != 0 else 0
        
        # Calculate volatility
        scores = [score for _, score in historical_data]
        volatility = self._calculate_volatility(scores)
        
        return SentimentTrend(
            entity=entity,
            time_series=historical_data,
            change_pct=change_pct,
            volatility=volatility
        )
    
    def compare_sentiment(
        self,
        entities: List[str],
        sources: List[str],
        timeframe: str = "7d"
    ) -> Dict[str, SentimentResult]:
        """
        Compare sentiment across multiple entities.
        
        Args:
            entities: List of entities to compare
            sources: Data sources
            timeframe: Time period
            
        Returns:
            Dictionary mapping entities to sentiment results
        """
        results = {}
        for entity in entities:
            results[entity] = self.analyze_sentiment(entity, sources, timeframe)
        return results
    
    def _collect_data(
        self,
        entity: str,
        sources: List[str],
        timeframe: str
    ) -> List[Dict[str, Any]]:
        """
        Collect data from multiple sources.
        
        Args:
            entity: Entity to search for
            sources: Sources to collect from
            timeframe: Time period
            
        Returns:
            List of data items
        """
        # Placeholder: Collect actual data from APIs
        # - Twitter API
        # - Reddit API
        # - Discord API
        # - News aggregators
        
        # Simulated data
        import random
        data = []
        for i in range(100):
            data.append({
                'text': f"Sample text about {entity}",
                'source': random.choice(sources),
                'timestamp': datetime.now() - timedelta(hours=random.randint(0, 168)),
                'engagement': random.randint(1, 100)
            })
        
        return data
    
    def _calculate_overall_sentiment(self, data: List[Dict[str, Any]]) -> float:
        """
        Calculate overall sentiment score.
        
        Args:
            data: List of data items
            
        Returns:
            Sentiment score between -1 and +1
        """
        # Placeholder: Use sentiment model to classify texts
        # - BERT-based sentiment models
        # - RoBERTa
        # - Custom fine-tuned models
        
        # Simulated sentiment scores
        import random
        scores = []
        for item in data:
            # Weight by engagement
            score = random.uniform(-1, 1)
            weight = item.get('engagement', 1)
            scores.extend([score] * min(weight, 10))
        
        if not scores:
            return 0.0
        
        return sum(scores) / len(scores)
    
    def _score_to_label(self, score: float) -> SentimentLabel:
        """Convert numeric score to sentiment label."""
        if score >= 0.5:
            return SentimentLabel.VERY_POSITIVE
        elif score >= 0.1:
            return SentimentLabel.POSITIVE
        elif score >= -0.1:
            return SentimentLabel.NEUTRAL
        elif score >= -0.5:
            return SentimentLabel.NEGATIVE
        else:
            return SentimentLabel.VERY_NEGATIVE
    
    def _analyze_aspects(
        self,
        data: List[Dict[str, Any]],
        aspects: Optional[List[str]]
    ) -> Dict[str, float]:
        """
        Perform aspect-based sentiment analysis.
        
        Args:
            data: Data items
            aspects: Specific aspects to analyze
            
        Returns:
            Dictionary of aspect sentiments
        """
        # Default aspects if not specified
        if not aspects:
            aspects = [
                "technology",
                "governance",
                "community",
                "performance",
                "security"
            ]
        
        # Placeholder: Analyze sentiment for each aspect
        import random
        aspect_sentiments = {}
        for aspect in aspects:
            aspect_sentiments[aspect] = random.uniform(-1, 1)
        
        return aspect_sentiments
    
    def _identify_trend(self, entity: str, current_score: float) -> str:
        """Identify sentiment trend."""
        # Look at recent history
        recent_history = [
            entry['score']
            for entry in self.sentiment_history[-10:]
            if entry['entity'] == entity
        ]
        
        if len(recent_history) < 2:
            return "stable"
        
        # Compare current to average of recent history
        avg_recent = sum(recent_history) / len(recent_history)
        
        if current_score > avg_recent + 0.1:
            return "improving"
        elif current_score < avg_recent - 0.1:
            return "declining"
        else:
            return "stable"
    
    def _detect_risk_signals(
        self,
        data: List[Dict[str, Any]],
        overall_score: float
    ) -> List[str]:
        """
        Detect risk signals from sentiment data.
        
        Args:
            data: Data items
            overall_score: Overall sentiment score
            
        Returns:
            List of risk signals
        """
        risk_signals = []
        
        # Check for negative sentiment
        if overall_score < -0.3:
            risk_signals.append("Strong negative sentiment detected")
        
        # Check for sudden changes (placeholder)
        # Would compare to historical data
        
        # Check for specific negative keywords (placeholder)
        negative_keywords = ['scam', 'hack', 'vulnerability', 'risk', 'concern']
        for item in data:
            text = item.get('text', '').lower()
            for keyword in negative_keywords:
                if keyword in text:
                    risk_signals.append(f"Increased mentions of '{keyword}'")
                    break
        
        # Remove duplicates
        return list(set(risk_signals))
    
    def _identify_opportunities(
        self,
        data: List[Dict[str, Any]],
        overall_score: float
    ) -> List[str]:
        """
        Identify opportunities from sentiment data.
        
        Args:
            data: Data items
            overall_score: Overall sentiment score
            
        Returns:
            List of opportunities
        """
        opportunities = []
        
        # Check for positive sentiment
        if overall_score > 0.3:
            opportunities.append("Strong positive sentiment - potential growth opportunity")
        
        # Check for positive keywords (placeholder)
        positive_keywords = ['innovative', 'growth', 'adoption', 'partnership', 'upgrade']
        for item in data:
            text = item.get('text', '').lower()
            for keyword in positive_keywords:
                if keyword in text:
                    opportunities.append(f"Positive buzz around '{keyword}'")
                    break
        
        # Remove duplicates
        return list(set(opportunities))
    
    def _calculate_volatility(self, scores: List[float]) -> float:
        """Calculate volatility of sentiment scores."""
        if len(scores) < 2:
            return 0.0
        
        # Calculate standard deviation
        mean = sum(scores) / len(scores)
        variance = sum((x - mean) ** 2 for x in scores) / len(scores)
        return variance ** 0.5
    
    def generate_sentiment_report(
        self,
        entities: List[str],
        sources: List[str]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive sentiment report.
        
        Args:
            entities: Entities to analyze
            sources: Data sources
            
        Returns:
            Comprehensive sentiment report
        """
        results = self.compare_sentiment(entities, sources)
        
        return {
            'summary': {
                'total_entities': len(entities),
                'positive_entities': len([r for r in results.values() if r.overall_score > 0.1]),
                'negative_entities': len([r for r in results.values() if r.overall_score < -0.1]),
                'neutral_entities': len([r for r in results.values() if -0.1 <= r.overall_score <= 0.1])
            },
            'entity_results': results,
            'top_risks': self._aggregate_top_risks(results),
            'top_opportunities': self._aggregate_top_opportunities(results)
        }
    
    def _aggregate_top_risks(self, results: Dict[str, SentimentResult]) -> List[Dict[str, Any]]:
        """Aggregate top risk signals across entities."""
        all_risks = []
        for entity, result in results.items():
            for risk in result.risk_signals:
                all_risks.append({'entity': entity, 'risk': risk})
        return all_risks[:5]  # Top 5
    
    def _aggregate_top_opportunities(self, results: Dict[str, SentimentResult]) -> List[Dict[str, Any]]:
        """Aggregate top opportunities across entities."""
        all_opportunities = []
        for entity, result in results.items():
            for opp in result.opportunities:
                all_opportunities.append({'entity': entity, 'opportunity': opp})
        return all_opportunities[:5]  # Top 5


# Example usage
if __name__ == "__main__":
    agent = SentimentAnalysisAgent()
    
    # Analyze sentiment
    result = agent.analyze_sentiment(
        entity="Ethereum",
        sources=["twitter", "reddit", "news"],
        timeframe="7d"
    )
    
    print(f"Sentiment Analysis for {result.entity}:")
    print(f"  Overall: {result.sentiment_label.value} ({result.overall_score:.2f})")
    print(f"  Volume: {result.volume} mentions")
    print(f"  Trend: {result.trend}")
    print(f"\nAspect Breakdown:")
    for aspect, score in result.breakdown.items():
        print(f"  {aspect}: {score:.2f}")
    print(f"\nRisk Signals:")
    for risk in result.risk_signals:
        print(f"  - {risk}")
    print(f"\nOpportunities:")
    for opp in result.opportunities:
        print(f"  - {opp}")
