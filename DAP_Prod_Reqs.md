# Digital Asset Research Platform
## Product Requirements Document (PRD)

### Executive Summary

An AI-powered Digital Asset Research Platform that enables researchers, traders, quants, and portfolio managers to efficiently gather data, generate insights, and produce professional research reports with minimal manual effort. The platform uses LLMs and autonomous agents to create an end-to-end agentic research experience where humans validate and approve AI-generated outputs.

---

## 1. Target Users & Priorities

### User Personas (Priority Order)
| Priority | User Type | Primary Needs |
|----------|-----------|---------------|
| 1 | Researchers | Gather data, analyze, provide supporting evidence, write opinions |
| 2 | Traders | Market insights, quick data access, trading signals |
| 3 | Quants | Metrics, quantitative analysis, algorithmic insights |
| 4 | Portfolio Managers | Portfolio summaries, performance reports, rebalancing recommendations |
| 5 | Product Positioning Teams | Market intelligence, competitor analysis |

### Core Pain Points to Solve
- **Data Gathering**: Consolidating data from multiple sources is time-consuming
- **Sense-Making**: Processing large volumes of data to extract meaningful insights
- **Opinion Formation**: Producing well-formed, evidence-backed research opinions
- **Report Production**: Manual report creation is labor-intensive

### Access Control
- Role-based access control (RBAC)
- User segmentation and entitlements (future enhancement)

---

## 2. Data Sources & Integration

### External Data Providers

| Category | Providers | Data Types |
|----------|-----------|------------|
| **Blockchain Data** | Allium, Flipside, Dune | On-chain metrics, protocol analytics, real-time rankings |
| **Market Data** | CoinGecko, Kaiko, Lukka | Prices, volumes, market cap, trading data |
| **News Data** | Messari | Market news, regulatory updates, industry developments |

### Internal Data Sources
- Portfolio holdings and allocations
- Trading history and performance
- Internally generated market information
- Historical research and opinions

### Research Coverage
- **Total Assets**: 500 research assets
- **Active Focus**: 
  - Top 20 blockchains
  - Top 20 protocols
  - Select infrastructure assets

### Data Presentation
- Interactive dashboards for data visualization
- Unified view across all data sources
- Real-time and historical data access

---

## 3. AI/Agent Architecture

### Agent Autonomy Model

| Autonomy Level | Use Cases | Human Involvement |
|----------------|-----------|-------------------|
| **Full Autonomy** | Data gathering, routine monitoring, metric calculations, data normalization, alert detection | None - fully automated |
| **Semi-Autonomous** | Draft report generation, alert creation, market summaries, trend identification, sentiment analysis | Review optional |
| **Human-in-the-Loop** | Final report approval, publishing, critical decisions, rebalancing recommendations, investment thesis | Mandatory approval |

### LLM Infrastructure
- **Available Models**: OpenAI (GPT-4, GPT-3.5), Claude (Opus, Sonnet, Haiku), Gemini (Ultra, Pro)
- **Selection Criteria**: Task complexity, response time requirements, cost optimization, context length needs
- **Model Usage Guidelines**:
  - **Premium Models** (GPT-4, Claude Opus, Gemini Ultra): Complex analysis, long-form reports, strategic decisions
  - **Standard Models** (GPT-3.5, Claude Sonnet, Gemini Pro): Daily reports, query responses, routine analysis
  - **Fast Models** (GPT-4 Turbo, Claude Haiku): Real-time alerts, classification, entity extraction

### Agent Capabilities

#### 1. Data Aggregation Agent
**Primary Functions**: Pull and normalize data from all sources
- Multi-source data reconciliation and conflict resolution
- Unstructured data extraction (news, regulatory documents)
- API response interpretation and transformation
- Data quality validation and anomaly flagging
- Automated data pipeline orchestration

#### 2. Analysis Agent
**Primary Functions**: Process data, identify patterns, generate insights
- Trend identification and correlation analysis
- Comparative analysis across protocols and assets
- Anomaly detection with contextual explanations
- Sentiment analysis at scale (news, social media)
- Pattern recognition in on-chain data
- Statistical analysis and forecasting

#### 3. Report Drafting Agent
**Primary Functions**: Auto-generate report content with proper formatting
- Daily market briefs with narrative synthesis
- Weekly snapshots with trend analysis
- Monthly comprehensive reports
- Protocol deep dive research
- Regulatory update summaries
- Portfolio performance reports with attribution analysis
- Maintains consistent voice and style across all reports

#### 4. Monitoring Agent
**Primary Functions**: Track markets, protocols, and assets for significant changes
- Real-time price and volume monitoring
- On-chain activity tracking (whale movements, smart contract events)
- Protocol governance and upgrade monitoring
- Regulatory news surveillance
- Social sentiment tracking
- Technical indicator monitoring (support/resistance levels, momentum)

#### 5. Alert Agent
**Primary Functions**: Generate proactive notifications based on triggers
- Price movement alerts with causal analysis
- Smart contract risk alerts
- Regulatory compliance notifications
- Portfolio threshold breach alerts
- Market regime change detection
- Opportunity identification (arbitrage, undervaluation)

#### 6. Conversational Research Agent (New)
**Primary Functions**: Natural language interface for data queries and analysis
- Complex multi-dimensional queries
- Historical research reference and synthesis
- Ad-hoc report generation through conversation
- Portfolio analysis and what-if scenarios
- Research collaboration and knowledge discovery

#### 7. Rebalancing Agent (New)
**Primary Functions**: Portfolio optimization and trade recommendations
- Deviation analysis (current vs. target allocations)
- Trade recommendation generation with rationale
- Transaction cost and market impact estimation
- Execution strategy planning
- Risk assessment post-rebalancing

### LLM Use Case Examples by Agent

**Detailed use case scenarios, example prompts, and implementation patterns are documented in:**
[LLM_Use_Cases_Research_Platform.md](./LLM_Use_Cases_Research_Platform.md)

**Key Use Case Categories**:
1. **Data Operations**: Aggregation, normalization, quality assurance
2. **Market Intelligence**: Analysis, insights, trend identification
3. **Report Automation**: Brief to comprehensive report generation
4. **Interactive Research**: Conversational queries, ad-hoc analysis
5. **Portfolio Management**: Performance analysis, rebalancing, risk assessment
6. **Monitoring & Alerts**: Event detection, contextual notifications
7. **Knowledge Management**: Research synthesis, consistency checking

### Trigger Mechanisms

| Trigger Type | Frequency | Examples |
|--------------|-----------|----------|
| **Scheduled - Daily** | Every day | Daily market briefs |
| **Scheduled - Weekly** | Every week | Weekly snapshots |
| **Event-Driven** | Real-time | Price movements, regulatory news, protocol updates |
| **On-Demand** | User-initiated | Ad-hoc research queries |

---

## 4. Report Types & Generation

### Report Portfolio

| Report Type | Frequency | Content |
|-------------|-----------|---------|
| **Daily Market Briefs** | Daily | Market overview, key movements, notable events |
| **Weekly Snapshots** | Weekly | Week summary, trends, outlook |
| **Monthly Wraps** | Monthly | Comprehensive monthly analysis |
| **Portfolio Summaries** | On-demand | Holdings, allocations, exposure |
| **Portfolio Performance** | Periodic | Returns, attribution, benchmarking |
| **Regulatory Updates** | Event-triggered | New regulations, compliance implications |
| **Rebalancing Reports** | As needed | Rebalancing recommendations with rationale |

### Report Generation Pipeline
1. **Data Collection**: Agents gather relevant data from all sources
2. **Analysis**: AI processes data and generates insights
3. **Drafting**: Auto-generate report content
4. **Layout**: Automated PDF layout using Aspose (no human intervention)
5. **Review**: Human review and annotations
6. **Approval**: Mandatory approval workflow before publishing
7. **Distribution**: Email links with corporate branding

### PDF Generation
- **Technology**: Aspose PDF
- **Layout**: Fully automated, template-driven
- **Branding**: Corporate branding applied automatically

---

## 5. Conversational AI Interface

### Chat Capabilities
- **Natural Language Queries**: Ask questions in plain English against all platform data
- **Context-Aware Responses**: System maintains conversation context for follow-up questions
- **Report Generation**: Create custom reports through conversational interactions
- **Multi-Step Analysis**: Complex queries broken down into logical steps automatically
- **Data Exploration**: Drill down into specific metrics or protocols interactively
- **Historical Research**: Query past reports and analysis with semantic search
- **What-If Scenarios**: Explore hypothetical portfolio changes and their impacts

### Query Examples by Complexity

**Simple Data Queries**:
- "What's the TVL trend for Uniswap over the last 30 days?"
- "Show me today's top gainers and losers"
- "What's our current DeFi allocation?"

**Analysis Queries**:
- "Compare Ethereum and Solana fee generation over Q4 2025"
- "Analyze correlation between BTC price and our portfolio returns"
- "Identify protocols with growing TVL but declining user counts"

**Report Generation Queries**:
- "Generate a market brief for today focusing on DeFi protocols"
- "Create a deep dive on Arbitrum including technical analysis and competitive positioning"
- "Draft a regulatory update on the recent SEC announcement"

**Portfolio Management Queries**:
- "Compare our portfolio performance against BTC this quarter"
- "Suggest rebalancing if we're significantly over/under allocated in any sector"
- "What would be the impact of reducing our SOL position by 20%?"

**Historical Research Queries**:
- "What regulatory changes affected our holdings this month?"
- "What did we say about Ethereum scalability in Q3 2025?"
- "Show me our historical stance on Layer 2 protocols"

**Complex Multi-Step Queries**:
- "Identify undervalued protocols in the DeFi lending space, analyze their fundamentals, and recommend if we should increase exposure"
- "Track all governance proposals from our portfolio holdings this week and assess which require our attention"

### Data Context & Retrieval

**Available Context Sources**:
- Real-time market data (prices, volumes, market caps)
- On-chain metrics from all integrated data providers
- Historical reports and research (full-text searchable)
- Portfolio holdings and transaction history
- News and regulatory updates
- Protocol documentation and technical specs

**Retrieval-Augmented Generation (RAG)**:
- Vector database stores embeddings of all historical research
- Semantic search retrieves relevant context for queries
- LLM synthesizes retrieved information with current data
- Citations provided for all information sources

**Context Management**:
- Conversation history maintained across sessions
- Ability to reference previous queries and responses
- Smart context window management for long conversations
- Option to start fresh context for new topics

### Response Features

**Structured Outputs**:
- Tables for comparative data
- Bullet points for key insights
- Charts and visualization recommendations
- Citation links to source data and reports

**Interactive Elements**:
- Suggested follow-up questions
- Deep dive options for any mentioned protocol/asset
- Quick actions (e.g., "Generate full report on this topic")
- Export conversation as report

**Quality Indicators**:
- Confidence levels for analysis and predictions
- Data freshness indicators (last updated timestamp)
- Source attribution for all claims
- Uncertainty acknowledgment when data is incomplete

### Advanced Capabilities

**Agent Orchestration**:
- Complex queries automatically routed to appropriate specialized agents
- Parallel execution of independent sub-queries for faster response
- Results synthesized into coherent narrative

**Learning & Personalization**:
- System learns user preferences and query patterns
- Personalized query suggestions based on role and history
- Frequently asked questions surfaced proactively

**Integration with Workflows**:
- Convert conversation into report draft with one click
- Schedule recurring queries (e.g., weekly DeFi summary)
- Set up alerts based on conversational criteria

### Example Conversation Flow

```
User: "How is our DeFi exposure performing?"

System: "Your DeFi allocation is currently 32% of portfolio ($8.4M), up from 
28% last quarter. Performance highlights:
- QTD Return: +18.2% vs. portfolio average of +12.4%
- Top performers: Uniswap (+34%), Aave (+28%)
- Underperformers: Curve (+3%), MakerDAO (+5%)
Overall, DeFi outperforming portfolio by +5.8pp. [View Details]"

User: "Is 32% too high compared to market benchmarks?"

System: "Your 32% DeFi allocation is +7pp above the DeFi Pulse Index benchmark 
(25%). This represents moderate overallocation. Analysis:
- Market trend: DeFi share of crypto market declining from 30% to 25% over past 6 months
- Risk: Concentration risk in DeFi protocols
- Recommendation: Consider reducing exposure to target 25-28% range
Would you like me to generate rebalancing recommendations? [Yes/No]"

User: "Yes, suggest specific trades"

System: [Generates rebalancing report with specific buy/sell recommendations]
"Rebalancing strategy to achieve 28% DeFi allocation:
1. Reduce Curve position by $800K (current premium valuation)
2. Reduce Aave position by $600K (target allocation reached)
3. Reallocate $1.4M to: BTC (+$700K), ETH (+500K), SOL (+200K)

Expected outcomes:
- DeFi allocation: 28% (target range)
- Reduced concentration risk
- Estimated transaction costs: $14K (1% of trades)
- Improved risk-adjusted returns (projected)

[Generate Full Rebalancing Report] [Save Recommendations]"
```

**For detailed implementation patterns and examples, see:**
[LLM_Use_Cases_Research_Platform.md](./LLM_Use_Cases_Research_Platform.md) - Section 4

---

## 6. Collaboration & Workflow

### Version Control
- All research documents version-controlled
- Change history and audit trail
- Ability to revert to previous versions

### Annotations & Comments
- Inline comments on research content
- Threaded discussions
- Mention/notify team members

### Approval Workflow
- **Mandatory before publishing**
- Configurable approval chains
- Approval status tracking
- Rejection with feedback capability

### Research Team Context
- Small team currently
- No multi-user simultaneous collaboration required initially
- Focus on sequential review and approval

---

## 7. Client Portal & Distribution

### Client Access
- Dedicated portal for clients
- Access to published reports
- Historical report archive
- Search and filter capabilities

### Distribution Mechanism
- Email distribution with branded links
- Direct portal access
- Notification of new reports

### User Management
- User segmentation (future enhancement)
- Entitlement management (future enhancement)
- Access logging and analytics

---

## 8. Search & Knowledge Management

### Search Capabilities
- Full-text search across all research
- Filter by:
  - Asset
  - Blockchain
  - Protocol
  - Date range
  - Author
  - Report type

### Research Reusability
- Past research searchable and accessible
- Reference previous opinions and analysis
- Build on existing research

### Knowledge Base
- Centralized research repository
- Tagged and categorized content
- Linkable research artifacts

---

## 9. Notifications & Alerts

### Notification Channels
- **Desktop Application**: Push notifications
- **Web Application**: In-app notifications
- **No mobile notifications**

### Alert Types
- Market event alerts
- Protocol change notifications
- Report ready for review
- Approval required
- New research published

### Proactive Monitoring
- AI-driven anomaly detection
- Threshold-based alerts
- Custom alert configuration

---

## 10. Platform Architecture

### Deployment
- **Hosting**: Cloud-hosted
- **Type**: Standalone platform (no external integrations)
- **Compliance**: Internal controls (SOC 2/GDPR handled internally)

### Application Type
- **Single Page Application (SPA)** - Web-based
- **Desktop Application** - Native desktop experience
- **No mobile application**

### Technical Stack Recommendations
- **Frontend**: React/Vue.js SPA
- **Backend**: Python/Node.js microservices
- **Database**: PostgreSQL + Vector DB for embeddings
- **Message Queue**: Redis/RabbitMQ for event processing
- **PDF Generation**: Aspose
- **LLM Integration**: OpenAI, Claude, Gemini APIs

---

## 11. Success Metrics

### Primary Metrics
| Metric | Description | Target |
|--------|-------------|--------|
| **Time Saved** | Reduction in research and report generation time | Significant improvement |
| **Usability Score** | User satisfaction with platform | High adoption rate |

### Secondary Metrics
- Number of reports generated
- Agent automation rate
- Query response accuracy
- User engagement frequency

---

## 12. Implementation Priorities

### Phase 1: Foundation
- Data source integrations
- Basic agent framework
- Report generation pipeline
- User authentication and RBAC

### Phase 2: Intelligence
- Full LLM integration
- Conversational interface
- Automated report drafting
- Event-triggered monitoring

### Phase 3: Polish
- Client portal
- Advanced search
- Notification system
- Dashboard enhancements

### Phase 4: Scale
- User segmentation
- Entitlement management
- Advanced collaboration
- Performance optimization

---

## 13. Timeline & Quality

- **No hard deadlines**
- **Focus on quality over speed**
- **Iterative delivery with continuous feedback**

---

## 14. Appendix

### Glossary
- **TVL**: Total Value Locked
- **DeFi**: Decentralized Finance
- **Protocol**: Blockchain-based application or system
- **Rebalancing**: Adjusting portfolio allocations

### Document History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-24 | Product Team | Initial PRD |

---

**END OF DOCUMENT**
