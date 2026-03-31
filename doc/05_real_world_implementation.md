# Real World Guidelines (What to Ignore)

When taking this architectural pattern and plugging it into your actual enterprise infrastructure, you should **ignore/delete** the following sandbox components:

| Sandbox Component | Why to ignore in Real Life | What to do instead |
| :--- | :--- | :--- |
| **`traffic.sh`** | Simulates "Real Users" so Prometheus knows the APIs exist. | **Delete it.** Your actual users and frontends generate this traffic automatically. |
| **`backend/`** | A dummy Go service exposing basic Prometheus metrics. | **Delete it.** Reuse your existing production/staging services already reporting to Prometheus. |
| **`grafana/`** | Automatic provisioning configs for localhost. | **Ignore.** Import `grafana/dashboards/coverage.json` directly into your enterprise Grafana via the UI. |

## 4 Steps to Implement in Reality

1. **Deploy Pushgateway:** Ask DevOps to spin up a Prometheus Pushgateway in your cluster and ensure Prometheus scrapes it.

2. **Update your Pytest Framework (`conftest.py`):**
   ```python
   QA_API_TESTED = Counter(
       "qa_api_tested_total",
       "APIs tested by QA",
       ["uri", "method", "service"],  # Include the service label!
       registry=REGISTRY
   )
   ```

3. **Tag every API call with its service name:**
   ```python
   def qa_get(uri, service):
       response = requests.get(f"{BASE_URL}{uri}")
       QA_API_TESTED.labels(uri=uri, method="GET", service=service).inc()
       return response
   ```

4. **Import the Dashboard:** Load `grafana/dashboards/coverage.json` into production Grafana. The **Service dropdown** will automatically populate from Prometheus and immediately show coverage per microservice.
