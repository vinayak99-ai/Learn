"""Async HTTP client for Java backend APIs.

This module provides an asynchronous HTTP client with connection pooling,
error handling, retry logic, and request/response logging for communicating
with the Java backend investment data APIs.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import httpx
from .config import config

logger = logging.getLogger(__name__)


class APIClientError(Exception):
    """Base exception for API client errors."""
    pass


class APIClient:
    """Async HTTP client for Java backend APIs with caching and error handling."""
    
    def __init__(self):
        """Initialize the API client with connection pooling."""
        self.base_url = config.get_base_api_url()
        self.timeout = config.REQUEST_TIMEOUT_SECONDS
        self.max_concurrent = config.MAX_CONCURRENT_REQUESTS
        
        # Initialize httpx async client with connection pooling
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(self.timeout),
            limits=httpx.Limits(max_connections=self.max_concurrent, max_keepalive_connections=10)
        )
        
        # Simple in-memory cache with TTL
        self._cache: Dict[str, tuple[Any, datetime]] = {}
        self._cache_duration = timedelta(minutes=config.CACHE_DURATION_MINUTES)
        
        # Semaphore for rate limiting
        self._semaphore = asyncio.Semaphore(self.max_concurrent)
        
        logger.info(f"API Client initialized with base URL: {self.base_url}")
    
    async def close(self):
        """Close the HTTP client and clean up resources."""
        await self.client.aclose()
        logger.info("API Client closed")
    
    def _get_cache_key(self, endpoint: str, params: Dict) -> str:
        """Generate a cache key from endpoint and parameters."""
        import json
        params_str = json.dumps(params, sort_keys=True)
        return f"{endpoint}:{params_str}"
    
    def _get_from_cache(self, cache_key: str) -> Optional[Any]:
        """Retrieve data from cache if not expired."""
        if cache_key in self._cache:
            data, timestamp = self._cache[cache_key]
            if datetime.now() - timestamp < self._cache_duration:
                logger.debug(f"Cache hit for key: {cache_key}")
                return data
            else:
                # Remove expired entry
                del self._cache[cache_key]
        return None
    
    def _set_cache(self, cache_key: str, data: Any) -> None:
        """Store data in cache with current timestamp."""
        self._cache[cache_key] = (data, datetime.now())
        logger.debug(f"Cached data for key: {cache_key}")
    
    async def _make_request(
        self,
        endpoint: str,
        payload: Dict,
        use_cache: bool = True,
        max_retries: int = 3
    ) -> Dict:
        """
        Make an HTTP POST request with retry logic and caching.
        
        Args:
            endpoint: API endpoint path
            payload: Request payload
            use_cache: Whether to use caching
            max_retries: Maximum number of retry attempts
            
        Returns:
            Response data as dictionary
            
        Raises:
            APIClientError: If request fails after all retries
        """
        url = f"{self.base_url}/{endpoint}"
        cache_key = self._get_cache_key(endpoint, payload)
        
        # Check cache first
        if use_cache:
            cached_data = self._get_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
        
        # Make request with semaphore for rate limiting
        async with self._semaphore:
            for attempt in range(max_retries):
                try:
                    logger.info(f"Request to {endpoint} (attempt {attempt + 1}/{max_retries})")
                    
                    response = await self.client.post(url, json=payload)
                    response.raise_for_status()
                    
                    data = response.json()
                    logger.info(f"Successful response from {endpoint}")
                    
                    # Cache the response
                    if use_cache:
                        self._set_cache(cache_key, data)
                    
                    return data
                    
                except httpx.HTTPStatusError as e:
                    logger.error(f"HTTP error {e.response.status_code} from {endpoint}: {e}")
                    if e.response.status_code >= 500 and attempt < max_retries - 1:
                        # Retry on server errors with exponential backoff
                        await asyncio.sleep(2 ** attempt)
                        continue
                    raise APIClientError(f"HTTP {e.response.status_code}: {e}")
                    
                except httpx.RequestError as e:
                    logger.error(f"Request error to {endpoint}: {e}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    raise APIClientError(f"Request failed: {e}")
                    
                except Exception as e:
                    logger.error(f"Unexpected error in request to {endpoint}: {e}")
                    raise APIClientError(f"Unexpected error: {e}")
        
        raise APIClientError(f"Failed after {max_retries} retries")
    
    async def get_asset_price(self, asset_id: str) -> Dict:
        """
        Fetch current price data for an asset.
        
        Args:
            asset_id: Asset identifier (e.g., "AAPL", "TSLA")
            
        Returns:
            Dict containing:
                - currentPrice: Current trading price
                - previousClose: Previous closing price
                - changePercent: Percentage change
                - volume: Trading volume
                - lastUpdated: Timestamp of last update
        """
        payload = {"assetId": asset_id}
        return await self._make_request("getAssetPrice", payload)
    
    async def get_asset_classification(self, asset_id: str) -> Dict:
        """
        Get sector, industry, and classification data for an asset.
        
        Args:
            asset_id: Asset identifier
            
        Returns:
            Dict containing:
                - sector: Business sector
                - industry: Specific industry
                - marketCap: Market capitalization
                - geography: Primary geographic market
                - assetType: Type of asset (stock, ETF, etc.)
        """
        payload = {"assetId": asset_id}
        return await self._make_request("getAssetClassification", payload)
    
    async def get_asset_baskets(self, criteria: Dict) -> List[str]:
        """
        Find assets matching specific criteria.
        
        Args:
            criteria: Dictionary of search criteria (sector, marketCap, etc.)
            
        Returns:
            List of asset IDs matching the criteria
        """
        payload = {"criteria": criteria}
        response = await self._make_request("getAssetBaskets", payload, use_cache=False)
        return response.get("assetIds", [])
    
    async def get_asset_research_data(self, asset_id: str) -> Dict:
        """
        Get fundamentals, analyst ratings, and research data.
        
        Args:
            asset_id: Asset identifier
            
        Returns:
            Dict containing:
                - peRatio: Price-to-earnings ratio
                - revenueGrowth: Revenue growth rate
                - profitMargin: Profit margin percentage
                - consensusRating: Analyst consensus (Buy/Hold/Sell)
                - analystCount: Number of analysts covering
                - targetPrice: Average analyst target price
                - riskFactors: List of identified risk factors
        """
        payload = {"assetId": asset_id}
        return await self._make_request("getAssetResearchData", payload)
    
    async def batch_fetch(
        self,
        asset_ids: List[str],
        fetch_func: str = "get_asset_price"
    ) -> Dict[str, Dict]:
        """
        Fetch data for multiple assets in parallel using asyncio.gather.
        
        Args:
            asset_ids: List of asset identifiers
            fetch_func: Name of the fetch function to use
            
        Returns:
            Dictionary mapping asset_id to response data
        """
        func = getattr(self, fetch_func)
        tasks = [func(asset_id) for asset_id in asset_ids]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        output = {}
        for asset_id, result in zip(asset_ids, results):
            if isinstance(result, Exception):
                logger.error(f"Error fetching {asset_id}: {result}")
                output[asset_id] = {"error": str(result)}
            else:
                output[asset_id] = result
        
        return output


# Create a singleton instance
api_client = APIClient()
