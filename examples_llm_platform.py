"""
LLM Research Platform - Example Usage

This file demonstrates how to use the 14 enhanced features for the
Digital Asset Research Platform.
"""

from llm_research_platform.agents import (
    SemanticSearchAgent,
    HypothesisAgent,
    GapFinderAgent,
    RecommendationAgent,
    AlertAgent,
    SentimentAnalysisAgent,
    ForecastingAgent,
    ComparativeAnalysisAgent,
)
from datetime import datetime
import numpy as np


def example_semantic_search():
    """Example: Using Semantic Search to find research documents."""
    print("=" * 80)
    print("EXAMPLE 1: Semantic Search Across Research Histories")
    print("=" * 80)
    
    # Initialize agent
    agent = SemanticSearchAgent()
    
    # Index some sample documents
    documents = [
        {
            'id': 'doc_001',
            'title': 'Q3 2023 Supply Chain Optimization Study',
            'content': 'Comprehensive analysis of supply chain optimization strategies in blockchain logistics...',
            'type': 'monthly_wrap',
            'created_at': datetime(2023, 9, 30),
            'metadata': {'tags': ['supply-chain', 'optimization', 'Q3-2023']}
        },
        {
            'id': 'doc_002',
            'title': 'DeFi Protocol Analysis Q4 2023',
            'content': 'Deep dive into DeFi lending protocols and their TVL dynamics...',
            'type': 'research_report',
            'created_at': datetime(2023, 12, 15),
            'metadata': {'tags': ['DeFi', 'TVL', 'lending']}
        }
    ]
    
    for doc in documents:
        agent.index_document(doc)
    
    # Search using natural language
    query = "Find all studies about supply chain optimization in last two quarters"
    results = agent.search(query, top_k=5, time_filter="last quarter")
    
    print(f"\nQuery: '{query}'")
    print(f"Found {len(results)} results:\n")
    for result in results:
        print(f"  - {result.title}")
        print(f"    Score: {result.score:.3f} | Type: {result.document_type}")
        print(f"    Date: {result.created_at.strftime('%Y-%m-%d')}\n")
    
    # Get statistics
    stats = agent.get_statistics()
    print(f"Index Statistics:")
    print(f"  Total documents: {stats['total_documents']}")
    print(f"  Document types: {stats['document_types']}")


def example_hypothesis_generation():
    """Example: Generating and validating hypotheses."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Hypothesis Generation and Validation")
    print("=" * 80)
    
    agent = HypothesisAgent()
    
    # Generate hypotheses
    hypotheses = agent.generate_hypothesis(
        context="DeFi Protocol Market Analysis",
        focus_areas=["TVL", "market_cap", "user_growth"],
        num_hypotheses=3
    )
    
    print(f"\nGenerated {len(hypotheses)} hypotheses:\n")
    for i, hyp in enumerate(hypotheses, 1):
        print(f"{i}. {hyp.statement}")
        print(f"   Variables: {', '.join(hyp.variables)}")
        print(f"   Data sources needed: {', '.join(hyp.data_sources)}\n")
    
    # Validate first hypothesis with sample data
    sample_data = {
        'TVL': np.random.rand(100) * 1000,  # Sample TVL data
        'market_cap': np.random.rand(100) * 5000  # Sample market cap data
    }
    
    result = agent.validate_hypothesis(hypotheses[0], sample_data)
    
    print(f"Validation Results for Hypothesis 1:")
    print(f"  Status: {result.status.value}")
    print(f"  Correlation: {result.correlation_coefficient:.3f}")
    print(f"  P-value: {result.p_value:.4f}")
    print(f"  Confidence Interval: {result.confidence_interval}")
    print(f"  Conclusion: {result.conclusion}")


def example_gap_finder():
    """Example: Finding gaps in research coverage."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Automatic Gaps Finder")
    print("=" * 80)
    
    agent = GapFinderAgent()
    
    # Analyze current research coverage
    current_research = {
        'covered_regions': ['North America', 'Europe'],
        'covered_categories': ['DeFi', 'Layer 1'],
        'metrics': ['TVL', 'User Activity'],
        'covered_time_range': ['Q1 2023', 'Q2 2023'],
        'expected_time_range': ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']
    }
    
    gaps = agent.analyze_coverage(current_research)
    
    print(f"\nIdentified {len(gaps)} gaps in research coverage:\n")
    for gap in gaps[:5]:  # Show first 5
        print(f"  {gap.priority.value.upper()}: {gap.description}")
        print(f"    Impact: {gap.impact_assessment}")
        print(f"    Recommendations:")
        for rec in gap.recommendations[:2]:
            print(f"      - {rec}")
        print()
    
    # Generate gap report
    report = agent.generate_gap_report(gaps)
    print(f"Gap Analysis Summary:")
    print(f"  Total gaps: {report['summary']['total_gaps']}")
    print(f"  By priority: {report['summary']['by_priority']}")
    print(f"  Estimated effort: {report['estimated_total_effort']}")


def example_recommendations():
    """Example: Personalized recommendations for researchers."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Personalized Recommendations")
    print("=" * 80)
    
    agent = RecommendationAgent()
    
    # Add content to database
    content_items = [
        {
            'id': 'content_001',
            'type': 'research',
            'title': 'Advanced DeFi Strategies Q4 2023',
            'description': 'Comprehensive analysis of emerging DeFi strategies',
            'tags': ['DeFi', 'strategies', 'Q4-2023'],
            'url': 'https://example.com/defi-strategies'
        },
        {
            'id': 'content_002',
            'type': 'dataset',
            'title': 'Ethereum L2 Metrics Dataset',
            'description': 'Complete dataset of Layer 2 scaling solutions',
            'tags': ['Ethereum', 'Layer 2', 'metrics'],
            'url': 'https://example.com/l2-dataset'
        }
    ]
    
    for item in content_items:
        agent.add_content(item)
    
    # Track user activities
    activities = [
        {'type': 'view', 'item_id': 'content_001', 'category': 'DeFi', 'tags': ['DeFi']},
        {'type': 'like', 'item_id': 'content_001', 'category': 'DeFi', 'tags': ['DeFi']},
        {'type': 'view', 'item_id': 'content_002', 'category': 'Layer 2', 'tags': ['Layer 2']},
    ]
    
    for activity in activities:
        agent.track_activity('researcher_001', activity)
    
    # Get recommendations
    recommendations = agent.get_recommendations('researcher_001', limit=5)
    
    print(f"\nPersonalized recommendations for Researcher 001:\n")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec.title} ({rec.type})")
        print(f"   Relevance: {rec.relevance_score:.2f}")
        print(f"   Reason: {rec.reasons[0]}")
        if rec.url:
            print(f"   URL: {rec.url}")
        print()


def example_contextual_alerts():
    """Example: Contextual alerts with suggested actions."""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Contextual Alerts with Suggested Actions")
    print("=" * 80)
    
    agent = AlertAgent()
    
    # Create alert from anomaly detection
    alert = agent.create_alert(
        anomaly_data={
            'metric': 'EU_market_demand',
            'change': -15,
            'current_value': 850,
            'expected_value': 1000,
            'data_quality': 0.95
        },
        context={
            'region': 'EU',
            'timeframe': 'week',
            'comparison': 'week-over-week'
        }
    )
    
    print(f"\nAlert Generated:")
    print(f"  Title: {alert.title}")
    print(f"  Priority: {alert.priority.value}")
    print(f"  Confidence: {alert.confidence:.1%}")
    print(f"  Description: {alert.description}")
    print(f"\n  Root Causes:")
    for cause in alert.root_causes:
        print(f"    - {cause}")
    print(f"\n  Impact: {alert.impact_assessment}")
    print(f"\n  Suggested Actions:")
    for i, action in enumerate(alert.suggested_actions, 1):
        print(f"    {i}. {action.action}")
        print(f"       Impact: {action.impact_level} | Effort: {action.effort_required}")
        print(f"       Expected outcome: {action.expected_outcome}")
        print(f"       Confidence: {action.confidence:.0%}\n")


def example_sentiment_analysis():
    """Example: Integrated sentiment analysis."""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Integrated Sentiment Analysis")
    print("=" * 80)
    
    agent = SentimentAnalysisAgent()
    
    # Analyze sentiment for Ethereum
    result = agent.analyze_sentiment(
        entity="Ethereum",
        sources=["twitter", "reddit", "news"],
        timeframe="7d"
    )
    
    print(f"\nSentiment Analysis for {result.entity}:")
    print(f"  Overall Sentiment: {result.sentiment_label.value}")
    print(f"  Score: {result.overall_score:.2f} (range: -1 to +1)")
    print(f"  Volume: {result.volume} mentions")
    print(f"  Trend: {result.trend}")
    
    print(f"\n  Aspect Breakdown:")
    for aspect, score in result.breakdown.items():
        sentiment = "Positive" if score > 0.1 else "Negative" if score < -0.1 else "Neutral"
        print(f"    {aspect}: {score:.2f} ({sentiment})")
    
    if result.risk_signals:
        print(f"\n  Risk Signals:")
        for signal in result.risk_signals:
            print(f"    ⚠ {signal}")
    
    if result.opportunities:
        print(f"\n  Opportunities:")
        for opp in result.opportunities:
            print(f"    ✓ {opp}")


def example_forecasting():
    """Example: Forecasting and predictive analytics."""
    print("\n" + "=" * 80)
    print("EXAMPLE 7: Forecasting and Predictive Analytics")
    print("=" * 80)
    
    agent = ForecastingAgent()
    
    # Historical TVL data (in billions)
    historical_data = [30, 32, 35, 38, 37, 39, 40, 42, 43]
    
    # Generate forecast
    forecast = agent.forecast(
        metric="Ethereum TVL",
        historical_data=historical_data,
        periods=30
    )
    
    print(f"\nForecast for {forecast.metric} (next quarter):")
    print(f"  Base Case: ${forecast.base_case:.2f}B")
    print(f"  Bull Case: ${forecast.bull_case:.2f}B (prob: {forecast.scenario_probabilities['bull']:.0%})")
    print(f"  Bear Case: ${forecast.bear_case:.2f}B (prob: {forecast.scenario_probabilities['bear']:.0%})")
    
    print(f"\n  Model Used: {forecast.model_used.value}")
    print(f"  Model Accuracy: {forecast.accuracy_score:.1%}")
    
    # Show first few forecast values
    print(f"\n  Next 7 days forecast:")
    for i, (date, value) in enumerate(zip(forecast.forecast_dates[:7], forecast.forecast_values[:7])):
        ci_lower, ci_upper = forecast.confidence_intervals[i]
        print(f"    {date.strftime('%Y-%m-%d')}: ${value:.2f}B (CI: ${ci_lower:.2f}B - ${ci_upper:.2f}B)")


def example_comparative_analysis():
    """Example: Comparative analysis assistant."""
    print("\n" + "=" * 80)
    print("EXAMPLE 8: Comparative Analysis Assistant")
    print("=" * 80)
    
    agent = ComparativeAnalysisAgent()
    
    # Compare Layer 2 solutions
    result = agent.compare(
        entities=["Arbitrum", "Optimism", "zkSync"],
        dimensions={
            "TVL_billions": [2.5, 1.8, 0.7],
            "Daily_Users_thousands": [150, 120, 45],
            "Transaction_Cost_dollars": [0.15, 0.18, 0.12],
            "TPS_thousands": [40, 35, 20]
        },
        dimension_metadata={
            "TVL_billions": {"unit": "B", "higher_is_better": True},
            "Daily_Users_thousands": {"unit": "K", "higher_is_better": True},
            "Transaction_Cost_dollars": {"unit": "$", "higher_is_better": False},
            "TPS_thousands": {"unit": "K", "higher_is_better": True}
        }
    )
    
    print(f"\nComparative Analysis: Layer 2 Scaling Solutions")
    print(f"Overall Winner: {result.overall_winner}")
    print(f"Confidence: {result.confidence_score:.1%}")
    
    print(f"\n  Rankings:")
    for entity, rank in sorted(result.rankings.items(), key=lambda x: x[1]):
        print(f"    {rank}. {entity}")
    
    print(f"\n  Winners by Dimension:")
    for dimension, winner in result.winner_by_dimension.items():
        print(f"    {dimension}: {winner}")
    
    print(f"\n  Comparative Strengths:")
    for entity, strengths in result.strengths.items():
        if strengths:
            print(f"    {entity}: {', '.join(strengths)}")
    
    print(f"\n  Recommendations:")
    for entity, rec in result.recommendations.items():
        print(f"    {entity}: {rec}")
    
    # Generate comparison table
    print(f"\n  Detailed Comparison Table:")
    table = agent.generate_comparison_table(result)
    print(table)


def main():
    """Run all examples."""
    print("\n")
    print("*" * 80)
    print("LLM RESEARCH PLATFORM - COMPREHENSIVE EXAMPLES")
    print("*" * 80)
    
    try:
        example_semantic_search()
        example_hypothesis_generation()
        example_gap_finder()
        example_recommendations()
        example_contextual_alerts()
        example_sentiment_analysis()
        example_forecasting()
        example_comparative_analysis()
        
        print("\n" + "=" * 80)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nFor more information, see:")
        print("  - LLM_Research_Enhancements.md: Complete feature specifications")
        print("  - llm_research_platform/: Source code for all agents")
        print("  - requirements.txt: Required dependencies")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
