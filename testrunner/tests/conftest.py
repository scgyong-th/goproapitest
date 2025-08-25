import json
import pytest
import os, sys
from types import SimpleNamespace

import camera

@pytest.fixture(scope="session")
def cfg():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "test_config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return SimpleNamespace(**data)

