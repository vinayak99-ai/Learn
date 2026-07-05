# Key Things an Engineering Manager Running Large Financial-Firm Programs Should Take Care Of

Context: this is for an EM/engineering leader responsible for large programs (multiple teams, multi-quarter roadmaps) building financial products — payments, trading, lending, banking infra, risk/compliance systems — inside or for a financial firm.

## 1. Regulatory and compliance context is non-negotiable
- Know which regulations apply to your program (e.g. PCI-DSS for card data, SOX for financial reporting controls, GDPR/CCPA for personal data, KYC/AML requirements, region-specific banking regulations) — this shapes architecture, not just paperwork.
- Build compliance and audit requirements into the plan from day one, not as a bolt-on before launch. Retrofitting audit trails or data-residency controls late is enormously expensive.
- Maintain a direct relationship with compliance/legal/risk teams — they should be reviewing designs early, not signing off at the end.

## 2. Correctness and auditability beat speed
- In financial systems, an incorrect number (a wrong balance, a misapplied fee, a bad trade calculation) is often worse than a slow or missing one. Bias designs toward correctness, idempotency, and reconciliation over raw velocity.
- Every financially meaningful action should be traceable: who/what triggered it, when, with what inputs, and what the system decided. Immutable audit logs are a requirement, not a nice-to-have.
- Build reconciliation jobs that continuously verify your system's state against source-of-truth ledgers or external systems, and alert on drift.

## 3. Data integrity and consistency
- Understand where your system needs strong consistency (balances, trade state, ledger entries) versus where eventual consistency is acceptable (analytics, notifications).
- Money math is not float math — use fixed-point/decimal types and well-defined rounding rules everywhere currency is involved. A single float bug can cause real financial loss.
- Design idempotent APIs and use idempotency keys for anything that moves money or state — network retries must never double-charge or double-book.

## 4. Security is a first-class engineering concern
- Threat-model the program: what's the impact of a breach (funds theft, PII leak, regulatory fine, reputational damage)? Size your security investment accordingly.
- Enforce least-privilege access to production data and systems, especially anything touching customer financial data. Access should be logged and reviewed regularly.
- Plan for encryption at rest and in transit, secrets management, and regular security reviews/pen tests — and budget engineering time for remediation, not just discovery.

## 5. Change management and release discipline
- Financial systems often need controlled, auditable release processes: change approval records, rollback plans, and a clear owner for every production change.
- Favor progressive rollout (feature flags, canary releases, phased regional rollout) over big-bang releases, especially for anything touching money movement.
- Maintain a clean, fast rollback path for every deployable change — "can we revert this in minutes if it's wrong" should be answered before merge, not during an incident.

## 6. Reliability, resilience, and disaster recovery
- Define and track SLOs (availability, latency, correctness) per critical system, and know your recovery time objective (RTO) and recovery point objective (RPO) for each.
- Design for graceful degradation: if a downstream system (payment processor, market data feed, KYC provider) is down, define what your system does — queue, reject cleanly, or fail safe — rather than leaving it undefined.
- Run real disaster recovery and failover tests on a schedule, not just tabletop exercises. Financial regulators increasingly expect evidence of tested resilience.

## 7. Vendor and third-party risk
- Large financial programs depend heavily on third parties (payment rails, market data providers, KYC/AML vendors, cloud providers). Track their SLAs, their own compliance certifications, and your contingency plan if they fail or are breached.
- Avoid hard-coupling your core logic to a single vendor's API/format where the cost of an abstraction layer is reasonable — vendor outages and vendor migrations both happen.
- Understand data residency and data-sharing terms with every vendor that touches customer financial data.

## 8. Program structure for scale
- At multi-team scale, invest deliberately in clear ownership boundaries (who owns which service, which ledger, which integration) to avoid diffusion of responsibility during incidents.
- Standardize cross-team contracts: API versioning policy, event schemas, and backward-compatibility rules — large financial programs live and die by integration discipline.
- Build a lightweight but real architecture review process for anything crossing team/service boundaries, so decisions aren't made in silos that later conflict.

## 9. Testing rigor proportional to blast radius
- Unit and integration tests are the baseline; for money-moving paths, also invest in property-based tests, reconciliation tests, and chaos/failure-injection tests.
- Maintain a realistic staging/sandbox environment that mirrors production integrations (payment processors, market data) closely enough to catch integration issues before release.
- Treat test data for financial scenarios (edge cases in currency, timezones, market holidays, leap seconds/days, negative balances) as a first-class asset — these are where real bugs hide.

## 10. Observability built for incident response
- Instrument systems so that, during an incident, you can quickly answer "how many customers/transactions are affected, and by how much financially" — not just "is the service up."
- Alert on business-meaningful signals (reconciliation mismatches, failed settlement batches, abnormal transaction volume/pattern) in addition to standard infra metrics.
- Maintain clear on-call runbooks, especially for anything that can cause financial loss if mishandled during an incident — engineers should not be improvising money-related decisions at 3am.

## 11. Cost and performance tradeoffs
- Understand the cost profile of your infrastructure (data volumes, transaction throughput, real-time market data feeds) and revisit it as scale grows — financial data volumes and compliance retention requirements can get expensive fast.
- For latency-sensitive systems (trading, real-time payments/fraud checks), define explicit latency budgets per hop and hold vendors and internal services to them.
- Don't over-engineer for theoretical scale — right-size for the actual regulatory retention periods, transaction volumes, and SLAs you're committed to.

## 12. Talent, process, and communication
- Financial-domain knowledge is a real skill gap — invest in onboarding engineers into the domain (settlement cycles, ledger accounting, regulatory terms), not just the codebase.
- Keep stakeholders (compliance, risk, finance, business) in the loop on technical tradeoffs that affect regulatory posture or customer money — surprises here erode trust fast.
- Document decisions and their rationale (design docs, ADRs) — in regulated environments, "why did we build it this way" is a question you will be asked again, often by auditors.

---

*Living document — update as regulations, vendors, and the program's scale evolve.*
