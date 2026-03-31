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
2. **Coverage Regression Alert** *(Implemented)* — Alert fires if coverage % drops between consecutive QA runs.
3. **Top Uncovered by Traffic Volume** *(Implemented)* — Ranks uncovered APIs by production hit count so teams fix high-impact gaps first.
4. **Exclusion Configuration** *(Implemented)* — Environment variable to exclude health-check endpoints (`/healthz`, `/metrics`, `/ping`) from coverage denominator.
5. **New API Detection Alert** — Alert if a new API appears in Prometheus with no QA test within 24 hours.
6. **Quality Gates** — Fail the CI/CD pipeline if any service drops below a configurable minimum coverage %.

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
- **Zero-Friction Adoption:** No backend code changes needed — any team can adopt instantly.
- **Language Agnostic:** Works across Go, Java, Python, Node — any backend exposing Prometheus metrics.
- **Multi-Team Ownership:** Service-level filtering prevents team A's coverage from masking team B's gaps.
- **Pinpoint Risk Management:** Leadership identifies high-risk untested APIs before production deployments.
- **Cleanup Identification:** Highlights "Ghost Tests" where QA wastes runtime testing deprecated endpoints.
