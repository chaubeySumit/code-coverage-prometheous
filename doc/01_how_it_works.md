# How It Works (The Math)

Prometheus natively tracks all HTTP requests hitting your services via standard metrics (e.g., `http_requests_total`). As real users navigate your application, Prometheus builds a list of "Known APIs" tagged with their respective `service` name.

Instead of forcing the backend to figure out if traffic is coming from a real user or a test script, the **QA Automation framework itself** pushes a separate metric directly to a Prometheus Pushgateway (e.g., `qa_api_tested_total`), also tagged with the `service` label.

Grafana uses a dynamic `$service` dropdown variable to filter both datasets and calculate coverage mathematically.

### V2 Core Math (with Exclusions)
We now exclude health/metrics endpoints from the denominator to ensure coverage % isn't diluted.

| Dashboard Panel | V2 PromQL (Simplified) |
|:---|:---|
| **All Known APIs** | `count by (uri, service) (http_requests_total{service=~"$service", uri!~"/health.*|/metrics|/ping"})` |
| **Covered APIs** | `count by (uri, service) (qa_api_tested_total{service=~"$service"}) and ...` |
| **Coverage %** | `count(covered) / count(all known)` |
| **Regression Alert**| `current_coverage < bool (coverage offset 5m)` |
| **Traffic Weight** | `topk(10, sum(http_requests_total) unless sum(qa_api_tested_total))` |

> [!NOTE]
> The exclusion list is configurable in `qa/qa_exclude.py` and is automatically applied to both the QA test runner and the Grafana dashboard.
