"""
FastAPI Backend for Widget Execution System
Provides endpoints to fetch widget configurations and execute Python code safely
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import time

from sandbox_executor import execute_sandboxed_code
from widget_configs import get_widget_configs, get_widget_by_id

app = FastAPI(title="Widget Execution API")

# Configure CORS for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class WidgetExecutionRequest(BaseModel):
    widgetId: str
    pythonCode: str
    parameters: Optional[Dict[str, Any]] = None

class WidgetExecutionResult(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    executionTime: Optional[float] = None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Widget Execution API",
        "version": "1.0.0"
    }

@app.get("/api/widgets")
async def get_widgets():
    """
    Get all widget configurations
    Returns a list of widget configurations with their Python code
    """
    try:
        configs = get_widget_configs()
        return configs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/widgets/{widget_id}")
async def get_widget(widget_id: str):
    """
    Get a specific widget configuration by ID
    """
    try:
        config = get_widget_by_id(widget_id)
        if not config:
            raise HTTPException(status_code=404, detail=f"Widget {widget_id} not found")
        return config
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/execute-widget")
async def execute_widget(request: WidgetExecutionRequest) -> WidgetExecutionResult:
    """
    Execute widget Python code in a sandboxed environment
    
    Security features:
    - RestrictedPython for safe execution
    - Timeout protection
    - Whitelisted builtins and libraries
    """
    start_time = time.time()
    
    try:
        # Execute the Python code in sandbox
        result = execute_sandboxed_code(
            code=request.pythonCode,
            parameters=request.parameters or {}
        )
        
        execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        if result["success"]:
            return WidgetExecutionResult(
                success=True,
                data=result["data"],
                executionTime=execution_time
            )
        else:
            return WidgetExecutionResult(
                success=False,
                error=result["error"],
                executionTime=execution_time
            )
            
    except Exception as e:
        execution_time = (time.time() - start_time) * 1000
        return WidgetExecutionResult(
            success=False,
            error=f"Execution failed: {str(e)}",
            executionTime=execution_time
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
