import json
import pytest
import os
from types import SimpleNamespace

@pytest.fixture(scope="session")
def cfg():
    config_path = os.path.join(os.path.dirname(__file__), "test_config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return SimpleNamespace(**data)

