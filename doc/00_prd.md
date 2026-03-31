# Product Requirements Document (PRD)
**Project:** Zero-Backend-Change QA API Coverage Tracker

## 1. Problem Statement
We need strict visibility into which production APIs in a **multi-service microservice environment** are actively being tested by our QA Automation framework versus which APIs are dangerously untested.

Currently, all traffic to our backend services hits the same native Prometheus counters (e.g., `http_requests_total`). Because Prometheus aggregates this data, we cannot mathematically differentiate a request made by a real user from a request made by a QA Python script. Additionally, without a service dimension, teams cannot isolate coverage for their specific microservice when multiple teams share the same observability stack.

## 2. Goals
- Trace exactly which API routes the QA automation framework tests.
- Mathematically calculate a "QA Coverage Percentage" at both global and per-service levels.
- Visually isolate APIs that are completely missing from the QA test suite.
- Support multi-service environments via a dynamic service-level dropdown filter.
- **Require absolutely ZERO code changes to the underlying Go backend services.**

## 3. Non-Goals
- **Line-level Code Coverage:** This tool strictly maps top-level API endpoint routing coverage, not deep line-by-line code execution (like JaCoCo, GoCover, or coverage.py).

## 4. Approach
The QA Automation Framework pushes its own coverage metric (`qa_api_tested_total`) with a `service` label directly to a centralized **Prometheus Pushgateway** during test execution. Grafana queries both the Backend and the Pushgateway and uses a dynamic `$service` dropdown to calculate coverage delta per microservice.

## 5. Acceptance Criteria (V1 - Implemented)

### Global Dashboard
1. **Total APIs Discovered:** Grafana displays all Known APIs from Prometheus.
2. **QA Tested APIs:** Grafana displays all APIs tested by QA.
3. **Uncovered APIs (Delta):** APIs existing in backend but missing in QA.
4. **Deprecated APIs (Ghost Tests):** APIs QA still tests that no longer exist in the backend.

### Service-Level Dashboard (Multi-Service)
5. **Service Dropdown:** Dynamic dropdown listing all services from Prometheus.
6. **Service-Level Coverage %:** Coverage percentage scoped to selected microservice.
7. **Service-Level Trend:** Historical coverage trend graph per service.
8. **Service-Level API Tables:** Covered, Uncovered, and Deprecated lists per service.

## 6. V2 Feature Roadmap

### 6.1 Coverage Intelligence
1. **RAG Indicator per Service** *(Implemented)* — Red/Amber/Green coverage badge per service on dashboard.
2. **Top Uncovered by Traffic Volume** *(Implemented)* — Ranks uncovered APIs by production hit count so teams fix high-impact gaps first.
3. **Exclusion Configuration** *(Implemented)* — Environment variable to exclude health-check endpoints (`/healthz`, `/metrics`, `/ping`) from coverage denominator.
4. **New API Detection Alert** — Alert if a new API appears in Prometheus with no QA test within 24 hours.
5. **Quality Gates** — Fail the CI/CD pipeline if any service drops below a configurable minimum coverage %.

### 6.2 Richer Dashboard Panels
7. **Coverage Heatmap by HTTP Method** — Break down coverage by `GET`, `POST`, `PUT`, `DELETE` to surface untested destructive operations.
8. **Per-Service Trend Comparison** — Single graph comparing coverage trend lines for all services simultaneously.
9. **Test Execution Timestamp** — Show when the QA suite was last run so leadership knows if data is fresh.

### 6.3 Operational Improvements
10. **Test Owner Labeling** — Tag tests with `team` label so managers can see coverage broken down by squad ownership.
11. **Multi-Environment Support** — Dropdown to switch between `staging`, `dev`, and `production` environments.

### 6.4 AI / Automation
12. **AI Auto-Test Generator** — When an API is flagged uncovered, an AI agent reads the OpenAPI/Swagger spec and generates the missing pytest test automatically.
13. **Pipeline Feedback Loop** — Auto-run QA after AI generates tests and verify coverage % increases before merging.

### 6.5 Notifications
14. **Slack/Teams Alertmanager Integration** — Weekly digest pushed to team channel with coverage % trend and top 5 uncovered APIs.
15. **Pre-Release Coverage Report** — Auto-generate a PDF/HTML coverage summary at each release tag and attach it to GitHub release notes.

## 7. Business & Engineering Benefits

### 7.1 Business Value
- **Accelerated Time-to-Market:** By identifying untested APIs instantly, teams can focus their QA efforts where they are most needed, reducing the risk of bugs in new features.
- **Zero-Cost Instrumentation:** Unlike traditional coverage tools that require expensive licenses or heavy code changes, this implementation leverages existing Prometheus infrastructure.
- **ROI on QA Automation:** Leadership can now see a direct correlation between QA headcount/effort and the actual coverage of the production API footprint.

### 7.2 Engineering Excellence
- **Zero-Code-Change Architecture:** Backend developers are never interrupted to add tracking headers or middleware. The system uses native HTTP counters.
- **Language & Framework Agnostic:** The solution works identically for Go, Java (Spring Boot), Python (FastAPI/Django), or Node.js, provided they expose a `/metrics` endpoint.
- **Reduced Test Execution Waste:** Identifies "Ghost Tests" (tests hitting endpoints that no longer exist), allowing teams to trim their test suites and reduce CI/CD runtimes.

### 7.3 Quality & Risk Management
- **Early Gap Detection:** Surfacing quality gaps in real-time.
- **Traffic-Weighted Prioritization:** Instead of trying to hit 100% coverage on every single utility API, teams can prioritize 100% coverage on the **top 10 most-hit production endpoints**.
- **Cross-Service Visibility:** Prevents "Coverage Masking" where high coverage in one service hides dangerous gaps in another, crucial for microservice health.
