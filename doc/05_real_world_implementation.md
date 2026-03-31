# Real World Guidelines (What to Ignore)

When taking this architectural pattern and plugging it into your actual enterprise infrastructure, you should **ignore/delete** the following sandbox components:

| Sandbox Component | Why to ignore in Real Life | What to do instead |
| :--- | :--- | :--- |
| **`traffic.sh`** | This was just a fake script to simulate "Real Users" hitting your APIs so Prometheus would know they exist. | **Delete it.** Your actual frontend applications and real users generate this traffic automatically. |
| **`backend/`** | This was a dummy Go service to expose basic Prometheus metrics. | **Delete it.** Simply reuse your existing production or staging applications that are already reporting `http_requests_total` to Prometheus. |
| **`grafana/`** | Automatic provisioning configs for localhost. | **Ignore.** Import the `/grafana/dashboards/coverage.json` file directly into your enterprise Grafana instance via the UI. |

## 4 Steps to Implement in Reality

1. **Deploy Pushgateway:** Ask your DevOps team to spin up a Prometheus Pushgateway in your cluster and ensure Prometheus scrapes it.
2. **Update your Pytest Framework:** Copy the `CollectorRegistry` code block from `qa/test_api.py` into your actual automation framework's `conftest.py`. Update the `PUSHGATEWAY_URL` to point to the real one.
3. **Wrap your API Calls:** Add the `.inc()` line inside whatever utility function your QA team uses to make HTTP requests (so developers don't have to think about it when writing tests!).
4. **Import Dashboard:** Import the `coverage.json` file to your production Grafana and sit back as coverage calculations happen in real-time!
