"""Price tool for fetching current asset price data.

This tool retrieves real-time or latest available price information
for a given asset from the Java backend API.
"""

import logging
from typing import Dict
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from ..api_client import api_client, APIClientError

logger = logging.getLogger(__name__)


class PriceInput(BaseModel):
    """Input schema for the GetAssetPrice tool."""
    asset_id: str = Field(
        description="The asset identifier (e.g., 'AAPL' for Apple, 'TSLA' for Tesla)"
    )


async def get_asset_price_impl(asset_id: str) -> str:
    """
    Fetch current price data for an asset.
    
    Args:
        asset_id: Asset identifier
        
    Returns:
        Formatted string with price information
    """
    try:
        logger.info(f"Fetching price for asset: {asset_id}")
        data = await api_client.get_asset_price(asset_id)
        
        # Format the response
        result = f"""Asset Price Information for {asset_id}:
- Current Price: ${data.get('currentPrice', 'N/A')}
- Previous Close: ${data.get('previousClose', 'N/A')}
- Change: {data.get('changePercent', 'N/A')}%
- Volume: {data.get('volume', 'N/A'):,}
- Last Updated: {data.get('lastUpdated', 'N/A')}"""
        
        return result
        
    except APIClientError as e:
        logger.error(f"Error fetching price for {asset_id}: {e}")
        return f"Error fetching price data for {asset_id}: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error in get_asset_price: {e}")
        return f"Unexpected error: {str(e)}"


# Create the LangChain StructuredTool
get_asset_price_tool = StructuredTool.from_function(
    coroutine=get_asset_price_impl,
    name="GetAssetPrice",
    description="""Fetch the current price information for a specific asset.
    Use this when you need to know the current trading price, price changes,
    or trading volume of an asset. Provide the asset ticker symbol (e.g., 'AAPL', 'TSLA').""",
    args_schema=PriceInput,
)
