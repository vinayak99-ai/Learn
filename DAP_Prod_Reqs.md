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
| **Full Autonomy** | Data gathering, routine monitoring, metric calculations | None - fully automated |
| **Semi-Autonomous** | Draft report generation, alert creation, market summaries | Review optional |
| **Human-in-the-Loop** | Final report approval, publishing, critical decisions | Mandatory approval |

### LLM Infrastructure
- **Available Models**: OpenAI, Claude, Gemini
- **Selection Criteria**: Task-appropriate model selection based on capability requirements

### Agent Capabilities
1. **Data Aggregation Agent**: Pull and normalize data from all sources
2. **Analysis Agent**: Process data, identify patterns, generate insights
3. **Report Drafting Agent**: Auto-generate report content with proper formatting
4. **Monitoring Agent**: Track markets, protocols, and assets for significant changes
5. **Alert Agent**: Generate proactive notifications based on triggers

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
- Natural language queries against internal data
- Context-aware responses using platform data
- Report generation through conversation
- Follow-up questions and refinements

### Query Examples
- "What's the TVL trend for Uniswap over the last 30 days?"
- "Generate a market brief for today focusing on DeFi protocols"
- "Compare our portfolio performance against BTC this quarter"
- "What regulatory changes affected our holdings this month?"

### Data Context
- All integrated data sources available as context
- Historical research accessible for reference
- Portfolio and trading data queryable

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
