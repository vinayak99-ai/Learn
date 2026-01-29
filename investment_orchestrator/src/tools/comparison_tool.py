"""Comparison tool for side-by-side asset comparison.

This tool compares multiple assets across various metrics including
price, classification, and research data.
"""

import logging
from typing import List
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from ..api_client import api_client, APIClientError

logger = logging.getLogger(__name__)


class ComparisonInput(BaseModel):
    """Input schema for the CompareAssets tool."""
    asset_ids: List[str] = Field(
        description="List of asset identifiers to compare (e.g., ['AAPL', 'MSFT', 'GOOGL'])"
    )


async def compare_assets_impl(asset_ids: List[str]) -> str:
    """
    Compare multiple assets side-by-side.
    
    Args:
        asset_ids: List of asset identifiers to compare
        
    Returns:
        Formatted comparison table
    """
    try:
        if not asset_ids or len(asset_ids) < 2:
            return "Please provide at least 2 assets to compare."
        
        if len(asset_ids) > 5:
            return "Please limit comparisons to 5 assets at a time for clarity."
        
        logger.info(f"Comparing assets: {asset_ids}")
        
        # Fetch data for all assets in parallel
        prices = await api_client.batch_fetch(asset_ids, "get_asset_price")
        classifications = await api_client.batch_fetch(asset_ids, "get_asset_classification")
        research_data = await api_client.batch_fetch(asset_ids, "get_asset_research_data")
        
        # Build comparison table
        result = f"Comparison of {len(asset_ids)} Assets:\n"
        result += "=" * 80 + "\n\n"
        
        for asset_id in asset_ids:
            result += f"{asset_id}:\n"
            
            # Price data
            price = prices.get(asset_id, {})
            if "error" not in price:
                result += f"  Price: ${price.get('currentPrice', 'N/A')}"
                result += f" ({price.get('changePercent', 'N/A')}%)\n"
            
            # Classification
            classification = classifications.get(asset_id, {})
            if "error" not in classification:
                result += f"  Sector: {classification.get('sector', 'N/A')}\n"
                result += f"  Market Cap: {classification.get('marketCap', 'N/A')}\n"
            
            # Research data
            research = research_data.get(asset_id, {})
            if "error" not in research:
                result += f"  P/E Ratio: {research.get('peRatio', 'N/A')}\n"
                result += f"  Revenue Growth: {research.get('revenueGrowth', 'N/A')}%\n"
                result += f"  Analyst Rating: {research.get('consensusRating', 'N/A')}\n"
                result += f"  Target Price: ${research.get('targetPrice', 'N/A')}\n"
            
            result += "\n"
        
        result += "=" * 80
        
        return result
        
    except Exception as e:
        logger.error(f"Error comparing assets: {e}")
        return f"Error comparing assets: {str(e)}"


# Create the LangChain StructuredTool
compare_assets_tool = StructuredTool.from_function(
    coroutine=compare_assets_impl,
    name="CompareAssets",
    description="""Compare multiple assets side-by-side across price, classification, and
    research metrics. Use this when you need to evaluate multiple investment options against
    each other or help decide between different assets. Provide 2-5 asset ticker symbols.""",
    args_schema=ComparisonInput,
)
