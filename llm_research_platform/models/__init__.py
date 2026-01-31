"""
Data models for LLM Research Platform.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum


class Priority(Enum):
    """Priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Status(Enum):
    """Status values."""
    ACTIVE = "active"
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Document:
    """Generic document model."""
    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]
    tags: List[str]


@dataclass
class ResearchReport:
    """Research report model."""
    id: str
    title: str
    content: str
    report_type: str  # "daily_brief", "weekly_snapshot", "monthly_wrap"
    author: str
    created_at: datetime
    published_at: Optional[datetime]
    status: Status
    metadata: Dict[str, Any]


@dataclass
class DataSource:
    """Data source model."""
    id: str
    name: str
    type: str  # "api", "database", "file"
    connection_params: Dict[str, Any]
    last_sync: Optional[datetime]
    is_active: bool


@dataclass
class Metric:
    """Metric data model."""
    name: str
    value: float
    unit: str
    timestamp: datetime
    entity: str  # What the metric is about (e.g., "Ethereum", "DeFi")
    source: str
    metadata: Dict[str, Any]


@dataclass
class TimeSeriesData:
    """Time series data model."""
    metric_name: str
    timestamps: List[datetime]
    values: List[float]
    entity: str
    source: str


@dataclass
class UserActivity:
    """User activity model."""
    user_id: str
    activity_type: str  # "view", "create", "edit", "delete", "search"
    resource_id: str
    resource_type: str
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass
class Notification:
    """Notification model."""
    id: str
    user_id: str
    title: str
    message: str
    priority: Priority
    created_at: datetime
    read_at: Optional[datetime]
    action_url: Optional[str]


@dataclass
class APIResponse:
    """Standard API response model."""
    success: bool
    data: Optional[Any]
    error: Optional[str]
    timestamp: datetime
    metadata: Dict[str, Any]


__all__ = [
    "Priority",
    "Status",
    "Document",
    "ResearchReport",
    "DataSource",
    "Metric",
    "TimeSeriesData",
    "UserActivity",
    "Notification",
    "APIResponse"
]
