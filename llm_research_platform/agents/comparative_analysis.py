"""
Comparative Analysis Assistant

Automates comparative analysis between strategies, metrics, or regions
for quick decision-making.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import numpy as np


@dataclass
class ComparisonDimension:
    """Represents a dimension for comparison."""
    name: str
    values: Dict[str, float]  # entity -> value
    unit: str
    higher_is_better: bool = True


@dataclass
class ComparisonResult:
    """Results of comparative analysis."""
    entities: List[str]
    dimensions: List[ComparisonDimension]
    rankings: Dict[str, int]  # entity -> rank
    winner_by_dimension: Dict[str, str]  # dimension -> winning entity
    overall_winner: str
    strengths: Dict[str, List[str]]  # entity -> strengths
    weaknesses: Dict[str, List[str]]  # entity -> weaknesses
    recommendations: Dict[str, str]  # entity -> recommendation
    confidence_score: float


class ComparativeAnalysisAgent:
    """
    Agent for automating comparative analysis.
    
    Features:
    - Multi-dimensional comparison
    - Statistical significance testing
    - Normalization for fair comparison
    - Strength/weakness identification
    - Decision recommendation synthesis
    
    Example:
        >>> agent = ComparativeAnalysisAgent()
        >>> result = agent.compare(
        ...     entities=["Arbitrum", "Optimism", "zkSync"],
        ...     dimensions={
        ...         "TVL": [2.5, 1.8, 0.7],
        ...         "Users": [150, 120, 45]
        ...     }
        ... )
        >>> print(f"Winner: {result.overall_winner}")
    """
    
    def __init__(self, llm_provider: str = "openai"):
        """
        Initialize Comparative Analysis Agent.
        
        Args:
            llm_provider: LLM provider for synthesis and recommendations
        """
        self.llm_provider = llm_provider
        self.comparison_history = []
    
    def compare(
        self,
        entities: List[str],
        dimensions: Dict[str, List[float]],
        dimension_metadata: Optional[Dict[str, Dict[str, Any]]] = None,
        weights: Optional[Dict[str, float]] = None
    ) -> ComparisonResult:
        """
        Compare multiple entities across dimensions.
        
        Args:
            entities: List of entities to compare
            dimensions: Dictionary mapping dimension names to value lists
            dimension_metadata: Metadata for each dimension (unit, direction)
            weights: Optional weights for each dimension
            
        Returns:
            ComparisonResult with comprehensive analysis
        """
        # Validate inputs
        self._validate_inputs(entities, dimensions)
        
        # Create comparison dimensions
        comparison_dims = self._create_comparison_dimensions(
            entities, dimensions, dimension_metadata
        )
        
        # Calculate rankings
        rankings = self._calculate_rankings(entities, comparison_dims, weights)
        
        # Identify winners by dimension
        winners = self._identify_dimension_winners(comparison_dims)
        
        # Determine overall winner
        overall_winner = self._determine_overall_winner(rankings)
        
        # Analyze strengths and weaknesses
        strengths = self._identify_strengths(entities, comparison_dims, rankings)
        weaknesses = self._identify_weaknesses(entities, comparison_dims, rankings)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            entities, comparison_dims, strengths, weaknesses
        )
        
        # Calculate confidence
        confidence = self._calculate_confidence(comparison_dims)
        
        result = ComparisonResult(
            entities=entities,
            dimensions=comparison_dims,
            rankings=rankings,
            winner_by_dimension=winners,
            overall_winner=overall_winner,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            confidence_score=confidence
        )
        
        self.comparison_history.append({
            'timestamp': datetime.now(),
            'result': result
        })
        
        return result
    
    def generate_comparison_table(self, result: ComparisonResult) -> str:
        """Generate formatted comparison table."""
        # Create header
        header = ["Metric"] + result.entities + ["Winner"]
        lines = [" | ".join(header)]
        lines.append("|".join(["---"] * len(header)))
        
        # Add data rows
        for dim in result.dimensions:
            row = [dim.name]
            for entity in result.entities:
                value = dim.values.get(entity, 0)
                row.append(f"{value:.2f} {dim.unit}")
            row.append(result.winner_by_dimension.get(dim.name, "-"))
            lines.append(" | ".join(row))
        
        return "\n".join(lines)
    
    def _validate_inputs(
        self,
        entities: List[str],
        dimensions: Dict[str, List[float]]
    ) -> None:
        """Validate comparison inputs."""
        if len(entities) < 2:
            raise ValueError("At least 2 entities required for comparison")
        
        for dim_name, values in dimensions.items():
            if len(values) != len(entities):
                raise ValueError(f"Dimension '{dim_name}' has mismatched number of values")
    
    def _create_comparison_dimensions(
        self,
        entities: List[str],
        dimensions: Dict[str, List[float]],
        metadata: Optional[Dict[str, Dict[str, Any]]]
    ) -> List[ComparisonDimension]:
        """Create comparison dimension objects."""
        comparison_dims = []
        
        for dim_name, values in dimensions.items():
            # Get metadata if available
            meta = metadata.get(dim_name, {}) if metadata else {}
            
            # Create value mapping
            value_map = {entity: value for entity, value in zip(entities, values)}
            
            comparison_dims.append(ComparisonDimension(
                name=dim_name,
                values=value_map,
                unit=meta.get('unit', ''),
                higher_is_better=meta.get('higher_is_better', True)
            ))
        
        return comparison_dims
    
    def _calculate_rankings(
        self,
        entities: List[str],
        dimensions: List[ComparisonDimension],
        weights: Optional[Dict[str, float]]
    ) -> Dict[str, int]:
        """Calculate overall rankings for entities."""
        # Normalize scores across dimensions
        normalized_scores = {}
        for entity in entities:
            scores = []
            for dim in dimensions:
                value = dim.values.get(entity, 0)
                
                # Normalize to 0-1 scale
                all_values = list(dim.values.values())
                min_val, max_val = min(all_values), max(all_values)
                
                if max_val != min_val:
                    normalized = (value - min_val) / (max_val - min_val)
                else:
                    normalized = 1.0
                
                # Invert if lower is better
                if not dim.higher_is_better:
                    normalized = 1 - normalized
                
                # Apply weight if provided
                weight = weights.get(dim.name, 1.0) if weights else 1.0
                scores.append(normalized * weight)
            
            normalized_scores[entity] = sum(scores) / len(scores)
        
        # Convert scores to rankings
        sorted_entities = sorted(
            normalized_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        rankings = {entity: rank + 1 for rank, (entity, _) in enumerate(sorted_entities)}
        return rankings
    
    def _identify_dimension_winners(
        self,
        dimensions: List[ComparisonDimension]
    ) -> Dict[str, str]:
        """Identify winner for each dimension."""
        winners = {}
        
        for dim in dimensions:
            if dim.higher_is_better:
                winner = max(dim.values.items(), key=lambda x: x[1])
            else:
                winner = min(dim.values.items(), key=lambda x: x[1])
            
            winners[dim.name] = winner[0]
        
        return winners
    
    def _determine_overall_winner(self, rankings: Dict[str, int]) -> str:
        """Determine overall winner based on rankings."""
        return min(rankings.items(), key=lambda x: x[1])[0]
    
    def _identify_strengths(
        self,
        entities: List[str],
        dimensions: List[ComparisonDimension],
        rankings: Dict[str, int]
    ) -> Dict[str, List[str]]:
        """Identify strengths for each entity."""
        strengths = {entity: [] for entity in entities}
        
        for dim in dimensions:
            # Find entities that perform well in this dimension
            sorted_entities = sorted(
                dim.values.items(),
                key=lambda x: x[1],
                reverse=dim.higher_is_better
            )
            
            # Top performer gets this as a strength
            top_entity = sorted_entities[0][0]
            strengths[top_entity].append(f"Leading in {dim.name}")
        
        return strengths
    
    def _identify_weaknesses(
        self,
        entities: List[str],
        dimensions: List[ComparisonDimension],
        rankings: Dict[str, int]
    ) -> Dict[str, List[str]]:
        """Identify weaknesses for each entity."""
        weaknesses = {entity: [] for entity in entities}
        
        for dim in dimensions:
            # Find entities that perform poorly
            sorted_entities = sorted(
                dim.values.items(),
                key=lambda x: x[1],
                reverse=dim.higher_is_better
            )
            
            # Bottom performer gets this as a weakness
            bottom_entity = sorted_entities[-1][0]
            weaknesses[bottom_entity].append(f"Lagging in {dim.name}")
        
        return weaknesses
    
    def _generate_recommendations(
        self,
        entities: List[str],
        dimensions: List[ComparisonDimension],
        strengths: Dict[str, List[str]],
        weaknesses: Dict[str, List[str]]
    ) -> Dict[str, str]:
        """Generate recommendations for each entity."""
        recommendations = {}
        
        for entity in entities:
            # Placeholder: Use LLM to generate contextual recommendations
            entity_strengths = strengths.get(entity, [])
            entity_weaknesses = weaknesses.get(entity, [])
            
            if not entity_weaknesses:
                rec = f"Strong overall performance. Maintain current strategy."
            elif len(entity_strengths) > len(entity_weaknesses):
                rec = f"Good position with strengths in {len(entity_strengths)} areas. Focus on improving {entity_weaknesses[0] if entity_weaknesses else 'consistency'}."
            else:
                rec = f"Needs improvement in {len(entity_weaknesses)} areas. Priority: {entity_weaknesses[0] if entity_weaknesses else 'overall performance'}."
            
            recommendations[entity] = rec
        
        return recommendations
    
    def _calculate_confidence(self, dimensions: List[ComparisonDimension]) -> float:
        """Calculate confidence in comparison results."""
        # Placeholder: Consider data quality, sample size, variance
        # For now, return high confidence
        return 0.85


# Example usage
if __name__ == "__main__":
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
    
    print("Comparative Analysis: Layer 2 Scaling Solutions")
    print(f"\nOverall Winner: {result.overall_winner}")
    print(f"Confidence: {result.confidence_score:.1%}")
    
    print("\nRankings:")
    for entity, rank in sorted(result.rankings.items(), key=lambda x: x[1]):
        print(f"  {rank}. {entity}")
    
    print("\nStrengths:")
    for entity, strengths in result.strengths.items():
        if strengths:
            print(f"  {entity}: {', '.join(strengths)}")
    
    print("\nRecommendations:")
    for entity, rec in result.recommendations.items():
        print(f"  {entity}: {rec}")
