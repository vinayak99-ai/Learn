#!/usr/bin/env python3
"""
Test script for the widget backend
Tests the sandbox executor and widget configuration functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sandbox_executor import execute_sandboxed_code
from widget_configs import get_widget_configs, get_widget_by_id

def test_sandbox_executor():
    """Test the sandbox executor with various code samples"""
    
    print("=" * 70)
    print("Testing Sandbox Executor")
    print("=" * 70)
    
    # Test 1: Simple result
    print("\n1. Testing simple result assignment:")
    code1 = "result = {'value': 42, 'message': 'Hello'}"
    result1 = execute_sandboxed_code(code1)
    print(f"   Code: {code1}")
    print(f"   Success: {result1['success']}")
    print(f"   Data: {result1['data']}")
    assert result1['success'] == True
    assert result1['data']['value'] == 42
    print("   ✓ Test passed")
    
    # Test 2: Using whitelisted functions
    print("\n2. Testing whitelisted functions:")
    code2 = "result = sum([1, 2, 3, 4, 5])"
    result2 = execute_sandboxed_code(code2)
    print(f"   Code: {code2}")
    print(f"   Success: {result2['success']}")
    print(f"   Data: {result2['data']}")
    assert result2['success'] == True
    assert result2['data'] == 15
    print("   ✓ Test passed")
    
    # Test 3: Using fetch_sales_data
    print("\n3. Testing fetch_sales_data function:")
    code3 = """
data = fetch_sales_data()
result = {
    'count': len(data),
    'first_month': data[0]['month'],
    'total_sales': sum(item['sales'] for item in data)
}
"""
    result3 = execute_sandboxed_code(code3)
    print(f"   Success: {result3['success']}")
    print(f"   Data: {result3['data']}")
    assert result3['success'] == True
    assert result3['data']['count'] == 4
    print("   ✓ Test passed")
    
    # Test 4: Error handling - missing result
    print("\n4. Testing error handling (missing result):")
    code4 = "x = 42"
    result4 = execute_sandboxed_code(code4)
    print(f"   Code: {code4}")
    print(f"   Success: {result4['success']}")
    print(f"   Error: {result4['error']}")
    assert result4['success'] == False
    print("   ✓ Test passed")
    
    # Test 5: Error handling - syntax error
    print("\n5. Testing error handling (syntax error):")
    code5 = "result = {"
    result5 = execute_sandboxed_code(code5)
    print(f"   Code: {code5}")
    print(f"   Success: {result5['success']}")
    print(f"   Error: {result5['error']}")
    assert result5['success'] == False
    print("   ✓ Test passed")
    
    print("\n" + "=" * 70)
    print("All sandbox executor tests passed!")
    print("=" * 70)

def test_widget_configs():
    """Test widget configuration functions"""
    
    print("\n" + "=" * 70)
    print("Testing Widget Configurations")
    print("=" * 70)
    
    # Test 1: Get all configs
    print("\n1. Testing get_widget_configs:")
    configs = get_widget_configs()
    print(f"   Number of widgets: {len(configs)}")
    for config in configs:
        print(f"   - {config['id']}: {config['name']} ({config['type']})")
    assert len(configs) == 5
    print("   ✓ Test passed")
    
    # Test 2: Get specific widget
    print("\n2. Testing get_widget_by_id:")
    widget = get_widget_by_id("sales-chart")
    print(f"   Widget ID: {widget['id']}")
    print(f"   Widget Name: {widget['name']}")
    print(f"   Widget Type: {widget['type']}")
    assert widget is not None
    assert widget['type'] == 'chart'
    print("   ✓ Test passed")
    
    # Test 3: Non-existent widget
    print("\n3. Testing non-existent widget:")
    widget = get_widget_by_id("non-existent")
    print(f"   Result: {widget}")
    assert widget is None
    print("   ✓ Test passed")
    
    print("\n" + "=" * 70)
    print("All widget configuration tests passed!")
    print("=" * 70)

def test_widget_execution():
    """Test executing actual widget code"""
    
    print("\n" + "=" * 70)
    print("Testing Widget Code Execution")
    print("=" * 70)
    
    configs = get_widget_configs()
    
    for i, config in enumerate(configs, 1):
        print(f"\n{i}. Testing widget: {config['name']} ({config['id']})")
        result = execute_sandboxed_code(config['pythonCode'], config.get('parameters', {}))
        
        if result['success']:
            print(f"   ✓ Execution successful")
            print(f"   Data type: {type(result['data'])}")
            if isinstance(result['data'], dict):
                print(f"   Data keys: {list(result['data'].keys())}")
            elif isinstance(result['data'], list):
                print(f"   Data items: {len(result['data'])}")
        else:
            print(f"   ✗ Execution failed: {result['error']}")
            return False
    
    print("\n" + "=" * 70)
    print("All widget executions passed!")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        test_sandbox_executor()
        test_widget_configs()
        test_widget_execution()
        
        print("\n" + "=" * 70)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("=" * 70)
        sys.exit(0)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
