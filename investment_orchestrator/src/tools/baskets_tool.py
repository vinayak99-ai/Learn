"""Baskets tool for finding assets matching specific criteria.

This tool searches for assets based on various filters like sector,
market cap, price range, and other criteria.
"""

import logging
from typing import Dict, Optional
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from ..api_client import api_client, APIClientError

logger = logging.getLogger(__name__)


class BasketsInput(BaseModel):
    """Input schema for the GetAssetBaskets tool."""
    sector: Optional[str] = Field(
        default=None,
        description="Filter by sector (e.g., 'Technology', 'Healthcare', 'Finance')"
    )
    industry: Optional[str] = Field(
        default=None,
        description="Filter by industry (e.g., 'Software', 'Biotechnology')"
    )
    market_cap: Optional[str] = Field(
        default=None,
        description="Filter by market cap (e.g., 'Large', 'Mid', 'Small')"
    )
    price_range: Optional[str] = Field(
        default=None,
        description="Filter by price range (e.g., '<100', '50-200', '>500')"
    )
    min_growth: Optional[float] = Field(
        default=None,
        description="Minimum revenue growth rate (as percentage)"
    )


async def get_asset_baskets_impl(
    sector: Optional[str] = None,
    industry: Optional[str] = None,
    market_cap: Optional[str] = None,
    price_range: Optional[str] = None,
    min_growth: Optional[float] = None
) -> str:
    """
    Find assets matching the specified criteria.
    
    Args:
        sector: Business sector filter
        industry: Industry filter
        market_cap: Market cap category filter
        price_range: Price range filter
        min_growth: Minimum growth rate filter
        
    Returns:
        Formatted string with matching asset IDs
    """
    try:
        # Build criteria dictionary
        criteria = {}
        if sector:
            criteria["sector"] = sector
        if industry:
            criteria["industry"] = industry
        if market_cap:
            criteria["marketCap"] = market_cap
        if price_range:
            criteria["priceRange"] = price_range
        if min_growth is not None:
            criteria["minGrowth"] = min_growth
        
        logger.info(f"Searching assets with criteria: {criteria}")
        asset_ids = await api_client.get_asset_baskets(criteria)
        
        if not asset_ids:
            return "No assets found matching the specified criteria."
        
        # Format the response
        result = f"Found {len(asset_ids)} assets matching criteria:\n"
        result += f"Criteria: {criteria}\n\n"
        result += "Matching Assets:\n"
        result += "\n".join(f"- {asset_id}" for asset_id in asset_ids[:20])
        
        if len(asset_ids) > 20:
            result += f"\n... and {len(asset_ids) - 20} more"
        
        return result
        
    except APIClientError as e:
        logger.error(f"Error fetching asset baskets: {e}")
        return f"Error fetching asset baskets: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error in get_asset_baskets: {e}")
        return f"Unexpected error: {str(e)}"


# Create the LangChain StructuredTool
get_asset_baskets_tool = StructuredTool.from_function(
    coroutine=get_asset_baskets_impl,
    name="GetAssetBaskets",
    description="""Find assets that match specific criteria such as sector, industry, market cap,
    price range, or minimum growth rate. Use this when you need to screen for assets meeting
    certain conditions or build a list of candidates for further analysis.""",
    args_schema=BasketsInput,
)
