from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str) -> ModuleType:
    path = PROJECT_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def producer_module() -> ModuleType:
    return load_module("smartops_producer", "producer/log_generator.py")


@pytest.fixture
def consumer_module() -> ModuleType:
    return load_module("smartops_consumer", "kafka/consumer.py")


@pytest.fixture
def rag_module() -> ModuleType:
    return load_module("smartops_rag", "rag/incident_rag.py")


@pytest.fixture
def mcp_module() -> ModuleType:
    return load_module("smartops_mcp", "mcp/server.py")
