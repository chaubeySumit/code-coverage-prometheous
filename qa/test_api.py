import requests
import pytest
from prometheus_client import CollectorRegistry, Counter, push_to_gateway
import os

REGISTRY = CollectorRegistry()

QA_API_TESTED = Counter(
    "qa_api_tested_total",
    "Number of times QA tested a specific API endpoint",
    ["uri", "method", "service"],
    registry=REGISTRY
)

# Service URLs from environment variables
USER_SERVICE_URL      = os.getenv("USER_SERVICE_URL",      "http://localhost:8081")
CHECKOUT_SERVICE_URL  = os.getenv("CHECKOUT_SERVICE_URL",  "http://localhost:8082")
INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL", "http://localhost:8083")
PUSHGATEWAY_URL       = os.getenv("PUSHGATEWAY_URL",       "localhost:9091")

@pytest.fixture(scope="session", autouse=True)
def push_metrics_after_tests():
    yield
    print(f"\nPushing QA coverage metrics to Pushgateway at {PUSHGATEWAY_URL}...")
    try:
        push_to_gateway(PUSHGATEWAY_URL, job='qa_automation', registry=REGISTRY)
        print("Metrics pushed successfully!")
    except Exception as e:
        print(f"Failed to push metrics: {e}")

def qa_get(base_url, uri, service):
    response = requests.get(f"{base_url}{uri}")
    QA_API_TESTED.labels(uri=uri, method="GET", service=service).inc()
    return response

# ---- USER SERVICE TESTS ----
# Testing: /api/users and /api/login
# Intentionally NOT testing: /api/profile (to show as uncovered)

def test_user_service_users():
    resp = qa_get(USER_SERVICE_URL, "/api/users", "user-service")
    assert resp.status_code == 200

def test_user_service_login():
    resp = qa_get(USER_SERVICE_URL, "/api/login", "user-service")
    assert resp.status_code == 200

# ---- CHECKOUT SERVICE TESTS ----
# Testing: /api/checkout only
# Intentionally NOT testing: /api/payment and /api/orders (to show as uncovered)

def test_checkout_service_checkout():
    resp = qa_get(CHECKOUT_SERVICE_URL, "/api/checkout", "checkout-service")
    assert resp.status_code == 200

# ---- INVENTORY SERVICE TESTS ----
# Testing: all 3 endpoints (100% coverage for this service)

def test_inventory_service_products():
    resp = qa_get(INVENTORY_SERVICE_URL, "/api/products", "inventory-service")
    assert resp.status_code == 200

def test_inventory_service_stock():
    resp = qa_get(INVENTORY_SERVICE_URL, "/api/stock", "inventory-service")
    assert resp.status_code == 200

def test_inventory_service_categories():
    resp = qa_get(INVENTORY_SERVICE_URL, "/api/categories", "inventory-service")
    assert resp.status_code == 200

# ---- DEPRECATED API SIMULATION ----
# QA script still tests a deprecated endpoint that no longer exists in the backend
def test_deprecated_endpoint():
    QA_API_TESTED.labels(uri="/api/deprecated-v1", method="GET", service="user-service").inc()
