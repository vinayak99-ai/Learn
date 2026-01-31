"""
Automatic Gaps Finder Agent

Identifies missing dimensions in research data and suggests additional data collection strategies.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class GapPriority(Enum):
    """Priority level for addressing gaps."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class DataGap:
    """Represents an identified gap in research data."""
    id: str
    gap_type: str  # "geographic", "temporal", "categorical", "dimensional"
    description: str
    affected_areas: List[str]
    priority: GapPriority
    impact_assessment: str
    recommendations: List[str]
    suggested_sources: List[str]
    estimated_effort: str  # "low", "medium", "high"
    created_at: datetime


class GapFinderAgent:
    """
    Agent for identifying gaps in research coverage.
    
    Features:
    - Dimensional analysis of research coverage
    - Comparison against research framework
    - Geographic, temporal, and categorical gap detection
    - Prioritized recommendations
    - Data source suggestions
    
    Example:
        >>> agent = GapFinderAgent()
        >>> gaps = agent.analyze_coverage(research_data, expected_framework)
        >>> for gap in gaps:
        ...     print(f"{gap.description} - Priority: {gap.priority}")
    """
    
    def __init__(
        self,
        research_framework: Optional[Dict[str, Any]] = None,
        llm_provider: str = "openai"
    ):
        """
        Initialize Gap Finder Agent.
        
        Args:
            research_framework: Expected research framework/ontology
            llm_provider: LLM provider for gap analysis
        """
        self.research_framework = research_framework or self._default_framework()
        self.llm_provider = llm_provider
        self.identified_gaps = []
        
    def analyze_coverage(
        self,
        current_data: Dict[str, Any],
        context: Optional[str] = None
    ) -> List[DataGap]:
        """
        Analyze current data coverage and identify gaps.
        
        Args:
            current_data: Current research data to analyze
            context: Additional context for gap analysis
            
        Returns:
            List of identified gaps
        """
        gaps = []
        
        # Analyze different dimensions
        gaps.extend(self._find_geographic_gaps(current_data))
        gaps.extend(self._find_temporal_gaps(current_data))
        gaps.extend(self._find_categorical_gaps(current_data))
        gaps.extend(self._find_dimensional_gaps(current_data))
        
        # Prioritize gaps
        gaps = self._prioritize_gaps(gaps, context)
        
        # Store identified gaps
        self.identified_gaps.extend(gaps)
        
        return gaps
    
    def _find_geographic_gaps(self, data: Dict[str, Any]) -> List[DataGap]:
        """
        Find gaps in geographic coverage.
        
        Args:
            data: Current data
            
        Returns:
            List of geographic gaps
        """
        gaps = []
        expected_regions = self.research_framework.get('regions', [
            'North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East', 'Africa'
        ])
        
        covered_regions = data.get('covered_regions', [])
        missing_regions = [r for r in expected_regions if r not in covered_regions]
        
        for region in missing_regions:
            gap = DataGap(
                id=f"geo_{region.replace(' ', '_').lower()}_{datetime.now().timestamp()}",
                gap_type="geographic",
                description=f"Data missing for region: {region}",
                affected_areas=[region],
                priority=self._assess_regional_priority(region),
                impact_assessment=f"Geographic analysis incomplete without {region} data",
                recommendations=[
                    f"Collect data from {region}-specific sources",
                    f"Include {region} in next research cycle",
                    "Consider regional partnerships for data access"
                ],
                suggested_sources=self._suggest_regional_sources(region),
                estimated_effort="medium",
                created_at=datetime.now()
            )
            gaps.append(gap)
        
        return gaps
    
    def _find_temporal_gaps(self, data: Dict[str, Any]) -> List[DataGap]:
        """
        Find gaps in temporal coverage.
        
        Args:
            data: Current data
            
        Returns:
            List of temporal gaps
        """
        gaps = []
        
        # Check for missing time periods
        expected_periods = data.get('expected_time_range', [])
        covered_periods = data.get('covered_time_range', [])
        
        # Identify missing periods
        missing_periods = self._identify_missing_periods(expected_periods, covered_periods)
        
        for period in missing_periods:
            gap = DataGap(
                id=f"temp_{period}_{datetime.now().timestamp()}",
                gap_type="temporal",
                description=f"Missing data for time period: {period}",
                affected_areas=["time_series_analysis", "trend_analysis"],
                priority=GapPriority.HIGH,
                impact_assessment="Temporal continuity broken, trend analysis may be inaccurate",
                recommendations=[
                    f"Backfill data for {period}",
                    "Adjust analysis to account for missing period",
                    "Use interpolation if appropriate"
                ],
                suggested_sources=["historical_database", "archive_api"],
                estimated_effort="high",
                created_at=datetime.now()
            )
            gaps.append(gap)
        
        return gaps
    
    def _find_categorical_gaps(self, data: Dict[str, Any]) -> List[DataGap]:
        """
        Find gaps in categorical coverage.
        
        Args:
            data: Current data
            
        Returns:
            List of categorical gaps
        """
        gaps = []
        expected_categories = self.research_framework.get('categories', [])
        covered_categories = data.get('covered_categories', [])
        
        missing_categories = [c for c in expected_categories if c not in covered_categories]
        
        for category in missing_categories:
            gap = DataGap(
                id=f"cat_{category.replace(' ', '_')}_{datetime.now().timestamp()}",
                gap_type="categorical",
                description=f"No data for category: {category}",
                affected_areas=[category],
                priority=GapPriority.MEDIUM,
                impact_assessment=f"Analysis incomplete without {category} coverage",
                recommendations=[
                    f"Add {category} to data collection pipeline",
                    f"Research availability of {category} data",
                    "Prioritize based on research goals"
                ],
                suggested_sources=self._suggest_category_sources(category),
                estimated_effort="low",
                created_at=datetime.now()
            )
            gaps.append(gap)
        
        return gaps
    
    def _find_dimensional_gaps(self, data: Dict[str, Any]) -> List[DataGap]:
        """
        Find gaps in dimensional coverage (missing metrics/dimensions).
        
        Args:
            data: Current data
            
        Returns:
            List of dimensional gaps
        """
        gaps = []
        expected_dimensions = self.research_framework.get('dimensions', [])
        
        for dimension in expected_dimensions:
            if not self._is_dimension_covered(dimension, data):
                gap = DataGap(
                    id=f"dim_{dimension['name'].replace(' ', '_')}_{datetime.now().timestamp()}",
                    gap_type="dimensional",
                    description=f"Missing dimension: {dimension['name']}",
                    affected_areas=dimension.get('affects', []),
                    priority=self._assess_dimension_priority(dimension),
                    impact_assessment=dimension.get('impact', 'Analysis may be incomplete'),
                    recommendations=[
                        f"Add {dimension['name']} to metrics collection",
                        "Review data sources for availability",
                        "Consider alternative proxies if direct data unavailable"
                    ],
                    suggested_sources=dimension.get('sources', []),
                    estimated_effort=dimension.get('effort', 'medium'),
                    created_at=datetime.now()
                )
                gaps.append(gap)
        
        return gaps
    
    def _prioritize_gaps(
        self,
        gaps: List[DataGap],
        context: Optional[str]
    ) -> List[DataGap]:
        """
        Prioritize gaps based on context and impact.
        
        Args:
            gaps: List of gaps to prioritize
            context: Additional context
            
        Returns:
            Prioritized list of gaps
        """
        # Sort by priority (critical > high > medium > low)
        priority_order = {
            GapPriority.CRITICAL: 0,
            GapPriority.HIGH: 1,
            GapPriority.MEDIUM: 2,
            GapPriority.LOW: 3
        }
        
        return sorted(gaps, key=lambda x: priority_order[x.priority])
    
    def generate_gap_report(self, gaps: Optional[List[DataGap]] = None) -> Dict[str, Any]:
        """
        Generate comprehensive gap analysis report.
        
        Args:
            gaps: Specific gaps to report (defaults to all identified gaps)
            
        Returns:
            Gap analysis report
        """
        gaps_to_report = gaps or self.identified_gaps
        
        return {
            'summary': {
                'total_gaps': len(gaps_to_report),
                'by_type': self._count_by_type(gaps_to_report),
                'by_priority': self._count_by_priority(gaps_to_report)
            },
            'critical_gaps': [g for g in gaps_to_report if g.priority == GapPriority.CRITICAL],
            'high_priority_gaps': [g for g in gaps_to_report if g.priority == GapPriority.HIGH],
            'all_gaps': gaps_to_report,
            'recommendations': self._aggregate_recommendations(gaps_to_report),
            'estimated_total_effort': self._estimate_total_effort(gaps_to_report)
        }
    
    def suggest_action_plan(self, gaps: List[DataGap]) -> Dict[str, Any]:
        """
        Suggest action plan for addressing gaps.
        
        Args:
            gaps: Gaps to address
            
        Returns:
            Action plan with priorities and timeline
        """
        # Group gaps by priority
        critical = [g for g in gaps if g.priority == GapPriority.CRITICAL]
        high = [g for g in gaps if g.priority == GapPriority.HIGH]
        medium = [g for g in gaps if g.priority == GapPriority.MEDIUM]
        low = [g for g in gaps if g.priority == GapPriority.LOW]
        
        return {
            'immediate_actions': {
                'description': 'Address critical and high-priority gaps immediately',
                'gaps': critical + high,
                'timeline': 'Week 1-2'
            },
            'short_term_actions': {
                'description': 'Address medium-priority gaps',
                'gaps': medium,
                'timeline': 'Week 3-4'
            },
            'long_term_actions': {
                'description': 'Address low-priority gaps as resources permit',
                'gaps': low,
                'timeline': 'Month 2+'
            },
            'resource_requirements': self._estimate_resources(gaps)
        }
    
    def _default_framework(self) -> Dict[str, Any]:
        """Create default research framework."""
        return {
            'regions': ['North America', 'Europe', 'Asia Pacific', 'Latin America'],
            'categories': ['DeFi', 'Layer 1', 'Layer 2', 'NFT', 'Infrastructure'],
            'dimensions': [
                {
                    'name': 'TVL',
                    'affects': ['protocol_health', 'market_analysis'],
                    'sources': ['defillama', 'dune'],
                    'effort': 'low'
                },
                {
                    'name': 'User Activity',
                    'affects': ['adoption_metrics', 'growth_analysis'],
                    'sources': ['flipside', 'allium'],
                    'effort': 'medium'
                },
                {
                    'name': 'Sentiment Analysis',
                    'affects': ['market_mood', 'risk_assessment'],
                    'sources': ['twitter_api', 'reddit_api'],
                    'effort': 'high'
                }
            ]
        }
    
    def _assess_regional_priority(self, region: str) -> GapPriority:
        """Assess priority for a regional gap."""
        high_priority_regions = ['North America', 'Europe', 'Asia Pacific']
        if region in high_priority_regions:
            return GapPriority.HIGH
        return GapPriority.MEDIUM
    
    def _suggest_regional_sources(self, region: str) -> List[str]:
        """Suggest data sources for a region."""
        # Placeholder: Map regions to data sources
        return ["regional_exchange_data", "regional_blockchain_analytics"]
    
    def _suggest_category_sources(self, category: str) -> List[str]:
        """Suggest data sources for a category."""
        # Placeholder: Map categories to sources
        return ["specialized_api", "category_database"]
    
    def _identify_missing_periods(
        self,
        expected: List[str],
        covered: List[str]
    ) -> List[str]:
        """Identify missing time periods."""
        return [p for p in expected if p not in covered]
    
    def _is_dimension_covered(self, dimension: Dict[str, Any], data: Dict[str, Any]) -> bool:
        """Check if a dimension is covered in data."""
        dimension_name = dimension['name']
        return dimension_name in data.get('metrics', [])
    
    def _assess_dimension_priority(self, dimension: Dict[str, Any]) -> GapPriority:
        """Assess priority for a dimensional gap."""
        # Placeholder: Use impact and criticality to assess priority
        if len(dimension.get('affects', [])) > 2:
            return GapPriority.HIGH
        return GapPriority.MEDIUM
    
    def _count_by_type(self, gaps: List[DataGap]) -> Dict[str, int]:
        """Count gaps by type."""
        counts = {}
        for gap in gaps:
            counts[gap.gap_type] = counts.get(gap.gap_type, 0) + 1
        return counts
    
    def _count_by_priority(self, gaps: List[DataGap]) -> Dict[str, int]:
        """Count gaps by priority."""
        counts = {}
        for gap in gaps:
            priority_str = gap.priority.value
            counts[priority_str] = counts.get(priority_str, 0) + 1
        return counts
    
    def _aggregate_recommendations(self, gaps: List[DataGap]) -> List[str]:
        """Aggregate recommendations from all gaps."""
        all_recommendations = []
        for gap in gaps:
            all_recommendations.extend(gap.recommendations)
        # Remove duplicates while preserving order
        return list(dict.fromkeys(all_recommendations))
    
    def _estimate_total_effort(self, gaps: List[DataGap]) -> str:
        """Estimate total effort for addressing gaps."""
        effort_scores = {'low': 1, 'medium': 3, 'high': 5}
        total_score = sum(effort_scores.get(gap.estimated_effort, 3) for gap in gaps)
        
        if total_score < 10:
            return "low"
        elif total_score < 25:
            return "medium"
        else:
            return "high"
    
    def _estimate_resources(self, gaps: List[DataGap]) -> Dict[str, Any]:
        """Estimate resources needed to address gaps."""
        return {
            'data_sources_needed': len(set(
                source for gap in gaps for source in gap.suggested_sources
            )),
            'estimated_person_weeks': len(gaps) * 0.5,  # Rough estimate
            'budget_implications': 'To be determined based on data source costs'
        }


# Example usage
if __name__ == "__main__":
    agent = GapFinderAgent()
    
    # Sample data with gaps
    current_research = {
        'covered_regions': ['North America', 'Europe'],
        'covered_categories': ['DeFi', 'Layer 1'],
        'metrics': ['TVL'],
        'covered_time_range': ['Q1 2023', 'Q2 2023'],
        'expected_time_range': ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']
    }
    
    # Analyze gaps
    gaps = agent.analyze_coverage(current_research)
    
    print(f"Found {len(gaps)} gaps:")
    for gap in gaps:
        print(f"\n{gap.priority.value.upper()}: {gap.description}")
        print(f"  Impact: {gap.impact_assessment}")
        print(f"  Recommendations: {gap.recommendations[0]}")
    
    # Generate report
    report = agent.generate_gap_report(gaps)
    print(f"\nGap Analysis Summary:")
    print(f"  Total gaps: {report['summary']['total_gaps']}")
    print(f"  By priority: {report['summary']['by_priority']}")
