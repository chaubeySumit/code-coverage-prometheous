import requests
import pytest
from prometheus_client import CollectorRegistry, Counter, push_to_gateway

# This is the registry we will push to the Gateway
REGISTRY = CollectorRegistry()

# The brand new metric defined strictly in QA
QA_API_TESTED = Counter(
    "qa_api_tested_total",
    "Number of times QA tested a specific API endpoint",
    ["uri", "method"],
    registry=REGISTRY
)

import os

# Configuration for the PoC
BASE_URL = os.getenv("API_URL", "http://localhost:8080")
PUSHGATEWAY_URL = os.getenv("PUSHGATEWAY_URL", "localhost:9091")

# Fixture to push metrics after all tests finish
@pytest.fixture(scope="session", autouse=True)
def push_metrics_after_tests():
    yield # Run the tests
    print(f"\nPushing QA coverage metrics to Pushgateway at {PUSHGATEWAY_URL}...")
    try:
        push_to_gateway(PUSHGATEWAY_URL, job='qa_automation', registry=REGISTRY)
        print("Metrics pushed successfully!")
    except Exception as e:
        print(f"Failed to push metrics: {e}")

# Helper to automatically record QA coverage 
def qa_get(uri):
    # Call the actual API
    response = requests.get(f"{BASE_URL}{uri}")
    
    # Inform Prometheus that QA tested this URI!
    QA_API_TESTED.labels(uri=uri, method="GET").inc()
    
    return response

# ---- THE ACTUAL TESTS ----

def test_users_endpoint_is_tested_by_qa():
    """ QA explicitly tests the /api/users endpoint. """
    resp = qa_get("/api/users")
    assert resp.status_code == 200

def test_deprecated_endpoint():
    """ 
    QA tests an endpoint that no longer exists in Prometheus (the Go code deleted it).
    We manually push the metric directly to simulate QA trying to test it.
    """
    QA_API_TESTED.labels(uri="/api/deprecated-v1", method="GET").inc()

# NOTICE: We do NOT write a test for /api/checkout.
# This simulates a "Missing Test" so we can see the uncovered API in Grafana!
