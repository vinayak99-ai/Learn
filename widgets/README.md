# Angular Widgets System with Python Backend

A complete, production-ready widgets system that enables dynamic execution of Python code through a secure backend, with real-time data visualization in Angular.

## 📋 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Features](#features)
- [File Structure](#file-structure)
- [Setup Instructions](#setup-instructions)
  - [Python Backend Setup](#python-backend-setup)
  - [Angular Frontend Setup](#angular-frontend-setup)
- [Usage Guide](#usage-guide)
- [Security Considerations](#security-considerations)
- [Creating New Widgets](#creating-new-widgets)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

## 🏗️ Architecture Overview

This system consists of two main components:

### Frontend (Angular)
- **Models**: TypeScript interfaces for type-safe widget configurations
- **Services**: HTTP service for backend communication
- **Components**: Reusable widget components with different visualizations
- **Module**: Self-contained Angular module for easy integration

### Backend (Python/FastAPI)
- **FastAPI Server**: RESTful API with CORS support for Angular
- **Sandboxed Execution**: RestrictedPython for safe code execution
- **Widget Configs**: Centralized widget configuration management
- **Timeout Protection**: Prevents long-running code execution

### Data Flow
```
Angular Component → Widget Service → FastAPI Endpoint → 
Sandboxed Executor → Python Code Execution → Result → 
Angular Component → Visualization
```

## ✨ Features

### Frontend Features
- **Dynamic Widget Loading**: Load widgets from backend configurations
- **Multiple Widget Types**: Chart, Table, Metric, and Custom widgets
- **Auto-Refresh**: Configurable automatic data refresh intervals
- **Loading States**: User-friendly loading and error states
- **Responsive Grid**: Adaptive grid layout for different screen sizes
- **Manual Refresh**: Button to manually refresh individual widgets

### Backend Features
- **Secure Execution**: RestrictedPython sandboxing with whitelisted functions
- **Timeout Protection**: 30-second execution timeout
- **Error Handling**: Comprehensive error messages and logging
- **CORS Support**: Configured for Angular development server
- **Fast Performance**: Async FastAPI for high throughput
- **Sample Data**: Built-in mock data functions for testing

## 📁 File Structure

```
widgets/
├── README.md                          # This file
├── frontend/
│   └── src/
│       └── app/
│           └── widgets/
│               ├── widgets.module.ts                    # Angular module
│               ├── models/
│               │   └── widget-config.model.ts          # TypeScript interfaces
│               ├── services/
│               │   └── widget.service.ts               # HTTP service
│               └── components/
│                   ├── dynamic-widget/                 # Main widget component
│                   │   ├── dynamic-widget.component.ts
│                   │   ├── dynamic-widget.component.html
│                   │   └── dynamic-widget.component.css
│                   ├── dashboard/                      # Dashboard container
│                   │   ├── dashboard.component.ts
│                   │   ├── dashboard.component.html
│                   │   └── dashboard.component.css
│                   ├── chart-widget/                   # Chart visualization
│                   │   └── chart-widget.component.ts
│                   ├── table-widget/                   # Table visualization
│                   │   └── table-widget.component.ts
│                   └── metric-widget/                  # Metric/KPI visualization
│                       └── metric-widget.component.ts
└── backend/
    ├── main.py                        # FastAPI application
    ├── sandbox_executor.py            # RestrictedPython execution engine
    ├── widget_configs.py              # Widget configuration storage
    └── requirements.txt               # Python dependencies
```

## 🚀 Setup Instructions

### Python Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd widgets/backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server:**
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Verify the server is running:**
   - Visit: http://localhost:8000
   - API docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Angular Frontend Setup

1. **Ensure you have Node.js and Angular CLI installed:**
   ```bash
   node --version  # Should be v14+ 
   npm --version
   npm install -g @angular/cli
   ```

2. **Navigate to your Angular project root:**
   ```bash
   cd your-angular-project
   ```

3. **Copy the widgets folder into your Angular app:**
   ```bash
   # The widgets folder should be at:
   # your-angular-project/src/app/widgets/
   ```

4. **Import the WidgetsModule in your app.module.ts:**
   ```typescript
   import { WidgetsModule } from './widgets/widgets.module';

   @NgModule({
     declarations: [
       AppComponent,
       // ... other components
     ],
     imports: [
       BrowserModule,
       WidgetsModule,  // Add this
       // ... other modules
     ],
     bootstrap: [AppComponent]
   })
   export class AppModule { }
   ```

5. **Add the dashboard to your app component or routing:**
   
   In your template:
   ```html
   <app-dashboard></app-dashboard>
   ```
   
   Or in your routing module:
   ```typescript
   import { DashboardComponent } from './widgets/components/dashboard/dashboard.component';

   const routes: Routes = [
     { path: 'dashboard', component: DashboardComponent },
     // ... other routes
   ];
   ```

6. **Start the Angular development server:**
   ```bash
   ng serve
   ```

7. **Access the application:**
   - Open: http://localhost:4200
   - Navigate to your dashboard route

## 📖 Usage Guide

### Using the Dashboard

1. Start both the Python backend and Angular frontend
2. Navigate to the dashboard in your browser
3. Widgets will automatically load and execute their Python code
4. Use the refresh button (🔄) to manually update a widget
5. Widgets with auto-refresh will update automatically at their configured intervals

### Widget Types

#### Chart Widget
- Displays bar charts with labeled data
- Best for comparing values across categories
- Supports gradient coloring and animations

#### Table Widget
- Displays data in a structured table format
- Supports sorting and formatting
- Best for detailed data inspection

#### Metric Widget
- Displays key performance indicators (KPIs)
- Shows change percentages with up/down indicators
- Supports icons and descriptions
- Best for at-a-glance metrics

#### Custom Widget
- Displays raw JSON data
- Flexible format for any data structure
- Best for debugging or custom visualizations

## 🔒 Security Considerations

### RestrictedPython Sandboxing

The system uses RestrictedPython to safely execute user-provided Python code:

1. **Whitelisted Builtins**: Only safe built-in functions are available
   - Allowed: `range`, `len`, `str`, `int`, `float`, `list`, `dict`, etc.
   - Blocked: `eval`, `exec`, `open`, `__import__`, etc.

2. **Whitelisted Libraries**: Only approved libraries are accessible
   - Allowed: `pandas`, `json`, `datetime`
   - Custom data fetching functions are pre-defined
   - No arbitrary imports allowed

3. **Timeout Protection**:
   - Maximum execution time: 30 seconds
   - Prevents infinite loops and long-running operations
   - Automatic termination on timeout

4. **No File System Access**: 
   - Code cannot read or write files
   - No network access from sandbox
   - Cannot execute system commands

### Recommended Additional Security Measures

For production deployment, implement:

1. **Authentication & Authorization**:
   ```python
   # Add to main.py
   from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
   
   security = HTTPBearer()
   
   @app.post("/api/execute-widget")
   async def execute_widget(
       request: WidgetExecutionRequest,
       credentials: HTTPAuthorizationCredentials = Depends(security)
   ):
       # Verify token
       verify_token(credentials.credentials)
       # ... rest of code
   ```

2. **Rate Limiting**:
   ```python
   from slowapi import Limiter
   from slowapi.util import get_remote_address
   
   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
   
   @app.post("/api/execute-widget")
   @limiter.limit("10/minute")
   async def execute_widget(request: WidgetExecutionRequest):
       # ... code
   ```

3. **Input Validation**:
   - Validate all input parameters
   - Limit code length (e.g., max 10KB)
   - Sanitize widget IDs and parameters

4. **Logging & Monitoring**:
   - Log all code executions
   - Monitor execution times and errors
   - Alert on suspicious patterns

5. **Resource Limits**:
   - Set memory limits per execution
   - Limit concurrent executions
   - Use containerization (Docker) for isolation

6. **HTTPS Only**:
   - Use TLS/SSL in production
   - Never send code over unencrypted connections

## 🎨 Creating New Widgets

### Step 1: Add Widget Configuration

Edit `backend/widget_configs.py`:

```python
{
    "id": "my-new-widget",
    "name": "My Custom Widget",
    "type": "chart",  # or "table", "metric", "custom"
    "description": "Description of what this widget does",
    "pythonCode": """
# Your Python code here
# Must set 'result' variable with output data

data = fetch_sales_data()  # Use provided functions
result = [
    {"label": item["month"], "value": item["sales"]}
    for item in data
]
""",
    "parameters": {},  # Optional parameters
    "refreshInterval": 60  # Optional: seconds between auto-refresh
}
```

### Step 2: Write the Python Code

Your Python code should:
1. Use whitelisted functions and libraries
2. Set a variable named `result` with the output data
3. Format data according to widget type expectations

#### Chart Widget Data Format:
```python
result = [
    {"label": "Category 1", "value": 100},
    {"label": "Category 2", "value": 200},
    # ...
]
```

#### Table Widget Data Format:
```python
result = {
    "data": [
        {"col1": "value1", "col2": "value2"},
        {"col1": "value3", "col2": "value4"},
    ],
    "columns": ["col1", "col2"]  # Optional
}
```

#### Metric Widget Data Format:
```python
result = {
    "metrics": [
        {
            "label": "Total Sales",
            "value": 15234,
            "icon": "💰",
            "change": 12.5,  # Optional: percentage change
            "description": "Total sales this month"
        },
        # ...
    ]
}
```

### Step 3: Restart Backend

Restart the FastAPI server to load new configurations:
```bash
# Stop the server (Ctrl+C)
# Start again
python main.py
```

### Step 4: Test

The new widget will automatically appear in the dashboard!

## 📚 API Documentation

### GET `/api/widgets`

Get all widget configurations.

**Response:**
```json
[
  {
    "id": "sales-chart",
    "name": "Monthly Sales",
    "type": "chart",
    "description": "Monthly sales data visualization",
    "pythonCode": "...",
    "parameters": {},
    "refreshInterval": 60
  }
]
```

### GET `/api/widgets/{widget_id}`

Get a specific widget configuration.

**Parameters:**
- `widget_id` (path): Widget ID

**Response:**
```json
{
  "id": "sales-chart",
  "name": "Monthly Sales",
  "type": "chart",
  "pythonCode": "...",
  "parameters": {},
  "refreshInterval": 60
}
```

### POST `/api/execute-widget`

Execute widget Python code.

**Request Body:**
```json
{
  "widgetId": "sales-chart",
  "pythonCode": "result = {'data': [1, 2, 3]}",
  "parameters": {}
}
```

**Response:**
```json
{
  "success": true,
  "data": {"data": [1, 2, 3]},
  "error": null,
  "executionTime": 45.2
}
```

## 🔧 Troubleshooting

### Backend Issues

**Issue: "Module not found" errors**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

**Issue: "Port 8000 already in use"**
```bash
# Solution: Use a different port
uvicorn main:app --port 8001
# Update Angular service URL accordingly
```

**Issue: RestrictedPython import errors**
```bash
# Solution: Ensure correct version
pip install RestrictedPython==6.2
```

### Frontend Issues

**Issue: CORS errors**
```
Solution: Ensure backend CORS is configured for your frontend URL
Update allow_origins in backend/main.py if needed
```

**Issue: "Cannot find module" errors**
```bash
# Solution: Ensure module is imported in app.module.ts
# Check that all paths are correct
```

**Issue: Widgets not loading**
```
Solution: 
1. Check backend is running (http://localhost:8000)
2. Check browser console for errors
3. Verify API URL in widget.service.ts
```

### Common Python Code Issues

**Issue: "Code did not set 'result' variable"**
```python
# Solution: Always set result variable
result = your_data
```

**Issue: "Compilation errors"**
```python
# Solution: Avoid restricted operations
# ❌ Don't use: import, open(), eval(), exec()
# ✅ Use whitelisted functions and provided utilities
```

## 🤝 Contributing

To extend this system:

1. **Add new widget types**: Create new specialized components
2. **Add data sources**: Extend `sandbox_executor.py` with new safe functions
3. **Enhance security**: Add authentication, rate limiting, etc.
4. **Add features**: Implement widget editing, saving, export, etc.

## 📄 License

This is a learning project. Use and modify as needed.

## 🙋 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API documentation at http://localhost:8000/docs
3. Inspect browser console and backend logs for errors

---

**Built with ❤️ using Angular and FastAPI**
