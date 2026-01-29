# Java Backend Reference Implementation

This directory contains reference implementations for the Java backend APIs that the Python Investment Orchestrator integrates with.

## Files

### AssetDataController.java
Spring Boot REST controller that defines the API endpoints for:
- `POST /api/getAssetPrice` - Get current price and trading data
- `POST /api/getAssetClassification` - Get sector and industry classification
- `POST /api/getAssetBaskets` - Search for assets matching criteria
- `POST /api/getAssetResearchData` - Get fundamentals and analyst ratings

### DTOs.java
Data Transfer Objects (DTOs) for all request and response types:

**Request DTOs:**
- `AssetPriceRequest`
- `AssetClassificationRequest`
- `AssetBasketRequest` (with nested `Criteria` class)
- `AssetResearchRequest`

**Response DTOs:**
- `AssetPriceResponse` - price, volume, change percent
- `AssetClassificationResponse` - sector, industry, market cap
- `AssetBasketResponse` - list of matching asset IDs
- `AssetResearchResponse` - fundamentals, ratings, risk factors

## Integration Notes

### Expected API Contract

The Python orchestrator expects these endpoints to be available at:
```
{JAVA_BACKEND_URL}/api/{endpoint}
```

For example, if `JAVA_BACKEND_URL=http://localhost:8080`, the price endpoint would be:
```
http://localhost:8080/api/getAssetPrice
```

### Request Format

All endpoints expect POST requests with JSON body:
```json
{
  "assetId": "AAPL"
}
```

For basket searches:
```json
{
  "criteria": {
    "sector": "Technology",
    "marketCap": "Large",
    "priceRange": "<100",
    "minGrowth": 20
  }
}
```

### Response Format

Responses should be JSON objects matching the DTO structure. Example:
```json
{
  "assetId": "AAPL",
  "currentPrice": 150.25,
  "previousClose": 148.50,
  "changePercent": 1.18,
  "volume": 45678900,
  "lastUpdated": "2024-01-29T15:30:00Z"
}
```

## Implementation Guide

### Spring Boot Setup

1. **Add dependencies to pom.xml or build.gradle**:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

2. **Create the controller and DTOs** using the reference files provided

3. **Implement the business logic** to fetch real data from your data sources

4. **Configure CORS** to allow requests from the Python orchestrator:
```java
@CrossOrigin(origins = "*")  // Or specify your orchestrator URL
```

### Data Sources

The controller should integrate with:
- Market data providers (for prices)
- Financial databases (for fundamentals)
- Analyst rating services
- Internal classification systems

### Error Handling

Implement proper error handling:
```java
@ExceptionHandler(ResourceNotFoundException.class)
public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
    return ResponseEntity.status(HttpStatus.NOT_FOUND)
        .body(new ErrorResponse(ex.getMessage()));
}
```

### Testing

Test endpoints with curl:
```bash
curl -X POST http://localhost:8080/api/getAssetPrice \
  -H "Content-Type: application/json" \
  -d '{"assetId": "AAPL"}'
```

## Alternative: Mock Server

For development and testing, you can create a mock server that returns sample data. See the reference implementation for example response structures.

### Using WireMock

```java
@Test
public void testMockEndpoints() {
    stubFor(post(urlEqualTo("/api/getAssetPrice"))
        .willReturn(aResponse()
            .withHeader("Content-Type", "application/json")
            .withBody(samplePriceResponse)));
}
```

## Security Considerations

1. **Authentication**: Implement API authentication (JWT, OAuth2)
2. **Rate Limiting**: Prevent abuse with rate limiting
3. **Input Validation**: Validate all input parameters
4. **HTTPS**: Use HTTPS in production
5. **CORS**: Configure appropriate CORS policies

## Performance Optimization

1. **Caching**: Implement caching for frequently accessed data
2. **Database Indexing**: Index commonly queried fields
3. **Connection Pooling**: Use database connection pooling
4. **Async Processing**: Consider async processing for heavy operations

## Monitoring

Monitor these metrics:
- Request rate and latency
- Error rates by endpoint
- Database query performance
- Cache hit ratios

## Support

For questions about the Python orchestrator integration, see the main [README.md](../README.md).
