# How It Works (The Math)

Prometheus natively tracks all HTTP requests hitting your services via standard metrics (e.g., `http_requests_total`). As real users navigate your application, Prometheus builds a list of "Known APIs" tagged with their respective `service` name.

Instead of forcing the backend to figure out if traffic is coming from a real user or a test script, the **QA Automation framework itself** pushes a separate metric directly to a Prometheus Pushgateway (e.g., `qa_api_tested_total`), also tagged with the `service` label.

Grafana uses a dynamic `$service` dropdown variable to filter both datasets and calculate coverage mathematically:

| Dashboard Panel | PromQL |
|:---|:---|
| **All Known APIs** | `count by (uri, service) (http_requests_total{service=~"$service"})` |
| **Covered APIs** | `count by (uri, service) (qa_api_tested_total{service=~"$service"}) and count by (uri, service) (http_requests_total{service=~"$service"})` |
| **Uncovered APIs** | `count by (uri, service) (http_requests_total{service=~"$service"}) unless count by (uri, service) (qa_api_tested_total{service=~"$service"})` |
| **Deprecated APIs** | `count by (uri, service) (qa_api_tested_total{service=~"$service"}) unless count by (uri, service) (http_requests_total{service=~"$service"})` |
| **Coverage %** | `count(covered) / count(all known)` |
