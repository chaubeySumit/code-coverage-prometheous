# Real World Guidelines (What to Ignore)

When taking this architectural pattern and plugging it into your actual enterprise infrastructure, you should **ignore/delete** the following sandbox components:

| Sandbox Component | Why to ignore in Real Life | What to do instead |
| :--- | :--- | :--- |
| **`traffic.sh`** | Simulates real users hitting all 3 services so Prometheus knows the APIs exist. | **Delete it.** Your actual users and frontends generate this traffic automatically. |
| **`services/`** | Three dummy Go services exposing basic Prometheus metrics. | **Delete them.** Reuse your existing production/staging microservices already reporting `http_requests_total` to Prometheus. |
| **`grafana/`** | Automatic provisioning configs for localhost. | **Ignore.** Import `grafana/dashboards/coverage.json` directly into your enterprise Grafana via the UI. |

## 4 Steps to Implement in Reality

1. **Deploy Pushgateway:** Ask DevOps to spin up a Prometheus Pushgateway in your cluster and ensure Prometheus scrapes it.

2. **Update your Pytest Framework (`conftest.py`):**
   ```python
   QA_API_TESTED = Counter(
       "qa_api_tested_total",
       "APIs tested by QA",
       ["uri", "method", "service"],  # service label is critical!
       registry=REGISTRY
   )
   ```

3. **Tag every API call with its service name:**
   ```python
   def qa_get(base_url, uri, service):
       response = requests.get(f"{base_url}{uri}")
       QA_API_TESTED.labels(uri=uri, method="GET", service=service).inc()
       return response

   # Usage:
   qa_get(USER_SERVICE_URL, "/api/users", "user-service")
   qa_get(CHECKOUT_SERVICE_URL, "/api/checkout", "checkout-service")
   ```

4. **Import the Dashboard:** Load `grafana/dashboards/coverage.json` into production Grafana. The **Service dropdown** auto-populates from Prometheus and instantly shows coverage per microservice!
