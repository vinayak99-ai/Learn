"""
Sandboxed Python Code Execution using RestrictedPython
Provides safe execution of user-provided Python code with whitelisted functions
"""

from RestrictedPython import compile_restricted, safe_globals
from RestrictedPython.Guards import guarded_iter_unpack_sequence, safe_builtins
from RestrictedPython.Eval import default_guarded_getitem, default_guarded_getiter
import signal
import json
from typing import Dict, Any

# Execution timeout in seconds
TIMEOUT_SECONDS = 30

class TimeoutException(Exception):
    """Exception raised when code execution times out"""
    pass

def timeout_handler(signum, frame):
    """Signal handler for execution timeout"""
    raise TimeoutException("Code execution timed out")

def get_safe_builtins():
    """
    Returns a dictionary of safe built-in functions
    Whitelists only necessary and safe functions
    """
    safe_dict = {
        'True': True,
        'False': False,
        'None': None,
        'range': range,
        'len': len,
        'str': str,
        'int': int,
        'float': float,
        'list': list,
        'dict': dict,
        'sum': sum,
        'max': max,
        'min': min,
        'abs': abs,
        'round': round,
        'sorted': sorted,
        'enumerate': enumerate,
        'zip': zip,
        'map': map,
        'filter': filter,
        'any': any,
        'all': all,
        '_iter_unpack_sequence_': guarded_iter_unpack_sequence,
        '_getiter_': default_guarded_getiter,
        '_getitem_': default_guarded_getitem,
        '__builtins__': safe_builtins,
    }
    return safe_dict

def get_safe_globals():
    """
    Returns a dictionary of safe global variables and modules
    Includes whitelisted libraries and utility functions
    """
    import pandas as pd
    import json
    from datetime import datetime, timedelta
    
    # Safe data fetching functions (mocked for demo)
    def fetch_sales_data():
        """Mock function to fetch sales data"""
        return [
            {"month": "Jan", "sales": 12500, "region": "North"},
            {"month": "Feb", "sales": 15000, "region": "North"},
            {"month": "Mar", "sales": 13800, "region": "North"},
            {"month": "Apr", "sales": 16200, "region": "North"},
        ]
    
    def fetch_user_metrics():
        """Mock function to fetch user metrics"""
        return {
            "active_users": 15234,
            "new_users": 892,
            "churn_rate": 3.2,
            "avg_session_duration": 12.5
        }
    
    def fetch_table_data():
        """Mock function to fetch table data"""
        return [
            {"product": "Widget A", "quantity": 145, "revenue": 14500},
            {"product": "Widget B", "quantity": 203, "revenue": 20300},
            {"product": "Widget C", "quantity": 89, "revenue": 8900},
            {"product": "Widget D", "quantity": 167, "revenue": 16700},
        ]
    
    globals_dict = {
        # Safe libraries
        'pd': pd,
        'json': json,
        'datetime': datetime,
        'timedelta': timedelta,
        
        # Safe utility functions
        'fetch_sales_data': fetch_sales_data,
        'fetch_user_metrics': fetch_user_metrics,
        'fetch_table_data': fetch_table_data,
        
        # Add safe builtins
        **get_safe_builtins()
    }
    
    return globals_dict

def execute_sandboxed_code(code: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Execute Python code in a sandboxed environment
    
    Args:
        code: Python code string to execute
        parameters: Optional parameters to pass to the code
        
    Returns:
        Dict with success status, data, and optional error message
    """
    if parameters is None:
        parameters = {}
    
    try:
        # Compile the code with RestrictedPython
        byte_code = compile_restricted(
            code,
            filename='<inline code>',
            mode='exec'
        )
        
        # In RestrictedPython 7.x, compile_restricted returns a code object or raises SyntaxError
        # Check if byte_code has errors attribute (older API) or is a code object (new API)
        if hasattr(byte_code, 'errors') and byte_code.errors:
            return {
                "success": False,
                "error": f"Compilation errors: {', '.join(byte_code.errors)}",
                "data": None
            }
        
        # For new API, byte_code is directly the code object
        code_obj = byte_code.code if hasattr(byte_code, 'code') else byte_code
        
        # Prepare the execution environment
        restricted_globals = get_safe_globals()
        restricted_globals['__builtins__'] = safe_builtins
        restricted_globals['parameters'] = parameters
        
        # Set up timeout (Unix systems only)
        try:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(TIMEOUT_SECONDS)
        except (AttributeError, ValueError):
            # signal.SIGALRM not available on Windows
            pass
        
        # Execute the code
        exec(code_obj, restricted_globals)
        
        # Cancel the timeout
        try:
            signal.alarm(0)
        except (AttributeError, ValueError):
            pass
        
        # Get the result
        # The code should set a variable named 'result'
        if 'result' in restricted_globals:
            result_data = restricted_globals['result']
            return {
                "success": True,
                "data": result_data,
                "error": None
            }
        else:
            return {
                "success": False,
                "error": "Code did not set 'result' variable",
                "data": None
            }
            
    except TimeoutException:
        try:
            signal.alarm(0)
        except (AttributeError, ValueError):
            pass
        return {
            "success": False,
            "error": f"Code execution timed out after {TIMEOUT_SECONDS} seconds",
            "data": None
        }
    except Exception as e:
        try:
            signal.alarm(0)
        except (AttributeError, ValueError):
            pass
        return {
            "success": False,
            "error": f"Execution error: {str(e)}",
            "data": None
        }
