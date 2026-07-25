# Specialist selection

Return overlays in this order:

1. API development — API routes, controllers, schemas, contracts.
2. Frontend development — components, styles, client state, accessibility.
3. Data development — models, migrations, queries, persistence.
4. Integration development — third-party clients, webhooks, retries.
5. Functional QA — business behavior and acceptance criteria.
6. Edge-case QA — boundaries, concurrency, recovery, failure modes.
7. Performance QA — hot paths, load, latency, resource use.
8. Application security — authentication, authorization, input, sessions.
9. Data privacy — personal, regulated, or sensitive data.

Select all matching overlays, but never select one from its name alone. Use
task scope and affected paths. The same normalized scope must always return the
same ordered list.
