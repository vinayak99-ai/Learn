"""Classification tool for fetching asset sector and industry information.

This tool retrieves classification data including sector, industry,
market cap, and other categorization details.
"""

import logging
from typing import Dict
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from ..api_client import api_client, APIClientError

logger = logging.getLogger(__name__)


class ClassificationInput(BaseModel):
    """Input schema for the GetAssetClassification tool."""
    asset_id: str = Field(
        description="The asset identifier (e.g., 'AAPL' for Apple, 'GOOGL' for Google)"
    )


async def get_asset_classification_impl(asset_id: str) -> str:
    """
    Fetch classification data for an asset.
    
    Args:
        asset_id: Asset identifier
        
    Returns:
        Formatted string with classification information
    """
    try:
        logger.info(f"Fetching classification for asset: {asset_id}")
        data = await api_client.get_asset_classification(asset_id)
        
        # Format the response
        result = f"""Asset Classification for {asset_id}:
- Sector: {data.get('sector', 'N/A')}
- Industry: {data.get('industry', 'N/A')}
- Market Cap: ${data.get('marketCap', 'N/A')}
- Geography: {data.get('geography', 'N/A')}
- Asset Type: {data.get('assetType', 'N/A')}"""
        
        return result
        
    except APIClientError as e:
        logger.error(f"Error fetching classification for {asset_id}: {e}")
        return f"Error fetching classification data for {asset_id}: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error in get_asset_classification: {e}")
        return f"Unexpected error: {str(e)}"


# Create the LangChain StructuredTool
get_asset_classification_tool = StructuredTool.from_function(
    coroutine=get_asset_classification_impl,
    name="GetAssetClassification",
    description="""Get the classification information for an asset including sector, industry,
    market capitalization, geography, and asset type. Use this when you need to understand
    what category an asset belongs to or want to know its business sector.""",
    args_schema=ClassificationInput,
)
