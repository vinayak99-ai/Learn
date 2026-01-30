"""
Contextual Alerts with Suggested Actions Agent

Provides alerts with context, explanations, and actionable recommendations.
Moves beyond simple anomaly detection to proactive guidance.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AlertPriority(Enum):
    """Alert priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AlertStatus(Enum):
    """Alert status."""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


@dataclass
class SuggestedAction:
    """Represents a suggested action for an alert."""
    action: str
    impact_level: str  # "high", "medium", "low"
    effort_required: str  # "low", "medium", "high"
    expected_outcome: str
    confidence: float


@dataclass
class Alert:
    """Represents a contextual alert."""
    id: str
    title: str
    description: str
    priority: AlertPriority
    status: AlertStatus
    context: Dict[str, Any]
    root_causes: List[str]
    impact_assessment: str
    suggested_actions: List[SuggestedAction]
    confidence: float
    created_at: datetime
    metadata: Dict[str, Any]


class AlertAgent:
    """
    Agent for generating contextual alerts with suggested actions.
    
    Features:
    - Multi-dimensional anomaly detection
    - Root cause analysis
    - Impact assessment
    - Action recommendation generation
    - Priority and urgency scoring
    
    Example:
        >>> agent = AlertAgent()
        >>> alert = agent.create_alert(
        ...     anomaly_data={"metric": "EU_demand", "change": -15},
        ...     context={"region": "EU", "timeframe": "week"}
        ... )
        >>> print(f"{alert.title} - Priority: {alert.priority.value}")
        >>> for action in alert.suggested_actions:
        ...     print(f"  Action: {action.action}")
    """
    
    def __init__(self, llm_provider: str = "openai"):
        """
        Initialize Alert Agent.
        
        Args:
            llm_provider: LLM provider for explanation generation
        """
        self.llm_provider = llm_provider
        self.active_alerts = []
        self.alert_history = []
    
    def create_alert(
        self,
        anomaly_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Alert:
        """
        Create a contextual alert from anomaly data.
        
        Args:
            anomaly_data: Detected anomaly information
            context: Additional context for the alert
            
        Returns:
            Contextual alert with suggested actions
        """
        # Generate alert title and description
        title = self._generate_alert_title(anomaly_data)
        description = self._generate_alert_description(anomaly_data, context)
        
        # Analyze root causes
        root_causes = self._identify_root_causes(anomaly_data, context)
        
        # Assess impact
        impact_assessment = self._assess_impact(anomaly_data, context)
        
        # Determine priority
        priority = self._determine_priority(anomaly_data, impact_assessment)
        
        # Generate suggested actions
        suggested_actions = self._generate_suggested_actions(
            anomaly_data, root_causes, impact_assessment
        )
        
        # Calculate confidence
        confidence = self._calculate_confidence(anomaly_data, root_causes)
        
        alert = Alert(
            id=f"alert_{datetime.now().timestamp()}",
            title=title,
            description=description,
            priority=priority,
            status=AlertStatus.ACTIVE,
            context=context,
            root_causes=root_causes,
            impact_assessment=impact_assessment,
            suggested_actions=suggested_actions,
            confidence=confidence,
            created_at=datetime.now(),
            metadata=anomaly_data
        )
        
        self.active_alerts.append(alert)
        return alert
    
    def get_active_alerts(
        self,
        priority_filter: Optional[AlertPriority] = None
    ) -> List[Alert]:
        """
        Get all active alerts, optionally filtered by priority.
        
        Args:
            priority_filter: Filter by priority level
            
        Returns:
            List of active alerts
        """
        alerts = [a for a in self.active_alerts if a.status == AlertStatus.ACTIVE]
        
        if priority_filter:
            alerts = [a for a in alerts if a.priority == priority_filter]
        
        return sorted(alerts, key=lambda x: self._priority_score(x.priority), reverse=True)
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Mark alert as acknowledged."""
        for alert in self.active_alerts:
            if alert.id == alert_id:
                alert.status = AlertStatus.ACKNOWLEDGED
                return True
        return False
    
    def resolve_alert(self, alert_id: str, resolution_notes: str = "") -> bool:
        """Mark alert as resolved."""
        for alert in self.active_alerts:
            if alert.id == alert_id:
                alert.status = AlertStatus.RESOLVED
                alert.metadata['resolution_notes'] = resolution_notes
                alert.metadata['resolved_at'] = datetime.now()
                self.alert_history.append(alert)
                self.active_alerts.remove(alert)
                return True
        return False
    
    def _generate_alert_title(self, anomaly_data: Dict[str, Any]) -> str:
        """Generate alert title."""
        metric = anomaly_data.get('metric', 'Unknown metric')
        change = anomaly_data.get('change', 0)
        
        if change < 0:
            return f"Declining {metric} detected ({change}%)"
        else:
            return f"Spike in {metric} detected (+{change}%)"
    
    def _generate_alert_description(
        self,
        anomaly_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Generate detailed alert description using LLM."""
        # Placeholder: Use LLM to generate contextual description
        metric = anomaly_data.get('metric', 'metric')
        change = anomaly_data.get('change', 0)
        region = context.get('region', 'Unknown region')
        timeframe = context.get('timeframe', 'recent period')
        
        return (
            f"{metric} has changed by {change}% in {region} over the {timeframe}. "
            f"This represents a significant deviation from normal patterns."
        )
    
    def _identify_root_causes(
        self,
        anomaly_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> List[str]:
        """Identify potential root causes for the anomaly."""
        root_causes = []
        
        # Analyze context and data to identify causes
        # Placeholder: Use LLM and rule-based analysis
        
        if 'region' in context and context['region'] == 'EU':
            root_causes.append("Regulatory uncertainty in EU markets")
            root_causes.append("Economic conditions affecting consumer behavior")
        
        if anomaly_data.get('change', 0) < -10:
            root_causes.append("Market sentiment shift")
        
        return root_causes
    
    def _assess_impact(
        self,
        anomaly_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Assess the impact of the anomaly."""
        change_magnitude = abs(anomaly_data.get('change', 0))
        
        if change_magnitude > 20:
            severity = "High"
        elif change_magnitude > 10:
            severity = "Medium"
        else:
            severity = "Low"
        
        # Calculate affected portfolio percentage (placeholder)
        affected_pct = 22
        
        return f"{severity} - affects {affected_pct}% of portfolio allocation"
    
    def _determine_priority(
        self,
        anomaly_data: Dict[str, Any],
        impact_assessment: str
    ) -> AlertPriority:
        """Determine alert priority."""
        change_magnitude = abs(anomaly_data.get('change', 0))
        
        if change_magnitude > 20 or "High" in impact_assessment:
            return AlertPriority.CRITICAL
        elif change_magnitude > 10 or "Medium" in impact_assessment:
            return AlertPriority.HIGH
        elif change_magnitude > 5:
            return AlertPriority.MEDIUM
        else:
            return AlertPriority.LOW
    
    def _generate_suggested_actions(
        self,
        anomaly_data: Dict[str, Any],
        root_causes: List[str],
        impact_assessment: str
    ) -> List[SuggestedAction]:
        """Generate actionable recommendations."""
        actions = []
        
        # Placeholder: Use LLM to generate contextual actions
        metric = anomaly_data.get('metric', '')
        change = anomaly_data.get('change', 0)
        
        if change < 0 and 'demand' in metric.lower():
            actions.append(SuggestedAction(
                action="Increase ad spend in APAC to counter declining EU demand",
                impact_level="high",
                effort_required="medium",
                expected_outcome="Compensate for EU losses with APAC growth",
                confidence=0.85
            ))
            
            actions.append(SuggestedAction(
                action="Diversify EU holdings to less regulated assets",
                impact_level="medium",
                effort_required="high",
                expected_outcome="Reduce regulatory risk exposure",
                confidence=0.75
            ))
            
            actions.append(SuggestedAction(
                action="Monitor regulatory developments closely",
                impact_level="low",
                effort_required="low",
                expected_outcome="Early warning for further deterioration",
                confidence=0.90
            ))
        
        return actions
    
    def _calculate_confidence(
        self,
        anomaly_data: Dict[str, Any],
        root_causes: List[str]
    ) -> float:
        """Calculate confidence in the alert."""
        # Base confidence on data quality and root cause identification
        base_confidence = 0.7
        
        # Increase confidence if we identified root causes
        if root_causes:
            base_confidence += 0.15
        
        # Adjust based on data quality (placeholder)
        data_quality = anomaly_data.get('data_quality', 1.0)
        
        return min(base_confidence * data_quality, 1.0)
    
    def _priority_score(self, priority: AlertPriority) -> int:
        """Convert priority to numeric score for sorting."""
        priority_map = {
            AlertPriority.CRITICAL: 5,
            AlertPriority.HIGH: 4,
            AlertPriority.MEDIUM: 3,
            AlertPriority.LOW: 2,
            AlertPriority.INFO: 1
        }
        return priority_map.get(priority, 0)
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get summary of all alerts."""
        return {
            'total_active': len([a for a in self.active_alerts if a.status == AlertStatus.ACTIVE]),
            'by_priority': {
                'critical': len([a for a in self.active_alerts if a.priority == AlertPriority.CRITICAL]),
                'high': len([a for a in self.active_alerts if a.priority == AlertPriority.HIGH]),
                'medium': len([a for a in self.active_alerts if a.priority == AlertPriority.MEDIUM]),
                'low': len([a for a in self.active_alerts if a.priority == AlertPriority.LOW])
            },
            'total_resolved': len(self.alert_history)
        }


# Example usage
if __name__ == "__main__":
    agent = AlertAgent()
    
    # Create alert from anomaly
    alert = agent.create_alert(
        anomaly_data={
            'metric': 'EU_demand',
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
    
    print(f"Alert: {alert.title}")
    print(f"Priority: {alert.priority.value}")
    print(f"Impact: {alert.impact_assessment}")
    print(f"\nRoot Causes:")
    for cause in alert.root_causes:
        print(f"  - {cause}")
    print(f"\nSuggested Actions:")
    for action in alert.suggested_actions:
        print(f"  - {action.action} (Impact: {action.impact_level}, Confidence: {action.confidence})")
