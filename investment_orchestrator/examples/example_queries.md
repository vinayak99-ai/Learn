# Example Queries for Investment Research Orchestrator

This document provides comprehensive examples of natural language queries you can use with the Investment Research Orchestrator.

## Simple Price Queries

### 1. Current Price Lookup
**Query**: "What's the current price of Apple?"

**Expected Flow**:
- Agent calls `GetAssetPrice` tool with "AAPL"
- Returns current price and price change

**Expected Output**:
```
Apple (AAPL) is currently trading at $150.25, up 1.18% from yesterday's close of $148.50. 
The trading volume is 45,678,900 shares. Last updated: 2024-01-29T15:30:00Z
```

### 2. Multiple Asset Prices
**Query**: "Show me the prices for Apple, Microsoft, and Google"

**Expected Flow**:
- Agent calls `GetAssetPrice` for AAPL, MSFT, GOOGL
- Consolidates results

**Expected Output**:
```
Current prices:
- Apple (AAPL): $150.25 (+1.18%)
- Microsoft (MSFT): $380.50 (+2.34%)
- Google (GOOGL): $142.80 (-0.45%)
```

## Classification Queries

### 3. Sector Information
**Query**: "What sector does Tesla belong to?"

**Expected Flow**:
- Agent calls `GetAssetClassification` for TSLA
- Returns sector and industry information

**Expected Output**:
```
Tesla (TSLA) belongs to:
- Sector: Consumer Discretionary
- Industry: Automobiles
- Market Cap: Large Cap
- Geography: United States
- Asset Type: Common Stock
```

### 4. Industry Comparison
**Query**: "Are Apple and Microsoft in the same industry?"

**Expected Flow**:
- Agent calls `GetAssetClassification` for both AAPL and MSFT
- Compares industry classifications

**Expected Output**:
```
Apple and Microsoft are both in the Technology sector, but in different industries:
- Apple: Consumer Electronics
- Microsoft: Software

However, they both compete in overlapping markets like cloud computing and enterprise software.
```

## Screening Queries

### 5. High-Growth Tech Stocks
**Query**: "Find me high-growth tech stocks under $100"

**Expected Flow**:
- Agent calls `ScreenAssets` with criteria: sector="Technology", priceRange="<100", minGrowth=20
- Returns enriched list of candidates

**Expected Output**:
```
Based on screening 50+ tech stocks, here are 5 high-growth options under $100:

1. Stock A ($87.50)
   Growth: 45% YoY | P/E: 28 | Rating: Strong Buy
   Sector: Technology | Industry: Software

2. Stock B ($62.30)
   Growth: 38% YoY | P/E: 22 | Rating: Buy
   Sector: Technology | Industry: Semiconductors

3. Stock C ($94.00)
   Growth: 35% YoY | P/E: 19 | Rating: Buy
   Sector: Technology | Industry: Cloud Services

All three show strong fundamentals with revenue growth exceeding 35% and positive analyst sentiment.
```

### 6. Value Stocks in Energy
**Query**: "Find large-cap energy stocks with PE ratio under 15"

**Expected Flow**:
- Agent calls `ScreenAssets` with sector="Energy", marketCap="Large", maxPeRatio=15
- Returns matching assets with fundamentals

**Expected Output**:
```
Found 8 large-cap energy stocks with P/E under 15:

1. XOM (Exxon Mobil) - P/E: 12.5, Market Cap: Large Cap
   Price: $105.30 | Growth: 15% | Rating: Buy

2. CVX (Chevron) - P/E: 11.8, Market Cap: Large Cap
   Price: $158.20 | Growth: 12% | Rating: Hold

3. COP (ConocoPhillips) - P/E: 14.2, Market Cap: Large Cap
   Price: $125.50 | Growth: 18% | Rating: Strong Buy

These stocks offer attractive valuations with P/E ratios below market average.
```

### 7. Dividend Aristocrats
**Query**: "Show me stocks with consistent dividends and low volatility"

**Expected Flow**:
- Agent calls `GetAssetBaskets` with dividend and volatility criteria
- Fetches research data for top matches

**Expected Output**:
```
Here are 5 dividend aristocrats with low volatility:

1. JNJ (Johnson & Johnson)
   Dividend Yield: 3.2% | Beta: 0.65 | Years of increases: 60
   
2. PG (Procter & Gamble)
   Dividend Yield: 2.8% | Beta: 0.58 | Years of increases: 67

3. KO (Coca-Cola)
   Dividend Yield: 3.1% | Beta: 0.62 | Years of increases: 61

These stocks have demonstrated consistent dividend growth and stability.
```

## Comparison Queries

### 8. Direct Comparison
**Query**: "Should I buy Tesla or Rivian?"

**Expected Flow**:
- Agent calls `CompareAssets` with ["TSLA", "RIVN"]
- Analyzes fundamentals, growth, and ratings
- Provides recommendation with reasoning

**Expected Output**:
```
Comparison of Tesla (TSLA) vs Rivian (RIVN):

Tesla (TSLA):
- Price: $245.80 (+2.1%)
- Market Cap: Large Cap ($780B)
- P/E Ratio: 68.5
- Revenue Growth: 25%
- Analyst Rating: Hold
- Profitable: Yes

Rivian (RIVN):
- Price: $18.50 (-1.5%)
- Market Cap: Mid Cap ($18B)
- P/E Ratio: N/A (not profitable)
- Revenue Growth: 185%
- Analyst Rating: Buy
- Profitable: No

Analysis:
Tesla is the more established player with proven profitability and scale. Rivian shows 
higher growth but carries more risk as it's still in growth/investment phase. 

For conservative investors: Tesla offers stability
For growth-focused investors: Rivian offers higher upside potential but with more risk
```

### 9. Semiconductor Showdown
**Query**: "Compare NVDA, AMD, and INTC"

**Expected Flow**:
- Agent calls `CompareAssets` with ["NVDA", "AMD", "INTC"]
- Provides side-by-side analysis

**Expected Output**:
```
Comparison of 3 Semiconductor Leaders:

NVIDIA (NVDA):
  Price: $485.20 (+3.5%)
  Market Cap: Large Cap
  P/E: 75.2 | Growth: 95% | Rating: Strong Buy
  Focus: AI chips, data center GPUs

AMD (AMD):
  Price: $175.30 (+2.8%)
  Market Cap: Large Cap  
  P/E: 42.8 | Growth: 48% | Rating: Buy
  Focus: CPUs, GPUs, data center

Intel (INTC):
  Price: $42.10 (-0.5%)
  Market Cap: Large Cap
  P/E: 15.5 | Growth: 12% | Rating: Hold
  Focus: CPUs, foundry services

Winner by Category:
- Growth: NVDA (95% revenue growth)
- Value: INTC (lowest P/E at 15.5)
- Balanced: AMD (good growth at reasonable valuation)
```

## Complex Multi-Step Queries

### 10. Portfolio Construction
**Query**: "Build me a diversified portfolio of 5 stocks across different sectors"

**Expected Flow**:
- Agent screens multiple sectors
- Selects top performer from each sector
- Provides diversification rationale

**Expected Output**:
```
Here's a diversified 5-stock portfolio:

1. Technology: AAPL (Apple) - $150.25
   - Reason: Market leader, strong fundamentals, 28% weight
   
2. Healthcare: JNJ (Johnson & Johnson) - $162.50
   - Reason: Defensive, dividend aristocrat, 20% weight
   
3. Finance: JPM (JPMorgan Chase) - $175.30
   - Reason: Banking leader, solid growth, 18% weight
   
4. Consumer: AMZN (Amazon) - $178.90
   - Reason: E-commerce + cloud, growth potential, 22% weight
   
5. Energy: XOM (Exxon Mobil) - $105.30
   - Reason: Value play, commodity exposure, 12% weight

Portfolio Characteristics:
- Sector Diversification: ✓ (5 different sectors)
- Market Cap: 100% Large Cap (lower risk)
- Average P/E: 24.5 (reasonable valuation)
- Dividend Yield: 2.1% (income component)

This portfolio balances growth (AAPL, AMZN) with value (XOM) and stability (JNJ, JPM).
```

### 11. Value + Growth Combination
**Query**: "What tech stocks are trading below their sector average PE but growing faster than 25%?"

**Expected Flow**:
- Agent screens tech sector for low P/E
- Filters for high growth rate
- Fetches detailed research data

**Expected Output**:
```
Found 3 tech stocks with below-average P/E but high growth:

Sector Average P/E: 32.5

1. STOCK_X ($85.40)
   P/E: 22.5 (31% below average) | Growth: 42% YoY
   Rating: Strong Buy | Target: $105
   Why undervalued: Recent selloff despite strong fundamentals

2. STOCK_Y ($124.80)
   P/E: 28.0 (14% below average) | Growth: 38% YoY
   Rating: Buy | Target: $145
   Why undervalued: Market hasn't priced in new product cycle

3. STOCK_Z ($67.20)
   P/E: 25.5 (22% below average) | Growth: 31% YoY
   Rating: Buy | Target: $82
   Why undervalued: Execution concerns now resolved

These stocks offer the rare combination of value pricing with growth momentum.
```

### 12. Risk Assessment Query
**Query**: "What are the top 3 healthcare stocks by analyst rating and what are their risks?"

**Expected Flow**:
- Agent screens healthcare sector
- Sorts by analyst rating
- Fetches research data including risk factors

**Expected Output**:
```
Top 3 Healthcare Stocks by Analyst Rating:

1. LLY (Eli Lilly) - Strong Buy
   Price: $625.40 | P/E: 45.2 | Growth: 28%
   Risk Factors:
   - Drug patent expirations in 2026-2027
   - High valuation relative to peers
   - Regulatory approval risks for pipeline drugs

2. UNH (UnitedHealth Group) - Strong Buy
   Price: $512.30 | P/E: 24.8 | Growth: 18%
   Risk Factors:
   - Healthcare policy changes
   - Medicare Advantage margin pressure
   - Regulatory scrutiny increasing

3. JNJ (Johnson & Johnson) - Buy
   Price: $162.50 | P/E: 18.5 | Growth: 12%
   Risk Factors:
   - Litigation liabilities (talc lawsuits)
   - Generic drug competition
   - Foreign exchange headwinds

Recommendation: LLY and UNH offer higher growth but carry more risk. JNJ is the 
most defensive choice with lower growth but more stability.
```

## Research & Analysis Queries

### 13. Fundamental Analysis
**Query**: "What are the fundamentals of Nvidia?"

**Expected Flow**:
- Agent calls `GetAssetResearchData` for NVDA
- Formats comprehensive fundamental analysis

**Expected Output**:
```
Nvidia (NVDA) Fundamental Analysis:

Valuation Metrics:
- P/E Ratio: 75.2 (premium to sector average of 32.5)
- Price: $485.20
- Market Cap: Large Cap

Financial Performance:
- Revenue Growth: 95% YoY (exceptional)
- Profit Margin: 53.2% (industry-leading)

Analyst Sentiment:
- Consensus Rating: Strong Buy
- Analyst Count: 42 analysts covering
- Target Price: $550.00 (13% upside)

Risk Factors:
- Concentrated customer base in data center
- Competition from AMD and custom chips
- High valuation leaves little room for disappointment
- Export restrictions to China

Overall Assessment: Strong fundamentals justify premium valuation. Leading 
position in AI chips provides significant growth runway.
```

### 14. Market Timing Query
**Query**: "Is now a good time to buy tech stocks?"

**Expected Flow**:
- Agent screens tech sector
- Analyzes current valuations vs historical
- Considers analyst ratings and momentum

**Expected Output**:
```
Tech Sector Analysis:

Current Valuation:
- Average P/E: 32.5
- Historical Average: 28.0
- Assessment: Slightly elevated (16% above average)

Momentum Indicators:
- 75% of tech stocks above 50-day MA (positive)
- Average YoY gain: 28% (strong)
- Analyst ratings: 65% Buy or Strong Buy

Top Opportunities:
1. Stocks with <30 P/E and >25% growth
2. Cloud computing leaders
3. Cybersecurity companies

Risks to Consider:
- Interest rate sensitivity
- High valuations limit upside
- Potential regulatory headwinds

Verdict: Selective opportunities exist, but avoid overpaying. Focus on stocks 
with strong fundamentals trading at reasonable valuations (P/E < 30, PEG < 1.5).
```

## Usage Tips

### Best Practices

1. **Be Specific**: Instead of "good stocks", ask "high-growth tech stocks under $100"
2. **Multiple Criteria**: Combine filters for better results
3. **Context Matters**: Provide timeframes and risk tolerance
4. **Follow-up**: Ask clarifying questions based on initial results

### Query Patterns

**Pattern 1 - Screen + Analyze**:
```
1. "Find tech stocks with P/E under 25"
2. "Now show me research data for the top 3"
```

**Pattern 2 - Compare + Decide**:
```
1. "Compare AAPL and MSFT"
2. "Which one is better for long-term growth?"
```

**Pattern 3 - Build + Validate**:
```
1. "Build a portfolio across 5 sectors"
2. "What are the risks in this portfolio?"
```

## API Usage Examples

### Using curl

```bash
# Simple query
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the price of Apple?"}'

# Comparison
curl -X POST http://localhost:8000/compare \
  -H "Content-Type: application/json" \
  -d '{"asset_ids": ["AAPL", "MSFT", "GOOGL"]}'

# Screening
curl -X POST http://localhost:8000/screen \
  -H "Content-Type: application/json" \
  -d '{
    "sector": "Technology",
    "market_cap": "Large",
    "price_range": "<100",
    "min_growth": 20,
    "limit": 10
  }'
```

### Using Python

```python
import requests

# Research query
response = requests.post(
    "http://localhost:8000/research",
    json={"query": "Find me high-growth tech stocks"}
)
print(response.json()["answer"])

# Comparison
response = requests.post(
    "http://localhost:8000/compare",
    json={"asset_ids": ["AAPL", "MSFT"]}
)
print(response.json()["comparison"])
```

### Using JavaScript

```javascript
// Research query
fetch('http://localhost:8000/research', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    query: 'What is the current price of Apple?' 
  })
})
.then(response => response.json())
.then(data => console.log(data.answer));
```

## Expected Response Times

- Simple queries (1 asset): 2-4 seconds
- Comparison (3 assets): 4-6 seconds
- Screening (10 assets): 6-10 seconds
- Complex multi-step: 10-15 seconds

*Note: Times vary based on backend performance and OpenAI API latency*
