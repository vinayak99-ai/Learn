# Comprehension Reading and Quiz Application - Documentation

Welcome to the comprehensive documentation for the Comprehension Reading and Quiz Application. This documentation suite provides complete technical specifications for building a full-stack application using Python Dash, FastAPI, and SQL database.

## Documentation Overview

### 📐 [ARCHITECTURE.md](./ARCHITECTURE.md)
Complete system architecture documentation including:
- System overview and high-level architecture
- Component descriptions (Frontend, Backend, Database)
- Technology stack specifications
- Mermaid architecture diagrams showing component interactions
- Data flow sequence diagrams for key operations
- User interface design for Admin and User tabs
- Deployment and security considerations

**Key Topics**: Three-tier architecture, Dash UI, FastAPI, PostgreSQL/SQLite, Data flow, UI/UX design

### 🗄️ [DATABASE_SCHEMA.md](./DATABASE_SCHEMA.md)
Detailed database schema design and documentation:
- Entity Relationship (ER) diagrams using Mermaid
- Complete table schemas for `comprehensions` and `quizzes`
- SQLAlchemy model implementations
- One-to-many relationship documentation
- Index strategy and performance optimization
- Sample data with realistic examples
- SQL scripts for PostgreSQL and SQLite
- Alembic migration examples
- Data validation rules

**Key Topics**: Database design, ER diagrams, SQL, SQLAlchemy, Indexing, Migrations

### 🚀 [API_DESIGN.md](./API_DESIGN.md)
Comprehensive REST API endpoint documentation:
- All CRUD endpoints for comprehensions and quizzes
- Search functionality and filtering
- Quiz submission and scoring endpoints
- Pydantic data models with validation
- Example request/response payloads
- Error handling and standard error codes
- FastAPI router implementation examples
- Dash frontend integration code
- Testing examples with pytest
- Rate limiting configuration

**Key Topics**: REST API, FastAPI, Endpoints, Validation, Error handling, Testing

## Quick Start Guide

### For Developers

1. **Start with Architecture**: Read [ARCHITECTURE.md](./ARCHITECTURE.md) to understand the overall system design
2. **Review Database Schema**: Study [DATABASE_SCHEMA.md](./DATABASE_SCHEMA.md) to understand data structure
3. **Explore API Endpoints**: Reference [API_DESIGN.md](./API_DESIGN.md) for API implementation details

### For Project Managers

- **System Overview**: [ARCHITECTURE.md - System Overview](./ARCHITECTURE.md#system-overview)
- **Technology Stack**: [ARCHITECTURE.md - Technology Stack](./ARCHITECTURE.md#technology-stack)
- **User Interface Design**: [ARCHITECTURE.md - User Interface Design](./ARCHITECTURE.md#user-interface-design)

### For Database Administrators

- **Database Schema**: [DATABASE_SCHEMA.md - Table Schemas](./DATABASE_SCHEMA.md#table-schemas)
- **SQL Scripts**: [DATABASE_SCHEMA.md - SQL Scripts](./DATABASE_SCHEMA.md#sql-scripts)
- **Performance**: [DATABASE_SCHEMA.md - Performance Considerations](./DATABASE_SCHEMA.md#performance-considerations)

### For API Developers

- **Endpoint Specifications**: [API_DESIGN.md - Endpoints](./API_DESIGN.md#comprehensions-endpoints)
- **Data Models**: [API_DESIGN.md - Data Models](./API_DESIGN.md#data-models)
- **Example Code**: [API_DESIGN.md - Example Code](./API_DESIGN.md#example-code)

## Application Features

### Admin Interface
- Create, edit, and delete reading comprehensions
- Manage quiz questions with multiple choice options
- Set difficulty levels (easy, medium, hard)
- View and manage all content in data grids

### User Interface
- Search and filter comprehensions by title and difficulty
- Read comprehension passages
- Take quizzes with multiple choice questions
- View results with scores and explanations
- Learn from detailed answer explanations

## Technical Stack

### Frontend
- **Python Dash**: Reactive web application framework
- **Dash Bootstrap Components**: UI component library
- **Plotly**: Data visualization (optional)

### Backend
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation and serialization
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool

### Database
- **PostgreSQL**: Production database (recommended)
- **SQLite**: Development and testing database

## Architecture Highlights

### Three-Tier Architecture
```
┌─────────────────────┐
│  Presentation Layer │  ← Python Dash UI
│  (Client Browser)   │
└──────────┬──────────┘
           │ HTTP/JSON
┌──────────▼──────────┐
│  Application Layer  │  ← FastAPI REST API
│   (API Server)      │
└──────────┬──────────┘
           │ SQL Queries
┌──────────▼──────────┐
│    Data Layer       │  ← PostgreSQL/SQLite
│   (Database)        │
└─────────────────────┘
```

### Key Relationships
- **One Comprehension** → **Many Quizzes** (1:N relationship)
- Foreign key with CASCADE DELETE ensures data integrity
- Indexed queries for optimal performance

## Database Schema Summary

### comprehensions Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| title | VARCHAR(255) | Comprehension title |
| content | TEXT | Reading passage |
| difficulty_level | VARCHAR(20) | easy/medium/hard |
| created_at | TIMESTAMP | Creation time |
| updated_at | TIMESTAMP | Last update time |

### quizzes Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| comprehension_id | INTEGER | Foreign key to comprehensions |
| question | TEXT | Quiz question |
| option_a/b/c/d | VARCHAR(500) | Multiple choice options |
| correct_answer | VARCHAR(1) | A/B/C/D |
| explanation | TEXT | Answer explanation |
| created_at | TIMESTAMP | Creation time |
| updated_at | TIMESTAMP | Last update time |

## API Endpoints Summary

### Comprehensions
- `GET /api/v1/comprehensions` - List all comprehensions
- `GET /api/v1/comprehensions/{id}` - Get single comprehension
- `POST /api/v1/comprehensions` - Create comprehension
- `PUT /api/v1/comprehensions/{id}` - Update comprehension
- `DELETE /api/v1/comprehensions/{id}` - Delete comprehension

### Quizzes
- `GET /api/v1/quizzes?comprehension_id={id}` - Get quizzes for comprehension
- `GET /api/v1/quizzes/{id}` - Get single quiz
- `POST /api/v1/quizzes` - Create quiz
- `PUT /api/v1/quizzes/{id}` - Update quiz
- `DELETE /api/v1/quizzes/{id}` - Delete quiz
- `POST /api/v1/quizzes/submit` - Submit quiz answers

### Search
- `GET /api/v1/search/comprehensions?q={query}` - Search comprehensions
- `GET /api/v1/search/statistics` - Get system statistics

## Data Flow Examples

### Creating a Comprehension
```
Admin → Dash UI → POST /api/v1/comprehensions → FastAPI → Database
                                                         ↓
Admin ← Dash UI ← 201 Created Response ← FastAPI ← Inserted Record
```

### Taking a Quiz
```
User → Select Comprehension → GET /api/v1/comprehensions/{id}
                            → GET /api/v1/quizzes?comprehension_id={id}
                            → Display Questions
User → Submit Answers → POST /api/v1/quizzes/submit
                      → Receive Score & Explanations
```

## Development Guidelines

### Code Quality
- Follow PEP 8 style guide for Python
- Use type hints throughout the codebase
- Write comprehensive docstrings
- Implement unit and integration tests

### Security
- Validate all input data
- Use parameterized queries (via ORM)
- Implement HTTPS in production
- Add authentication/authorization
- Sanitize user-generated content

### Performance
- Use database indexing strategically
- Implement connection pooling
- Cache frequently accessed data
- Use pagination for large result sets
- Optimize SQL queries

## Next Steps

1. **Set Up Environment**: Install Python 3.9+, PostgreSQL, and dependencies
2. **Create Database**: Run SQL scripts from DATABASE_SCHEMA.md
3. **Implement Backend**: Build FastAPI endpoints following API_DESIGN.md
4. **Build Frontend**: Create Dash UI components per ARCHITECTURE.md
5. **Test Integration**: Ensure frontend-backend-database communication works
6. **Deploy**: Follow deployment guidelines in ARCHITECTURE.md

## Contributing

When contributing to this project:
1. Follow the architecture patterns documented here
2. Maintain consistency with existing code style
3. Update documentation when making changes
4. Add tests for new features
5. Ensure backward compatibility

## Support

For questions or clarifications:
- Review the appropriate documentation file
- Check the example code sections
- Refer to sequence diagrams for data flow understanding

## License

This documentation is part of the Comprehension Reading and Quiz Application project.

---

**Documentation Version**: 1.0  
**Last Updated**: January 2025  
**Status**: Complete and Ready for Implementation
