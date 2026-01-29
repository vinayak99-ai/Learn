"""Investment Research Orchestrator - Main FastAPI Application.

This module provides a FastAPI-based service that uses LangChain to orchestrate
multiple Java backend APIs for investment research through natural language queries.
"""

import logging
from typing import Optional, Dict, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import uvicorn

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

from .config import config
from .api_client import api_client
from .tools import (
    get_asset_price_tool,
    get_asset_classification_tool,
    get_asset_baskets_tool,
    get_asset_research_data_tool,
    compare_assets_tool,
    screen_assets_tool,
)

# Configure logging
logging.basicConfig(
    level=config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Request/Response Models
class ResearchRequest(BaseModel):
    """Request model for research endpoint."""
    query: str = Field(
        description="Natural language question about investments",
        examples=["What's the current price of Apple?", "Find me high-growth tech stocks"]
    )
    
    
class ResearchResponse(BaseModel):
    """Response model for research endpoint."""
    query: str
    answer: str
    
    
class CompareRequest(BaseModel):
    """Request model for comparison endpoint."""
    asset_ids: List[str] = Field(
        description="List of 2-5 asset IDs to compare",
        min_length=2,
        max_length=5
    )
    

class CompareResponse(BaseModel):
    """Response model for comparison endpoint."""
    comparison: str


class ScreenRequest(BaseModel):
    """Request model for screening endpoint."""
    sector: Optional[str] = None
    market_cap: Optional[str] = None
    price_range: Optional[str] = None
    min_growth: Optional[float] = None
    max_pe_ratio: Optional[float] = None
    limit: int = Field(default=10, ge=1, le=50)


class ScreenResponse(BaseModel):
    """Response model for screening endpoint."""
    results: str


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str
    version: str
    backend_url: str


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application lifecycle events."""
    # Startup
    logger.info(f"Starting {config.APP_NAME} v{config.APP_VERSION}")
    
    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        logger.error(f"Configuration validation failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    await api_client.close()


# Create FastAPI application
app = FastAPI(
    title="Investment Research Orchestrator",
    description="LangChain-powered orchestration of Java backend investment APIs",
    version=config.APP_VERSION,
    lifespan=lifespan
)


def create_agent() -> AgentExecutor:
    """
    Create and configure the LangChain agent with OpenAI Functions.
    
    Returns:
        Configured AgentExecutor ready to process queries
    """
    # Initialize OpenAI LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        openai_api_key=config.OPENAI_API_KEY
    )
    
    # Define the tools available to the agent
    tools = [
        get_asset_price_tool,
        get_asset_classification_tool,
        get_asset_baskets_tool,
        get_asset_research_data_tool,
        compare_assets_tool,
        screen_assets_tool,
    ]
    
    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert investment research assistant with access to comprehensive
        financial data through multiple specialized tools. Your role is to help users make informed
        investment decisions by providing accurate, well-reasoned analysis.
        
        Available tools allow you to:
        - Get current price data for assets
        - Retrieve sector and industry classifications
        - Find assets matching specific criteria
        - Access fundamental research and analyst ratings
        - Compare multiple assets side-by-side
        - Screen for assets with enriched data
        
        When answering questions:
        1. Use the appropriate tools to gather necessary data
        2. Provide clear, concise analysis with supporting data
        3. Format numbers appropriately (currencies, percentages, etc.)
        4. Include relevant context and reasoning
        5. Be transparent about data limitations
        
        Always base your responses on data from the tools, not on assumptions."""),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create the agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    
    # Create the agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        return_intermediate_steps=False,
    )
    
    return agent_executor


# API Endpoints

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify service status.
    
    Returns:
        Service health information
    """
    return HealthResponse(
        status="healthy",
        version=config.APP_VERSION,
        backend_url=config.JAVA_BACKEND_URL
    )


@app.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):
    """
    Main research endpoint that accepts natural language questions.
    
    This endpoint uses a LangChain agent to intelligently orchestrate
    multiple Java backend APIs to answer investment questions.
    
    Args:
        request: Natural language query about investments
        
    Returns:
        AI-generated answer with supporting data
    """
    try:
        logger.info(f"Research query: {request.query}")
        
        # Create agent executor
        agent_executor = create_agent()
        
        # Execute the query
        result = await agent_executor.ainvoke({"input": request.query})
        
        answer = result.get("output", "Unable to generate response")
        
        logger.info(f"Research query completed successfully")
        
        return ResearchResponse(
            query=request.query,
            answer=answer
        )
        
    except Exception as e:
        logger.error(f"Error processing research query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )


@app.post("/compare", response_model=CompareResponse)
async def compare(request: CompareRequest):
    """
    Endpoint for direct asset comparison.
    
    Args:
        request: List of 2-5 asset IDs to compare
        
    Returns:
        Side-by-side comparison of assets
    """
    try:
        logger.info(f"Comparing assets: {request.asset_ids}")
        
        # Directly use the comparison tool
        result = await compare_assets_tool.ainvoke({"asset_ids": request.asset_ids})
        
        return CompareResponse(comparison=result)
        
    except Exception as e:
        logger.error(f"Error comparing assets: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error comparing assets: {str(e)}"
        )


@app.post("/screen", response_model=ScreenResponse)
async def screen(request: ScreenRequest):
    """
    Endpoint for screening assets by criteria.
    
    Args:
        request: Screening criteria (sector, market_cap, etc.)
        
    Returns:
        List of assets matching criteria with enriched data
    """
    try:
        logger.info(f"Screening assets with criteria: {request.dict()}")
        
        # Build input for screening tool
        screening_input = {
            k: v for k, v in request.dict().items() 
            if v is not None
        }
        
        # Use the screening tool
        result = await screen_assets_tool.ainvoke(screening_input)
        
        return ScreenResponse(results=result)
        
    except Exception as e:
        logger.error(f"Error screening assets: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error screening assets: {str(e)}"
        )


# Main entry point for running with uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "orchestrator:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=config.LOG_LEVEL.lower()
    )
