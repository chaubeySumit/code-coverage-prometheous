# Product Requirements Document (PRD)
**Project:** Zero-Backend-Change QA API Coverage Tracker

## 1. Problem Statement
We need strict visibility into which production APIs are actively being tested by our QA Automation framework versus which APIs are dangerously untested. 

Currently, all traffic to our backend services hits the same native Prometheus counters (e.g., `http_requests_total`). Because Prometheus aggregates this data, we cannot mathematically differentiate a request made by a real user from a request made by a QA Python script. Furthermore, requiring developers to modify the Go backend services to extract specialized "QA HTTP Headers" and expose custom labels is not scalable or feasible for our current architecture.

## 2. Goals
- Trace exactly which API routes the QA automation framework tests.
- Mathematically calculate an overall "QA Coverage Percentage" against the total pool of all known APIs.
- Visually isolate APIs that are completely missing from the QA test suite.
- **Require absolutely ZERO code changes to the underlying Go backend services.**

## 3. Non-Goals
- **Line-level Code Coverage:** This tool is not intended to measure deep, line-by-line code execution coverage (like JaCoCo, GoCover, or coverage.py) inside the backend binaries. It strictly maps top-level API endpoint routing coverage.

## 4. Approach
The QA Automation Framework will be updated to push its own coverage metric (`qa_api_tested_total`) directly to a centralized **Prometheus Pushgateway** during test execution. Grafana will then query both the Backend and the Pushgateway to calculate the coverage delta.

## 5. Acceptance Criteria
1. **Total APIs Discovered:** Grafana must display a complete list of all Known APIs by leveraging existing backend Prometheus metrics.
2. **QA Tested APIs:** Grafana must display a list of all APIs successfully tested by QA.
3. **Uncovered APIs (Delta):** Grafana must mathematically surface a list of completely uncovered APIs (exists in Backend, missing in QA).
4. **Deprecated APIs (Ghost Tests):** Grafana must surface APIs that the QA team is still testing, but which no longer exist in the backend Prometheus registry.

## 6. Business & Engineering Benefits
- **Zero-Friction Adoption:** Because it requires no backend code changes or infrastructure routing changes, any engineering team in the organization can adopt this instantly.
- **Language Agnostic:** The backend can be written in Go, Java, Python, or Node. As long as it spits out basic Prometheus metrics, the coverage calculator works.
- **Pinpoint Risk Management:** Leadership and Release Managers can immediately identify high-risk, untested APIs before production deployments.
- **Cleanup Identification:** Highlights "Ghost Tests" where QA is wasting runtime calculating assertions on deprecated endpoints.

## 7. Future Scope (v2.0 Vision)
To scale this tool for a larger enterprise audience, Version 2.0 will introduce the following advanced capabilities:

1. **AI-Driven Auto-Remediation:** 
   - When an API is flagged as "Uncovered" in Grafana, an AI agent will automatically analyze the API's swagger/openapi spec and generate the missing Python automation code.
2. **Automated Pipeline Feedback Loops:**
   - The CI/CD pipeline will automatically inject the AI-generated test code, re-run the QA suite, and verify in real-time that the Grafana Coverage Percentage has mathematically increased.
3. **Exclusion Configuration (`.qaignore`):**
   - Introduce a configuration file to explicitly ignore infrastructural algorithms, webhooks, or health-checks (e.g., `/metrics`, `/healthz`). These ignored APIs will be completely removed from the coverage percentage denominator so they don't drag down the team's score.
4. **Traffic-Weighted Coverage Heatmaps (Enterprise Feature):**
   - Plot the APIs not just by "Covered" vs "Uncovered", but weighted dynamically by how heavily they are used in production. This prioritizes QA efforts on fixing a missing test for a core `/checkout` API instead of a rarely used `/admin/logs` API.
5. **Slack/Teams Alerting:** 
   - Automated alerts fired into developer's chat instantly if they merge a new API but QA coverage hasn't caught up to it within 24 hours.
