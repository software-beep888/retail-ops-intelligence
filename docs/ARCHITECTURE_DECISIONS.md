# Architecture Decisions

## Why These Decisions Matter
This document explains the technical trade-offs made in this project. Each decision balances business value, implementation complexity, and demonstration of senior judgment.

## 1. Database Choice: PostgreSQL over Snowflake/BigQuery

### Decision
Use PostgreSQL in Docker for the entire data stack.

### Why
- **Data Volume**: < 1GB fits comfortably in PostgreSQL
- **Cost**: $0 vs. $2+/hour for cloud data warehouses
- **Simplicity**: Single container vs. multi-service orchestration
- **Signal**: Shows I can work with SQL databases (still 70% of analytics workloads)

### Trade-off Accepted
- No cloud-native features (auto-scaling, serverless compute)
- Manual backup management needed for production

### What Would Trigger Change
- Data volume > 10GB
- Need for real-time streaming analytics
- Team already standardized on Snowflake/BigQuery

## 2. Dashboard Framework: Streamlit over Dash/Shiny

### Decision
Use Streamlit for the dashboard interface.

### Why
- **Development Speed**: 5x faster to build initial version
- **Maintenance**: No callback hell, simpler state management
- **Business Focus**: Stakeholders care about insights, not UI engineering
- **Trade-off**: Accepting "less polished" look for faster iteration

### What We Don't Get
- Fine-grained control over UI components
- Advanced interactivity patterns
- Enterprise-grade theming

### When We'd Reconsider
- Dashboard needs complex user interactions
- Design system requirements from brand team
- Need for embedded analytics in existing web app

## 3. Data Processing: Daily Batch over Real-time Streaming

### Decision
Process data once daily via batch pipeline.

### Why
- **Business Need**: Managers review performance daily, not hourly
- **Complexity**: Batch is 10x simpler to implement and debug
- **Cost**: No need for Kafka/Flink infrastructure
- **Signal**: Shows understanding of appropriate technology selection

### Latency Accepted
- 24-hour data freshness (yesterday's data today)
- No intra-day alerts

### When We'd Add Streaming
- Need for hourly performance alerts
- Real-time inventory tracking requirements
- Promotion effectiveness monitoring during campaigns

## 4. Analytics Approach: Heuristics over ML Models

### Decision
Use business rules and heuristics instead of ML models.

### Why
- **Interpretability**: Business users need to understand "why"
- **Maintenance**: No model drift, no retraining pipelines
- **Speed**: Immediate insights without training time
- **Risk**: Fewer failure modes, easier to debug

### What We Sacrifice
- Potentially more accurate predictions
- Ability to discover complex patterns
- Personalization capabilities

### When ML Would Add Value
- Historical data > 3 years with clear patterns
- Need for demand forecasting
- Proven ROI on prediction accuracy improvements

## 5. Schema Drift Handling: Fail Fast over Auto-healing

### Decision
Pipeline stops immediately on schema drift.

### Why
- **Trust Protection**: Prevents silent data corruption
- **Ownership Enforcement**: Forces upstream teams to fix issues
- **Transparency**: Clear error messages show what broke
- **Signal**: Senior analysts prioritize data trust over convenience

### Business Impact Accepted
- Temporary unavailability of affected metrics
- Manual intervention required for fixes

### Alternative Considered and Rejected
- **Auto-healing**: Renaming columns automatically
- **Why rejected**: Masks upstream problems, reduces data trust

## 6. Testing Strategy: Minimal over Comprehensive

### Decision
Implement only 2 critical tests.

### Why
- **Focus**: Test what protects business value
- **Maintenance**: Fewer tests to maintain as code changes
- **Signal**: Tests exist to guard trust, not chase coverage metrics

### What's Tested
1. Schema drift causes immediate failure
2. Basic business rules (positive sales values)

### What's Not Tested (and Why)
- **Edge cases**: Business handles manually if they occur
- **Performance tests**: Data volume too small to matter
- **Integration tests**: Single pipeline, minimal integration points

## 7. Observability: Basic Logging over Advanced Monitoring

### Decision
Use simple file logging instead of Prometheus/Grafana.

### Why
- **Sufficiency**: Logs show pipeline success/failure
- **Simplicity**: No additional infrastructure needed
- **Signal**: Understands observability needs scale with system complexity

### What We Monitor
- Pipeline execution status
- Record counts processed
- Validation failures

### What We Don't Monitor (Yet)
- Query performance metrics
- User engagement with dashboard
- Infrastructure resource usage

## 8. Deployment: Docker Compose over Cloud Native

### Decision
Package entire system in Docker Compose.

### Why
- **Portability**: Runs anywhere Docker runs
- **Simplicity**: Single command to start everything
- **Demonstration**: Shows understanding of containerization

### Production Gaps
- No high availability
- Manual scaling required
- No cloud-specific optimizations

### Production Ready Additions Needed
1. Terraform for cloud resource provisioning
2. CI/CD pipeline for automated deployments
3. Monitoring and alerting setup

## 9. Data Generation: 6 Months over 2 Years

### Decision
Generate 6 months of synthetic data.

### Why
- **Sufficiency**: Enough to show seasonal patterns
- **Performance**: Faster generation and processing
- **Signal**: Builds only what's needed for demonstration

### What We Show
- Weekly patterns (weekend vs weekday)
- Monthly seasonality
- Promotion effects
- Stockout scenarios

### What We Don't Show (Unnecessary)
- Year-over-year comparisons
- Holiday season extremes
- Multi-year trend analysis

## 10. Error Handling: Quarantine over Complex Recovery

### Decision
Move bad files to quarantine directory.

### Why
- **Simplicity**: Easy to understand and implement
- **Safety**: Prevents bad data from entering system
- **Auditability**: Files preserved for investigation

### Production Enhancements Needed
- Automated alerts on quarantine
- Retry mechanisms with exponential backoff
- Integration with incident management tools

## Scaling Considerations

### Current Limits
- **150 stores**: Everything works as designed
- **500 stores**: Dashboard queries need optimization
- **5,000 stores**: Need aggregate tables and caching
- **50,000 stores**: Different architecture required

### Scaling Path
1. **First 500**: Query optimization, basic indexes
2. **Next 5,000**: Materialized views, query caching
3. **Beyond 5,000**: Data warehouse migration, streaming architecture

---

## Summary of Senior Judgment Signals

1. **Technology selection based on need, not trend**
2. **Explicit trade-offs documented**
3. **Failure modes considered and addressed**
4. **Scaling limits understood**
5. **Minimal viable implementation**
6. **Business value prioritized over technical cleverness**

This architecture demonstrates that I understand not just how to build systems, but more importantly, *when* and *why* to build them a certain way.