"""
Personalized Recommendations Agent

Suggests datasets, papers, and insights based on researchers' activities and interests.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict


@dataclass
class Recommendation:
    """Represents a personalized recommendation."""
    id: str
    type: str  # "dataset", "paper", "insight", "research"
    title: str
    description: str
    relevance_score: float
    reasons: List[str]
    url: Optional[str] = None
    metadata: Dict[str, Any] = None


@dataclass
class UserProfile:
    """User activity profile."""
    user_id: str
    interests: List[str]
    recent_activities: List[Dict[str, Any]]
    preference_vector: List[float]
    expertise_areas: List[str]


class RecommendationAgent:
    """
    Agent for generating personalized recommendations.
    
    Features:
    - User activity tracking and profiling
    - Collaborative filtering
    - Content-based recommendations
    - Trending topic identification
    - Cross-researcher learning
    
    Example:
        >>> agent = RecommendationAgent()
        >>> agent.track_activity("user_001", {"type": "view", "item": "DeFi research"})
        >>> recommendations = agent.get_recommendations("user_001", limit=5)
        >>> for rec in recommendations:
        ...     print(f"{rec.title} - Relevance: {rec.relevance_score:.2f}")
    """
    
    def __init__(self, llm_provider: str = "openai"):
        """
        Initialize Recommendation Agent.
        
        Args:
            llm_provider: LLM provider for content understanding
        """
        self.llm_provider = llm_provider
        self.user_profiles = {}
        self.content_database = []
        self.activity_log = defaultdict(list)
    
    def get_recommendations(
        self,
        user_id: str,
        limit: int = 10,
        min_score: float = 0.5
    ) -> List[Recommendation]:
        """
        Get personalized recommendations for a user.
        
        Args:
            user_id: User identifier
            limit: Maximum number of recommendations
            min_score: Minimum relevance score threshold
            
        Returns:
            List of personalized recommendations
        """
        # Get or create user profile
        profile = self._get_user_profile(user_id)
        
        # Generate recommendations from different sources
        content_based = self._content_based_recommendations(profile)
        collaborative = self._collaborative_recommendations(profile)
        trending = self._trending_recommendations()
        similar_users = self._similar_user_recommendations(profile)
        
        # Combine and rank recommendations
        all_recommendations = (
            content_based + collaborative + trending + similar_users
        )
        
        # Remove duplicates and filter by score
        unique_recs = self._deduplicate_recommendations(all_recommendations)
        filtered_recs = [r for r in unique_recs if r.relevance_score >= min_score]
        
        # Sort by relevance and return top N
        sorted_recs = sorted(
            filtered_recs,
            key=lambda x: x.relevance_score,
            reverse=True
        )
        
        return sorted_recs[:limit]
    
    def track_activity(self, user_id: str, activity: Dict[str, Any]) -> None:
        """
        Track user activity for building profile.
        
        Args:
            user_id: User identifier
            activity: Activity data (type, item, timestamp, etc.)
        """
        activity['timestamp'] = activity.get('timestamp', datetime.now())
        self.activity_log[user_id].append(activity)
        
        # Update user profile
        self._update_user_profile(user_id)
    
    def add_content(self, content: Dict[str, Any]) -> None:
        """
        Add content to recommendation database.
        
        Args:
            content: Content metadata (type, title, description, tags, etc.)
        """
        self.content_database.append(content)
    
    def _get_user_profile(self, user_id: str) -> UserProfile:
        """Get or create user profile."""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = UserProfile(
                user_id=user_id,
                interests=[],
                recent_activities=[],
                preference_vector=[],
                expertise_areas=[]
            )
        return self.user_profiles[user_id]
    
    def _update_user_profile(self, user_id: str) -> None:
        """Update user profile based on activities."""
        profile = self._get_user_profile(user_id)
        activities = self.activity_log[user_id]
        
        # Extract interests from recent activities
        profile.recent_activities = activities[-50:]  # Keep last 50
        profile.interests = self._extract_interests(activities)
        profile.preference_vector = self._build_preference_vector(activities)
        profile.expertise_areas = self._identify_expertise(activities)
    
    def _extract_interests(self, activities: List[Dict[str, Any]]) -> List[str]:
        """Extract interest topics from activities."""
        interests = []
        for activity in activities:
            if 'tags' in activity:
                interests.extend(activity['tags'])
            if 'category' in activity:
                interests.append(activity['category'])
        
        # Count frequency and return top interests
        from collections import Counter
        interest_counts = Counter(interests)
        return [interest for interest, _ in interest_counts.most_common(10)]
    
    def _build_preference_vector(self, activities: List[Dict[str, Any]]) -> List[float]:
        """Build user preference vector for similarity matching."""
        # Placeholder: Build embedding-based preference vector
        import numpy as np
        return np.random.rand(128).tolist()  # Simulated vector
    
    def _identify_expertise(self, activities: List[Dict[str, Any]]) -> List[str]:
        """Identify user's expertise areas."""
        # Analyze activities to identify expertise
        expertise = []
        
        # Activities with "create" or "publish" indicate expertise
        for activity in activities:
            if activity.get('type') in ['create', 'publish', 'review']:
                if 'category' in activity:
                    expertise.append(activity['category'])
        
        from collections import Counter
        expertise_counts = Counter(expertise)
        return [area for area, _ in expertise_counts.most_common(5)]
    
    def _content_based_recommendations(
        self,
        profile: UserProfile
    ) -> List[Recommendation]:
        """Generate content-based recommendations."""
        recommendations = []
        
        for content in self.content_database:
            score = self._calculate_content_similarity(profile, content)
            if score > 0.3:  # Threshold
                rec = Recommendation(
                    id=f"rec_{content.get('id', '')}_{datetime.now().timestamp()}",
                    type=content.get('type', 'content'),
                    title=content.get('title', ''),
                    description=content.get('description', ''),
                    relevance_score=score,
                    reasons=[
                        f"Matches your interest in {profile.interests[0] if profile.interests else 'research'}"
                    ],
                    url=content.get('url'),
                    metadata=content
                )
                recommendations.append(rec)
        
        return recommendations[:5]
    
    def _collaborative_recommendations(
        self,
        profile: UserProfile
    ) -> List[Recommendation]:
        """Generate collaborative filtering recommendations."""
        # Find similar users and recommend what they liked
        recommendations = []
        
        # Placeholder: Implement collaborative filtering
        # Using user-user or item-item similarity
        
        return recommendations
    
    def _trending_recommendations(self) -> List[Recommendation]:
        """Get trending content across all users."""
        recommendations = []
        
        # Analyze recent activity across all users
        all_activities = []
        for activities in self.activity_log.values():
            all_activities.extend(activities[-10:])  # Recent activities
        
        # Find trending items
        from collections import Counter
        trending_items = Counter(
            activity.get('item_id') for activity in all_activities
            if 'item_id' in activity
        )
        
        for item_id, count in trending_items.most_common(3):
            # Find content details
            content = self._find_content_by_id(item_id)
            if content:
                rec = Recommendation(
                    id=f"trending_{item_id}_{datetime.now().timestamp()}",
                    type=content.get('type', 'content'),
                    title=content.get('title', ''),
                    description=content.get('description', ''),
                    relevance_score=0.7,
                    reasons=[f"Trending - {count} recent views"],
                    url=content.get('url'),
                    metadata=content
                )
                recommendations.append(rec)
        
        return recommendations
    
    def _similar_user_recommendations(
        self,
        profile: UserProfile
    ) -> List[Recommendation]:
        """Recommendations based on similar users' activities."""
        recommendations = []
        
        # Find users with similar profiles
        similar_users = self._find_similar_users(profile)
        
        for similar_user_id in similar_users[:3]:
            # Get their recent activities
            similar_activities = self.activity_log[similar_user_id][-10:]
            
            for activity in similar_activities:
                if activity.get('type') == 'like' and 'item_id' in activity:
                    content = self._find_content_by_id(activity['item_id'])
                    if content:
                        rec = Recommendation(
                            id=f"similar_{activity['item_id']}_{datetime.now().timestamp()}",
                            type=content.get('type', 'content'),
                            title=content.get('title', ''),
                            description=content.get('description', ''),
                            relevance_score=0.6,
                            reasons=[f"Liked by similar researchers"],
                            url=content.get('url'),
                            metadata=content
                        )
                        recommendations.append(rec)
        
        return recommendations[:3]
    
    def _calculate_content_similarity(
        self,
        profile: UserProfile,
        content: Dict[str, Any]
    ) -> float:
        """Calculate similarity between user profile and content."""
        # Check interest overlap
        content_tags = content.get('tags', [])
        interest_overlap = len(set(profile.interests) & set(content_tags))
        
        # Normalize by number of interests
        if profile.interests:
            similarity = interest_overlap / len(profile.interests)
        else:
            similarity = 0.0
        
        return min(similarity, 1.0)
    
    def _find_similar_users(self, profile: UserProfile) -> List[str]:
        """Find users with similar profiles."""
        similar_users = []
        
        for user_id, other_profile in self.user_profiles.items():
            if user_id == profile.user_id:
                continue
            
            # Calculate similarity
            similarity = self._calculate_profile_similarity(profile, other_profile)
            if similarity > 0.5:  # Threshold
                similar_users.append(user_id)
        
        return similar_users
    
    def _calculate_profile_similarity(
        self,
        profile1: UserProfile,
        profile2: UserProfile
    ) -> float:
        """Calculate similarity between two user profiles."""
        # Interest overlap
        interests1 = set(profile1.interests)
        interests2 = set(profile2.interests)
        
        if not interests1 or not interests2:
            return 0.0
        
        overlap = len(interests1 & interests2)
        union = len(interests1 | interests2)
        
        return overlap / union if union > 0 else 0.0
    
    def _find_content_by_id(self, content_id: str) -> Optional[Dict[str, Any]]:
        """Find content by ID."""
        for content in self.content_database:
            if content.get('id') == content_id:
                return content
        return None
    
    def _deduplicate_recommendations(
        self,
        recommendations: List[Recommendation]
    ) -> List[Recommendation]:
        """Remove duplicate recommendations."""
        seen = set()
        unique = []
        
        for rec in recommendations:
            key = (rec.type, rec.title)
            if key not in seen:
                seen.add(key)
                unique.append(rec)
        
        return unique


# Example usage
if __name__ == "__main__":
    agent = RecommendationAgent()
    
    # Add sample content
    agent.add_content({
        'id': 'content_001',
        'type': 'research',
        'title': 'DeFi Protocol Analysis Q3 2023',
        'description': 'Comprehensive analysis of DeFi protocols',
        'tags': ['DeFi', 'analysis', 'Q3-2023'],
        'url': 'https://example.com/defi-analysis'
    })
    
    # Track user activities
    agent.track_activity('user_001', {
        'type': 'view',
        'item_id': 'content_001',
        'category': 'DeFi'
    })
    
    # Get recommendations
    recommendations = agent.get_recommendations('user_001', limit=5)
    
    print(f"Generated {len(recommendations)} recommendations:")
    for rec in recommendations:
        print(f"- {rec.title} (Score: {rec.relevance_score:.2f})")
        print(f"  Reason: {rec.reasons[0]}")
