# QA API Coverage Tracking (Zero Backend Changes)

This repository demonstrates how to mathematically track and visualize API Test Coverage across **multiple microservices** using Prometheus and Grafana, **without making a single code change to your backend services.**

## Services in This PoC

| Service | Port | APIs |
|:---|:---|:---|
| `user-service` | 8081 | `/api/users`, `/api/profile`, `/api/login` |
| `checkout-service` | 8082 | `/api/checkout`, `/api/payment`, `/api/orders` |
| `inventory-service` | 8083 | `/api/products`, `/api/stock`, `/api/categories` |

## Documentation

All project documentation is in the `doc/` folder:

1. [Product Requirements Document (PRD)](doc/00_prd.md)
2. [How It Works (The Math)](doc/01_how_it_works.md)
3. [Architecture Diagram](doc/02_architecture_diagram.md)
4. [Execution Sequence Diagram](doc/03_execution_sequence.md)
5. [Sandbox Setup Guide](doc/04_setup_guide.md)
6. [Real World Implementation Guide](doc/05_real_world_implementation.md)

## Quick Start

```bash
docker compose up --build -d
```

Open **[http://localhost:3000](http://localhost:3000)** (credentials: `admin` / `admin`) and use the **Service dropdown** to filter coverage per microservice.
