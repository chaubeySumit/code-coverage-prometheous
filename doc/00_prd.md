# Product Requirements Document (PRD)
**Project:** Zero-Backend-Change QA API Coverage Tracker

## 1. Problem Statement
We need strict visibility into which production APIs in a **multi-service microservice environment** are actively being tested by our QA Automation framework versus which APIs are dangerously untested.

Currently, all traffic to our backend services hits the same native Prometheus counters (e.g., `http_requests_total`). Because Prometheus aggregates this data, we cannot mathematically differentiate a request made by a real user from a request made by a QA Python script. Additionally, without a service dimension, teams cannot isolate coverage for their specific microservice when multiple teams share the same observability stack.

Requiring developers to modify the Go backend services to extract specialized "QA HTTP Headers" and expose custom labels is not scalable or feasible for our current architecture.

## 2. Goals
- Trace exactly which API routes the QA automation framework tests.
- Mathematically calculate an overall "QA Coverage Percentage" at both global and per-service levels.
- Visually isolate APIs that are completely missing from the QA test suite.
- Support multi-service environments via a dynamic service-level dropdown filter.
- **Require absolutely ZERO code changes to the underlying Go backend services.**

## 3. Non-Goals
- **Line-level Code Coverage:** This tool strictly maps top-level API endpoint routing coverage, not deep line-by-line code execution (like JaCoCo, GoCover, or coverage.py).

## 4. Approach
The QA Automation Framework will be updated to push its own coverage metric (`qa_api_tested_total`) with a `service` label directly to a centralized **Prometheus Pushgateway** during test execution. Grafana will then query both the Backend and the Pushgateway and use a dynamic `$service` dropdown to calculate coverage delta per microservice.

## 5. Acceptance Criteria

### Global Dashboard
1. **Total APIs Discovered:** Grafana displays a complete list of all Known APIs.
2. **QA Tested APIs:** Grafana displays a list of all APIs tested by QA.
3. **Uncovered APIs (Delta):** Grafana surfaces APIs existing in Backend but missing in QA.
4. **Deprecated APIs (Ghost Tests):** Grafana surfaces APIs QA still tests, but which no longer exist in the backend.

### Service-Level Dashboard (Multi-Service)
5. **Service Dropdown:** A dynamic dropdown listing all services discovered from Prometheus.
6. **Service-Level Coverage %:** Coverage percentage calculated strictly for the selected microservice.
7. **Service-Level Trend:** Historical coverage trend graph per service.
8. **Service-Level API Tables:** Covered, Uncovered, and Deprecated API lists scoped to the selected service.

## 6. Business & Engineering Benefits
- **Zero-Friction Adoption:** No backend code changes needed — any team can adopt this instantly.
- **Language Agnostic:** Works across Go, Java, Python, Node — any backend exposing Prometheus metrics.
- **Multi-Team Ownership:** Service-level filtering prevents team A's coverage from masking team B's gaps.
- **Pinpoint Risk Management:** Leadership and Release Managers can identify high-risk, untested APIs before production deployments.
- **Cleanup Identification:** Highlights "Ghost Tests" where QA wastes runtime testing deprecated endpoints.

## 7. Future Scope (v2.0 Vision)
1. **AI-Driven Auto-Remediation:** AI reads the Swagger/OpenAPI spec of an "Uncovered API" and automatically generates the missing Python test code.
2. **Automated Pipeline Feedback Loops:** CI/CD pipeline re-runs QA and verifies the coverage % increases in Grafana.
3. **Exclusion Configuration (`.qaignore`):** Config file to blacklist health-check and infrastructural endpoints (e.g., `/metrics`, `/healthz`) from the coverage denominator.
4. **Traffic-Weighted Coverage Heatmaps:** APIs ranked by production traffic volume to prioritize high-impact untested endpoints.
5. **Slack/Teams Alerting:** Automated alert if a new API is merged but QA hasn't covered it within 24 hours.
