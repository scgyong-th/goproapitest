import requests
import camera

from types import SimpleNamespace

def test_command_get_date_time(cfg):
    resp = requests.get(f'{cfg.base_url}/app/info')
    print(resp.text)
