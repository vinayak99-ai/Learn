# API Design Documentation

## Table of Contents
1. [Overview](#overview)
2. [Base Configuration](#base-configuration)
3. [Authentication](#authentication)
4. [Comprehensions Endpoints](#comprehensions-endpoints)
5. [Quizzes Endpoints](#quizzes-endpoints)
6. [Search Endpoints](#search-endpoints)
7. [Error Handling](#error-handling)
8. [Data Models](#data-models)
9. [Example Code](#example-code)

## Overview

The FastAPI backend provides RESTful API endpoints for managing comprehensions and quizzes. All endpoints return JSON responses and follow REST conventions.

**API Version**: v1  
**Base URL**: `http://localhost:8000/api/v1` (development)  
**Content-Type**: `application/json`  
**Status Codes**: Standard HTTP status codes

## Base Configuration

### FastAPI Application Setup

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Comprehension Quiz API",
    description="API for managing reading comprehensions and quizzes",
    version="1.0.0",
    docs_url="/api/docs",  # Swagger UI
    redoc_url="/api/redoc"  # ReDoc
)

# CORS configuration for Dash frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8050"],  # Dash default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Response Format

All successful responses follow this structure:

```json
{
    "status": "success",
    "data": { /* response data */ },
    "message": "Operation completed successfully"
}
```

Error responses:

```json
{
    "status": "error",
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable error message",
        "details": { /* optional additional details */ }
    }
}
```

## Authentication

**Note**: Authentication is optional for the initial version. Future versions will include JWT-based authentication.

### Future Authentication Flow

```
POST /api/v1/auth/login
POST /api/v1/auth/register
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
```

All protected endpoints will require:
```
Authorization: Bearer <jwt_token>
```

## Comprehensions Endpoints

### 1. Get All Comprehensions

Retrieve a list of all comprehensions with optional filtering and pagination.

**Endpoint**: `GET /api/v1/comprehensions`

**Query Parameters**:
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum number of records to return (default: 10, max: 100)
- `difficulty` (string, optional): Filter by difficulty ('easy', 'medium', 'hard')
- `sort_by` (string, optional): Sort field ('created_at', 'updated_at', 'title') (default: 'created_at')
- `sort_order` (string, optional): Sort order ('asc', 'desc') (default: 'desc')

**Request Example**:
```http
GET /api/v1/comprehensions?skip=0&limit=10&difficulty=easy&sort_by=created_at&sort_order=desc
```

**Response** (200 OK):
```json
{
    "status": "success",
    "data": {
        "comprehensions": [
            {
                "id": 1,
                "title": "Understanding Photosynthesis",
                "content": "Photosynthesis is the process...",
                "difficulty_level": "easy",
                "quiz_count": 5,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            },
            {
                "id": 2,
                "title": "The Water Cycle",
                "content": "The water cycle, also known as...",
                "difficulty_level": "medium",
                "quiz_count": 8,
                "created_at": "2024-01-14T14:20:00Z",
                "updated_at": "2024-01-14T14:20:00Z"
            }
        ],
        "total": 25,
        "skip": 0,
        "limit": 10
    },
    "message": "Comprehensions retrieved successfully"
}
```

### 2. Get Single Comprehension

Retrieve a specific comprehension by ID.

**Endpoint**: `GET /api/v1/comprehensions/{id}`

**Path Parameters**:
- `id` (integer, required): Comprehension ID

**Request Example**:
```http
GET /api/v1/comprehensions/1
```

**Response** (200 OK):
```json
{
    "status": "success",
    "data": {
        "id": 1,
        "title": "Understanding Photosynthesis",
        "content": "Photosynthesis is the process by which green plants...",
        "difficulty_level": "easy",
        "quiz_count": 5,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    },
    "message": "Comprehension retrieved successfully"
}
```

**Response** (404 Not Found):
```json
{
    "status": "error",
    "error": {
        "code": "COMPREHENSION_NOT_FOUND",
        "message": "Comprehension with ID 1 not found"
    }
}
```

### 3. Create Comprehension

Create a new comprehension.

**Endpoint**: `POST /api/v1/comprehensions`

**Request Body**:
```json
{
    "title": "Understanding Photosynthesis",
    "content": "Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize nutrients from carbon dioxide and water...",
    "difficulty_level": "easy"
}
```

**Validation Rules**:
- `title`: Required, 5-255 characters
- `content`: Required, minimum 50 characters
- `difficulty_level`: Required, must be 'easy', 'medium', or 'hard'

**Response** (201 Created):
```json
{
    "status": "success",
    "data": {
        "id": 1,
        "title": "Understanding Photosynthesis",
        "content": "Photosynthesis is the process...",
        "difficulty_level": "easy",
        "quiz_count": 0,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    },
    "message": "Comprehension created successfully"
}
```

**Response** (422 Unprocessable Entity):
```json
{
    "status": "error",
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": [
            {
                "field": "content",
                "message": "Content must be at least 50 characters long"
            }
        ]
    }
}
```

### 4. Update Comprehension

Update an existing comprehension.

**Endpoint**: `PUT /api/v1/comprehensions/{id}`

**Path Parameters**:
- `id` (integer, required): Comprehension ID

**Request Body** (all fields optional):
```json
{
    "title": "Understanding Photosynthesis - Updated",
    "content": "Updated content...",
    "difficulty_level": "medium"
}
```

**Response** (200 OK):
```json
{
    "status": "success",
    "data": {
        "id": 1,
        "title": "Understanding Photosynthesis - Updated",
        "content": "Updated content...",
        "difficulty_level": "medium",
        "quiz_count": 5,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T11:45:00Z"
    },
    "message": "Comprehension updated successfully"
}
```

### 5. Delete Comprehension

Delete a comprehension and all associated quizzes (cascade delete).

**Endpoint**: `DELETE /api/v1/comprehensions/{id}`

**Path Parameters**:
- `id` (integer, required): Comprehension ID

**Request Example**:
```http
DELETE /api/v1/comprehensions/1
```

**Response** (200 OK):
```json
{
    "status": "success",
    "data": {
        "id": 1,
        "deleted_quiz_count": 5
    },
    "message": "Comprehension and 5 associated quizzes deleted successfully"
}
```

**Response** (404 Not Found):
```json
{
    "status": "error",
    "error": {
        "code": "COMPREHENSION_NOT_FOUND",
        "message": "Comprehension with ID 1 not found"
    }
}
```

## Quizzes Endpoints

### 1. Get Quizzes by Comprehension

Retrieve all quizzes for a specific comprehension.

**Endpoint**: `GET /api/v1/quizzes`

**Query Parameters**:
- `comprehension_id` (integer, required): Filter by comprehension ID
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum records to return (default: 50, max: 100)

**Request Example**:
```http
GET /api/v1/quizzes?comprehension_id=1&skip=0&limit=50
```

**Response** (200 OK):
```json
{
    "status": "success",
    "data": {
        "quizzes": [
            {
                "id": 1,
                "comprehension_id": 1,
                "question": "What is the primary function of chlorophyll in photosynthesis?",
                "option_a": "To store water",
                "option_b": "To capture light energy",
                "option_c": "To release oxygen",
                "option_d": "To produce glucose",
                "correct_answer": "B",
                "explanation": "Chlorophyll is the green pigment in plants...",
                "created_at": "2024-01-15T10:35:00Z",
                "updated_at": "2024-01-15T10:35:00Z"
            },
            {
                "id": 2,
                "comprehension_id": 1,
                "question": "What is produced as a byproduct of photosynthesis?",
                "option_a": "Carbon dioxide",
                "option_b": "Nitrogen",
                "option_c": "Oxygen",
                "option_d": "Hydrogen",
                "correct_answer": "C",
                "explanation": "Oxygen (O2) is released as a byproduct...",
                "created_at": "2024-01-15T10:36:00Z",
                "updated_at": "2024-01-15T10:36:00Z"
            }
        ],
        "total": 5,
        "comprehension_title": "Understanding Photosynthesis"
    },
    "message": "Quizzes retrieved successfully"
}
```

### 2. Get Single Quiz

Retrieve a specific quiz by ID.

**Endpoint**: `GET /api/v1/quizzes/{id}`

**Path Parameters**:
- `id` (integer, required): Quiz ID

**Response** (200 OK):
```json
{
    "status": "success",
    "data": {
        "id": 1,
        "comprehension_id": 1,
        "comprehension_title": "Understanding Photosynthesis",
        "question": "What is the primary function of chlorophyll in photosynthesis?",
        "option_a": "To store water",
        "option_b": "To capture light energy",
        "option_c": "To release oxygen",
        "option_d": "To produce glucose",
        "correct_answer": "B",
        "explanation": "Chlorophyll is the green pigment in plants...",
        "created_at": "2024-01-15T10:35:00Z",
        "updated_at": "2024-01-15T10:35:00Z"
    },
    "message": "Quiz retrieved successfully"
}
```

### 3. Create Quiz

Create a new quiz for a comprehension.

**Endpoint**: `POST /api/v1/quizzes`

**Request Body**:
```json
{
    "comprehension_id": 1,
    "question": "What is the primary function of chlorophyll in photosynthesis?",
    "option_a": "To store water",
    "option_b": "To capture light energy",
    "option_c": "To release oxygen",
    "option_d": "To produce glucose",
    "correct_answer": "B",
    "explanation": "Chlorophyll is the green pigment in plants that captures light energy from the sun."
}
```

**Validation Rules**:
- `comprehension_id`: Required, must reference existing comprehension
- `question`: Required, minimum 10 characters
- `option_a`, `option_b`, `option_c`, `option_d`: Required, 1-500 characters each
- `correct_answer`: Required, must be 'A', 'B', 'C', or 'D'
- `explanation`: Optional, recommended 50-500 characters

**Response** (201 Created):
```json
{
    "status": "success",
    "data": {
        "id": 1,
        "comprehension_id": 1,
        "question": "What is the primary function of chlorophyll in photosynthesis?",
        "option_a": "To store water",
        "option_b": "To capture light energy",
        "option_c": "To release oxygen",
        "option_d": "To produce glucose",
        "correct_answer": "B",
        "explanation": "Chlorophyll is the green pigment in plants...",
        "created_at": "2024-01-15T10:35:00Z",
        "updated_at": "2024-01-15T10:35:00Z"
    },
    "message": "Quiz created successfully"
}
```

**Response** (404 Not Found):
```json
{
    "status": "error",
    "error": {
        "code": "COMPREHENSION_NOT_FOUND",
        "message": "Comprehension with ID 1 not found"
    }
}
```

### 4. Update Quiz

Update an existing quiz.

**Endpoint**: `PUT /api/v1/quizzes/{id}`

**Path Parameters**:
- `id` (integer, required): Quiz ID

**Request Body** (all fields optional):
```json
{
    "question": "Updated question text?",
    "option_a": "Updated option A",
    "correct_answer": "A",
    "explanation": "Updated explanation"
}
```

**Response** (200 OK):
```json
{
    "status": "success",
    "data": {
        "id": 1,
        "comprehension_id": 1,
        "question": "Updated question text?",
        "option_a": "Updated option A",
        "option_b": "To capture light energy",
        "option_c": "To release oxygen",
        "option_d": "To produce glucose",
        "correct_answer": "A",
        "explanation": "Updated explanation",
        "created_at": "2024-01-15T10:35:00Z",
        "updated_at": "2024-01-15T11:50:00Z"
    },
    "message": "Quiz updated successfully"
}
```

### 5. Delete Quiz

Delete a specific quiz.

**Endpoint**: `DELETE /api/v1/quizzes/{id}`

**Path Parameters**:
- `id` (integer, required): Quiz ID

**Response** (200 OK):
```json
{
    "status": "success",
    "data": {
        "id": 1
    },
    "message": "Quiz deleted successfully"
}
```

### 6. Submit Quiz Answers

Submit answers for multiple quiz questions and get scoring results.

**Endpoint**: `POST /api/v1/quizzes/submit`

**Request Body**:
```json
{
    "comprehension_id": 1,
    "answers": [
        {
            "quiz_id": 1,
            "selected_answer": "B"
        },
        {
            "quiz_id": 2,
            "selected_answer": "C"
        },
        {
            "quiz_id": 3,
            "selected_answer": "C"
        }
    ]
}
```

**Response** (200 OK):
```json
{
    "status": "success",
    "data": {
        "comprehension_id": 1,
        "comprehension_title": "Understanding Photosynthesis",
        "total_questions": 3,
        "correct_answers": 3,
        "incorrect_answers": 0,
        "score_percentage": 100.0,
        "results": [
            {
                "quiz_id": 1,
                "question": "What is the primary function of chlorophyll in photosynthesis?",
                "selected_answer": "B",
                "correct_answer": "B",
                "is_correct": true,
                "explanation": "Chlorophyll is the green pigment in plants..."
            },
            {
                "quiz_id": 2,
                "question": "What is produced as a byproduct of photosynthesis?",
                "selected_answer": "C",
                "correct_answer": "C",
                "is_correct": true,
                "explanation": "Oxygen (O2) is released as a byproduct..."
            },
            {
                "quiz_id": 3,
                "question": "Where does photosynthesis occur in plant cells?",
                "selected_answer": "C",
                "correct_answer": "C",
                "is_correct": true,
                "explanation": "Photosynthesis occurs in the chloroplasts..."
            }
        ]
    },
    "message": "Quiz submitted and scored successfully"
}
```

**Response** (400 Bad Request):
```json
{
    "status": "error",
    "error": {
        "code": "INVALID_QUIZ_ID",
        "message": "One or more quiz IDs do not belong to the specified comprehension",
        "details": {
            "invalid_quiz_ids": [5, 7]
        }
    }
}
```

## Search Endpoints

### 1. Search Comprehensions

Search for comprehensions using full-text search on title and content.

**Endpoint**: `GET /api/v1/search/comprehensions`

**Query Parameters**:
- `q` (string, required): Search query
- `difficulty` (string, optional): Filter by difficulty
- `skip` (integer, optional): Pagination offset (default: 0)
- `limit` (integer, optional): Results per page (default: 10, max: 50)

**Request Example**:
```http
GET /api/v1/search/comprehensions?q=photosynthesis&difficulty=easy&skip=0&limit=10
```

**Response** (200 OK):
```json
{
    "status": "success",
    "data": {
        "query": "photosynthesis",
        "comprehensions": [
            {
                "id": 1,
                "title": "Understanding Photosynthesis",
                "content": "Photosynthesis is the process...",
                "difficulty_level": "easy",
                "quiz_count": 5,
                "relevance_score": 0.95,
                "created_at": "2024-01-15T10:30:00Z"
            }
        ],
        "total": 1,
        "skip": 0,
        "limit": 10
    },
    "message": "Search completed successfully"
}
```

### 2. Get Comprehension Statistics

Get statistics about comprehensions in the system.

**Endpoint**: `GET /api/v1/search/statistics`

**Response** (200 OK):
```json
{
    "status": "success",
    "data": {
        "total_comprehensions": 25,
        "total_quizzes": 187,
        "by_difficulty": {
            "easy": 10,
            "medium": 12,
            "hard": 3
        },
        "average_quizzes_per_comprehension": 7.48,
        "most_recent_comprehension": {
            "id": 25,
            "title": "Climate Change",
            "created_at": "2024-01-20T15:30:00Z"
        }
    },
    "message": "Statistics retrieved successfully"
}
```

## Error Handling

### Standard Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 422 | Invalid input data |
| `COMPREHENSION_NOT_FOUND` | 404 | Comprehension not found |
| `QUIZ_NOT_FOUND` | 404 | Quiz not found |
| `INVALID_QUIZ_ID` | 400 | Quiz ID doesn't belong to comprehension |
| `DATABASE_ERROR` | 500 | Database operation failed |
| `INTERNAL_SERVER_ERROR` | 500 | Unexpected server error |
| `UNAUTHORIZED` | 401 | Authentication required |
| `FORBIDDEN` | 403 | Insufficient permissions |

### Error Response Format

```json
{
    "status": "error",
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable error message",
        "details": {
            /* Optional additional error details */
        }
    }
}
```

### Example Error Responses

**Validation Error**:
```json
{
    "status": "error",
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": [
            {
                "field": "difficulty_level",
                "message": "Must be one of: easy, medium, hard",
                "received": "expert"
            },
            {
                "field": "content",
                "message": "Must be at least 50 characters long",
                "received_length": 25
            }
        ]
    }
}
```

## Data Models

### Pydantic Models for Request/Response

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class CorrectAnswer(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"

# Comprehension Models
class ComprehensionBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=255)
    content: str = Field(..., min_length=50)
    difficulty_level: DifficultyLevel

class ComprehensionCreate(ComprehensionBase):
    pass

class ComprehensionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=255)
    content: Optional[str] = Field(None, min_length=50)
    difficulty_level: Optional[DifficultyLevel] = None

class ComprehensionResponse(ComprehensionBase):
    id: int
    quiz_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Quiz Models
class QuizBase(BaseModel):
    comprehension_id: int
    question: str = Field(..., min_length=10)
    option_a: str = Field(..., min_length=1, max_length=500)
    option_b: str = Field(..., min_length=1, max_length=500)
    option_c: str = Field(..., min_length=1, max_length=500)
    option_d: str = Field(..., min_length=1, max_length=500)
    correct_answer: CorrectAnswer
    explanation: Optional[str] = None

class QuizCreate(QuizBase):
    pass

class QuizUpdate(BaseModel):
    question: Optional[str] = Field(None, min_length=10)
    option_a: Optional[str] = Field(None, min_length=1, max_length=500)
    option_b: Optional[str] = Field(None, min_length=1, max_length=500)
    option_c: Optional[str] = Field(None, min_length=1, max_length=500)
    option_d: Optional[str] = Field(None, min_length=1, max_length=500)
    correct_answer: Optional[CorrectAnswer] = None
    explanation: Optional[str] = None

class QuizResponse(QuizBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Quiz Submission Models
class QuizAnswer(BaseModel):
    quiz_id: int
    selected_answer: CorrectAnswer

class QuizSubmission(BaseModel):
    comprehension_id: int
    answers: List[QuizAnswer]

class QuizResult(BaseModel):
    quiz_id: int
    question: str
    selected_answer: str
    correct_answer: str
    is_correct: bool
    explanation: Optional[str]

class QuizSubmissionResponse(BaseModel):
    comprehension_id: int
    comprehension_title: str
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    score_percentage: float
    results: List[QuizResult]
```

## Example Code

### FastAPI Router Example

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database

router = APIRouter(prefix="/api/v1", tags=["comprehensions"])

@router.post("/comprehensions", response_model=schemas.ComprehensionResponse, status_code=status.HTTP_201_CREATED)
async def create_comprehension(
    comprehension: schemas.ComprehensionCreate,
    db: Session = Depends(database.get_db)
):
    """Create a new comprehension."""
    db_comprehension = models.Comprehension(**comprehension.dict())
    db.add(db_comprehension)
    db.commit()
    db.refresh(db_comprehension)
    return db_comprehension

@router.get("/comprehensions", response_model=List[schemas.ComprehensionResponse])
async def get_comprehensions(
    skip: int = 0,
    limit: int = 10,
    difficulty: Optional[str] = None,
    db: Session = Depends(database.get_db)
):
    """Get all comprehensions with optional filtering."""
    query = db.query(models.Comprehension)
    
    if difficulty:
        query = query.filter(models.Comprehension.difficulty_level == difficulty)
    
    comprehensions = query.offset(skip).limit(limit).all()
    return comprehensions

@router.get("/comprehensions/{comprehension_id}", response_model=schemas.ComprehensionResponse)
async def get_comprehension(
    comprehension_id: int,
    db: Session = Depends(database.get_db)
):
    """Get a specific comprehension by ID."""
    comprehension = db.query(models.Comprehension).filter(
        models.Comprehension.id == comprehension_id
    ).first()
    
    if not comprehension:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comprehension with ID {comprehension_id} not found"
        )
    
    return comprehension

@router.put("/comprehensions/{comprehension_id}", response_model=schemas.ComprehensionResponse)
async def update_comprehension(
    comprehension_id: int,
    comprehension_update: schemas.ComprehensionUpdate,
    db: Session = Depends(database.get_db)
):
    """Update a comprehension."""
    db_comprehension = db.query(models.Comprehension).filter(
        models.Comprehension.id == comprehension_id
    ).first()
    
    if not db_comprehension:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comprehension with ID {comprehension_id} not found"
        )
    
    update_data = comprehension_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_comprehension, field, value)
    
    db.commit()
    db.refresh(db_comprehension)
    return db_comprehension

@router.delete("/comprehensions/{comprehension_id}")
async def delete_comprehension(
    comprehension_id: int,
    db: Session = Depends(database.get_db)
):
    """Delete a comprehension and all associated quizzes."""
    db_comprehension = db.query(models.Comprehension).filter(
        models.Comprehension.id == comprehension_id
    ).first()
    
    if not db_comprehension:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comprehension with ID {comprehension_id} not found"
        )
    
    quiz_count = len(db_comprehension.quizzes)
    db.delete(db_comprehension)
    db.commit()
    
    return {
        "status": "success",
        "data": {
            "id": comprehension_id,
            "deleted_quiz_count": quiz_count
        },
        "message": f"Comprehension and {quiz_count} associated quizzes deleted successfully"
    }
```

### Dash Frontend Example

```python
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import requests

API_URL = "http://localhost:8000/api/v1"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Comprehension Quiz App"),
            dbc.Tabs([
                dbc.Tab(label="Admin", tab_id="admin"),
                dbc.Tab(label="User", tab_id="user"),
            ], id="tabs", active_tab="user"),
        ])
    ]),
    html.Div(id="tab-content")
])

# Callback to switch tabs
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab")
)
def switch_tab(active_tab):
    if active_tab == "admin":
        return admin_layout
    return user_layout

# User layout
user_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Input(id="search-input", placeholder="Search comprehensions...", type="text"),
            dbc.Button("Search", id="search-button", color="primary", className="mt-2"),
        ])
    ]),
    dbc.Row([
        dbc.Col(id="search-results")
    ], className="mt-3")
])

# Search callback
@app.callback(
    Output("search-results", "children"),
    Input("search-button", "n_clicks"),
    State("search-input", "value")
)
def search_comprehensions(n_clicks, search_query):
    if not n_clicks or not search_query:
        return html.P("Enter a search query and click Search")
    
    try:
        response = requests.get(f"{API_URL}/search/comprehensions", params={"q": search_query})
        if response.status_code == 200:
            data = response.json()["data"]
            comprehensions = data["comprehensions"]
            
            return [
                dbc.Card([
                    dbc.CardBody([
                        html.H4(comp["title"]),
                        html.P(comp["content"][:200] + "..."),
                        dbc.Badge(comp["difficulty_level"], color="info"),
                        dbc.Button("Take Quiz", id={"type": "take-quiz", "index": comp["id"]})
                    ])
                ]) for comp in comprehensions
            ]
        else:
            return html.P("Error searching comprehensions", className="text-danger")
    except Exception as e:
        return html.P(f"Error: {str(e)}", className="text-danger")

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
```

## Testing

### Example API Tests with pytest

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_comprehension():
    response = client.post(
        "/api/v1/comprehensions",
        json={
            "title": "Test Comprehension",
            "content": "This is a test content with more than fifty characters to meet the minimum requirement.",
            "difficulty_level": "easy"
        }
    )
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["title"] == "Test Comprehension"
    assert data["difficulty_level"] == "easy"

def test_get_comprehensions():
    response = client.get("/api/v1/comprehensions")
    assert response.status_code == 200
    data = response.json()["data"]
    assert "comprehensions" in data
    assert isinstance(data["comprehensions"], list)

def test_submit_quiz():
    response = client.post(
        "/api/v1/quizzes/submit",
        json={
            "comprehension_id": 1,
            "answers": [
                {"quiz_id": 1, "selected_answer": "B"},
                {"quiz_id": 2, "selected_answer": "C"}
            ]
        }
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert "score_percentage" in data
    assert "results" in data
```

## Rate Limiting

Consider implementing rate limiting for production:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/v1/comprehensions")
@limiter.limit("100/minute")
async def get_comprehensions(request: Request):
    # endpoint logic
    pass
```

---

*For more information, see:*
- [Architecture Documentation](./ARCHITECTURE.md)
- [Database Schema Documentation](./DATABASE_SCHEMA.md)
