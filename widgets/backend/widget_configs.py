"""
Widget Configurations
Sample widget configurations demonstrating different widget types
"""

from typing import List, Dict, Any, Optional

# Sample widget configurations
WIDGET_CONFIGS = [
    {
        "id": "sales-chart",
        "name": "Monthly Sales",
        "type": "chart",
        "description": "Monthly sales data visualization",
        "pythonCode": """
# Fetch sales data
data = fetch_sales_data()

# Process for chart format
chart_data = [
    {"label": item["month"], "value": item["sales"]}
    for item in data
]

result = {
    "data": chart_data,
    "metadata": {
        "title": "Sales by Month",
        "subtitle": "North Region"
    }
}
""",
        "parameters": {},
        "refreshInterval": 60  # Auto-refresh every 60 seconds
    },
    {
        "id": "user-metrics",
        "name": "User Metrics",
        "type": "metric",
        "description": "Key user engagement metrics",
        "pythonCode": """
# Fetch user metrics
metrics_data = fetch_user_metrics()

# Format for metric widget
result = {
    "metrics": [
        {
            "label": "Active Users",
            "value": metrics_data["active_users"],
            "icon": "👥",
            "change": 12.5,
            "description": "Total active users"
        },
        {
            "label": "New Users",
            "value": metrics_data["new_users"],
            "icon": "✨",
            "change": 8.3,
            "description": "New sign-ups this month"
        },
        {
            "label": "Churn Rate",
            "value": str(metrics_data["churn_rate"]) + "%",
            "icon": "📉",
            "change": -2.1,
            "description": "User churn rate"
        },
        {
            "label": "Avg. Session",
            "value": str(metrics_data["avg_session_duration"]) + "m",
            "icon": "⏱️",
            "change": 5.7,
            "description": "Average session duration"
        }
    ]
}
""",
        "parameters": {},
        "refreshInterval": 120
    },
    {
        "id": "product-table",
        "name": "Product Performance",
        "type": "table",
        "description": "Product sales and revenue data",
        "pythonCode": """
# Fetch table data
data = fetch_table_data()

# Format for table widget
result = {
    "data": data,
    "columns": ["product", "quantity", "revenue"]
}
""",
        "parameters": {},
        "refreshInterval": 90
    },
    {
        "id": "custom-report",
        "name": "Custom Analytics",
        "type": "custom",
        "description": "Custom data analysis results",
        "pythonCode": """
# Custom analysis
sales = fetch_sales_data()
total_sales = sum(item["sales"] for item in sales)
avg_sales = total_sales / len(sales)

result = {
    "total_sales": total_sales,
    "average_sales": avg_sales,
    "num_months": len(sales),
    "analysis": "Sales trend is positive"
}
""",
        "parameters": {},
        "refreshInterval": None
    },
    {
        "id": "revenue-chart",
        "name": "Revenue Overview",
        "type": "chart",
        "description": "Product revenue comparison",
        "pythonCode": """
# Fetch and process revenue data
products = fetch_table_data()

result = [
    {"label": item["product"], "value": item["revenue"]}
    for item in products
]
""",
        "parameters": {}
    }
]

def get_widget_configs() -> List[Dict[str, Any]]:
    """
    Get all widget configurations
    """
    return WIDGET_CONFIGS

def get_widget_by_id(widget_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a specific widget configuration by ID
    """
    for config in WIDGET_CONFIGS:
        if config["id"] == widget_id:
            return config
    return None

def add_widget_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a new widget configuration
    In production, this would persist to a database
    """
    WIDGET_CONFIGS.append(config)
    return config

def update_widget_config(widget_id: str, config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Update an existing widget configuration
    In production, this would update the database
    """
    for i, existing_config in enumerate(WIDGET_CONFIGS):
        if existing_config["id"] == widget_id:
            WIDGET_CONFIGS[i] = {**existing_config, **config}
            return WIDGET_CONFIGS[i]
    return None

def delete_widget_config(widget_id: str) -> bool:
    """
    Delete a widget configuration
    In production, this would delete from database
    """
    for i, config in enumerate(WIDGET_CONFIGS):
        if config["id"] == widget_id:
            WIDGET_CONFIGS.pop(i)
            return True
    return False
