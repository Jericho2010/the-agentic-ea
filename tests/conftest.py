"""
Pytest configuration for The Agentic EA test suite.
Ensures local SQLite fallback mode is the default for offline workstation test execution.
"""
import os

# Set offline mode default so local workstation testing is fast and deterministic
os.environ.setdefault("DATABRICKS_OFFLINE", "1")
