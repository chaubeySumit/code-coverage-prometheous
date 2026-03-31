#!/usr/bin/env python3
"""
qa_exclude.py - Exclusion configuration for QA Coverage calculation.

Add any URI patterns here that should be EXCLUDED from the coverage
denominator (e.g. health checks, metrics endpoints, internal probes).

These endpoints will still be callable but will NOT count against
your coverage percentage in Grafana.
"""

# List of URI prefixes/exact paths to exclude from coverage calculation
EXCLUDED_URIS = [
    "/healthz",
    "/health",
    "/livez",
    "/readyz",
    "/metrics",
    "/ping",
    "/favicon.ico",
]

def is_excluded(uri: str) -> bool:
    """Returns True if the given URI should be excluded from coverage tracking."""
    for excluded in EXCLUDED_URIS:
        if uri == excluded or uri.startswith(excluded + "/"):
            return True
    return False
