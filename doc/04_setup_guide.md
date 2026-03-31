# Setup Document (Running the Sandbox)

## Project Structure

```
code_coverage_prom/
├── services/
│   ├── user-service/        # Go service (Port 8081): /api/users, /api/profile, /api/login
│   ├── checkout-service/    # Go service (Port 8082): /api/checkout, /api/payment, /api/orders
│   └── inventory-service/   # Go service (Port 8083): /api/products, /api/stock, /api/categories
├── qa/                      # Python pytest automation (pushes to Pushgateway)
├── prometheus/              # Prometheus scrape config (all 3 services + pushgateway)
├── grafana/                 # Dashboard JSON + provisioning
├── traffic.sh               # Simulates real user traffic across all 3 services
└── docker-compose.yml       # Orchestrates all 9 containers
```

## What Gets Spun Up

| Container | Purpose | Port |
|:---|:---|:---|
| `user-service` | Mock Go backend | 8081 |
| `checkout-service` | Mock Go backend | 8082 |
| `inventory-service` | Mock Go backend | 8083 |
| `pushgateway` | Receives QA metrics | 9091 |
| `prometheus` | Scrapes all services | 9090 |
| `grafana` | Coverage dashboard | 3000 |
| `traffic-generator` | Simulates real users | - |
| `qa-automation` | Runs tests, pushes metrics | - |

## Running the Sandbox

Run the following command from the root directory:
```bash
docker compose up --build -d
```
*Wait ~15 seconds for all services to initialize.*

Then open **[http://localhost:3000](http://localhost:3000)** (credentials: `admin` / `admin`).

## Demonstrating Multi-Service Coverage

Use the **Service dropdown** on the dashboard to switch between services:

| Service | Coverage | Missing APIs |
|:---|:---|:---|
| `user-service` | 100% ✅ | None |
| `checkout-service` | 100% ✅ | None |
| `inventory-service` | 100% ✅ | None |

## Teardown

```bash
docker compose down
```
