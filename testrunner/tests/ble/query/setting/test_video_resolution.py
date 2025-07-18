import requests
from camera import QueryRequest, QueryId, SettingId

def test_message(cfg):
    req = QueryRequest(QueryId.GET_SETTING_VALUES, SettingId.VIDEO_RESOLUTION, None)
    url = f'{cfg.base_url}/forward/ble/req.'
