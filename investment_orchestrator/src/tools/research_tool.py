"""Research tool for fetching fundamental and analyst data.

This tool retrieves detailed research data including fundamentals,
analyst ratings, target prices, and risk factors.
"""

import logging
from typing import Dict
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from ..api_client import api_client, APIClientError

logger = logging.getLogger(__name__)


class ResearchInput(BaseModel):
    """Input schema for the GetAssetResearchData tool."""
    asset_id: str = Field(
        description="The asset identifier (e.g., 'NVDA' for Nvidia, 'MSFT' for Microsoft)"
    )


async def get_asset_research_data_impl(asset_id: str) -> str:
    """
    Fetch research and fundamental data for an asset.
    
    Args:
        asset_id: Asset identifier
        
    Returns:
        Formatted string with research information
    """
    try:
        logger.info(f"Fetching research data for asset: {asset_id}")
        data = await api_client.get_asset_research_data(asset_id)
        
        # Format the response
        result = f"""Research Data for {asset_id}:

Fundamentals:
- P/E Ratio: {data.get('peRatio', 'N/A')}
- Revenue Growth: {data.get('revenueGrowth', 'N/A')}%
- Profit Margin: {data.get('profitMargin', 'N/A')}%

Analyst Coverage:
- Consensus Rating: {data.get('consensusRating', 'N/A')}
- Analyst Count: {data.get('analystCount', 'N/A')}
- Target Price: ${data.get('targetPrice', 'N/A')}

Risk Factors:"""
        
        risk_factors = data.get('riskFactors', [])
        if risk_factors:
            for risk in risk_factors:
                result += f"\n- {risk}"
        else:
            result += "\n- No specific risk factors identified"
        
        return result
        
    except APIClientError as e:
        logger.error(f"Error fetching research data for {asset_id}: {e}")
        return f"Error fetching research data for {asset_id}: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error in get_asset_research_data: {e}")
        return f"Unexpected error: {str(e)}"


# Create the LangChain StructuredTool
get_asset_research_data_tool = StructuredTool.from_function(
    coroutine=get_asset_research_data_impl,
    name="GetAssetResearchData",
    description="""Get detailed research data including fundamentals (P/E ratio, revenue growth,
    profit margin), analyst ratings (consensus, target price), and identified risk factors.
    Use this when you need deep analysis of an asset's financial health and analyst sentiment.""",
    args_schema=ResearchInput,
)
