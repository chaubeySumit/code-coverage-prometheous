# How It Works (The Math)

Prometheus natively tracks all HTTP requests hitting your services via standard metrics (e.g., `http_requests_total`). As real users navigate your application, Prometheus builds a list of "Known APIs."

Instead of forcing the backend to figure out if traffic is coming from a real user or a test script, we instruct the **QA Automation framework itself** to push a separate metric directly to a Prometheus Pushgateway (e.g., `qa_api_tested_total`).

Grafana then acts as the central brain, comparing the two datasets mathematically:
- **Total Known APIs:** `count by (uri) (http_requests_total)`
- **Covered By QA:** `count by (uri) (qa_api_tested_total)`
- **Uncovered APIs:** `count by (uri) (http_requests_total) unless count by (uri) (qa_api_tested_total)`
