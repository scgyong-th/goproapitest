
def test_config_loaded(cfg):
    assert hasattr(cfg, "base_url")
    assert cfg.timeout == 5
