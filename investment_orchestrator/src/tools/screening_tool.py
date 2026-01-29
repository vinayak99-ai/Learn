"""Screening tool for enriched asset search with full data.

This tool combines basket search with detailed data fetching to provide
comprehensive screening results.
"""

import logging
from typing import Optional
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from ..api_client import api_client, APIClientError

logger = logging.getLogger(__name__)


class ScreeningInput(BaseModel):
    """Input schema for the ScreenAssets tool."""
    sector: Optional[str] = Field(
        default=None,
        description="Filter by sector (e.g., 'Technology', 'Healthcare')"
    )
    market_cap: Optional[str] = Field(
        default=None,
        description="Filter by market cap (e.g., 'Large', 'Mid', 'Small')"
    )
    price_range: Optional[str] = Field(
        default=None,
        description="Filter by price range (e.g., '<100', '50-200')"
    )
    min_growth: Optional[float] = Field(
        default=None,
        description="Minimum revenue growth rate"
    )
    max_pe_ratio: Optional[float] = Field(
        default=None,
        description="Maximum P/E ratio"
    )
    min_analyst_rating: Optional[str] = Field(
        default=None,
        description="Minimum analyst rating (e.g., 'Buy', 'Strong Buy')"
    )
    limit: int = Field(
        default=10,
        description="Maximum number of results to return (default 10)"
    )


async def screen_assets_impl(
    sector: Optional[str] = None,
    market_cap: Optional[str] = None,
    price_range: Optional[str] = None,
    min_growth: Optional[float] = None,
    max_pe_ratio: Optional[float] = None,
    min_analyst_rating: Optional[str] = None,
    limit: int = 10
) -> str:
    """
    Screen assets with criteria and return enriched results.
    
    This tool first finds matching assets using criteria, then fetches
    full data for each to provide comprehensive screening results.
    
    Args:
        sector: Sector filter
        market_cap: Market cap filter
        price_range: Price range filter
        min_growth: Minimum growth filter
        max_pe_ratio: Maximum P/E ratio filter
        min_analyst_rating: Minimum rating filter
        limit: Maximum results to return
        
    Returns:
        Formatted screening results with full asset data
    """
    try:
        # Build criteria for initial basket search
        criteria = {}
        if sector:
            criteria["sector"] = sector
        if market_cap:
            criteria["marketCap"] = market_cap
        if price_range:
            criteria["priceRange"] = price_range
        if min_growth is not None:
            criteria["minGrowth"] = min_growth
        
        logger.info(f"Screening assets with criteria: {criteria}")
        
        # Get matching asset IDs
        asset_ids = await api_client.get_asset_baskets(criteria)
        
        if not asset_ids:
            return "No assets found matching the screening criteria."
        
        # Limit results
        asset_ids = asset_ids[:limit]
        
        logger.info(f"Fetching detailed data for {len(asset_ids)} assets")
        
        # Fetch detailed data for all matching assets in parallel
        prices = await api_client.batch_fetch(asset_ids, "get_asset_price")
        classifications = await api_client.batch_fetch(asset_ids, "get_asset_classification")
        research_data = await api_client.batch_fetch(asset_ids, "get_asset_research_data")
        
        # Build results with filtering
        results = []
        for asset_id in asset_ids:
            price = prices.get(asset_id, {})
            classification = classifications.get(asset_id, {})
            research = research_data.get(asset_id, {})
            
            # Apply additional filters
            if max_pe_ratio is not None:
                pe = research.get('peRatio')
                if pe and pe > max_pe_ratio:
                    continue
            
            if min_analyst_rating:
                rating = research.get('consensusRating', '')
                if rating and rating not in ['Strong Buy', 'Buy'] and min_analyst_rating in ['Strong Buy', 'Buy']:
                    continue
            
            # Build result entry
            entry = {
                'asset_id': asset_id,
                'price': price.get('currentPrice', 'N/A'),
                'change': price.get('changePercent', 'N/A'),
                'sector': classification.get('sector', 'N/A'),
                'market_cap': classification.get('marketCap', 'N/A'),
                'pe_ratio': research.get('peRatio', 'N/A'),
                'growth': research.get('revenueGrowth', 'N/A'),
                'rating': research.get('consensusRating', 'N/A'),
                'target': research.get('targetPrice', 'N/A')
            }
            results.append(entry)
        
        if not results:
            return "No assets passed the additional screening filters."
        
        # Format output
        output = f"Screening Results ({len(results)} assets found):\n"
        output += f"Criteria: {criteria}\n"
        output += "=" * 100 + "\n\n"
        
        for i, entry in enumerate(results, 1):
            output += f"{i}. {entry['asset_id']}\n"
            output += f"   Price: ${entry['price']} ({entry['change']}%)\n"
            output += f"   Sector: {entry['sector']} | Market Cap: {entry['market_cap']}\n"
            output += f"   P/E: {entry['pe_ratio']} | Growth: {entry['growth']}%\n"
            output += f"   Rating: {entry['rating']} | Target: ${entry['target']}\n\n"
        
        return output
        
    except Exception as e:
        logger.error(f"Error screening assets: {e}")
        return f"Error screening assets: {str(e)}"


# Create the LangChain StructuredTool
screen_assets_tool = StructuredTool.from_function(
    coroutine=screen_assets_impl,
    name="ScreenAssets",
    description="""Perform comprehensive asset screening with multiple criteria and get enriched
    results including price, fundamentals, and analyst ratings. Use this for complex queries
    like 'find tech stocks under $100 with high growth and good ratings'. This tool combines
    filtering with detailed data fetching.""",
    args_schema=ScreeningInput,
)
