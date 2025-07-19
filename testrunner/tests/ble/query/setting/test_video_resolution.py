import requests
from camera import QueryRequest, QueryId, SettingId

def test_message(cfg):
    req = QueryRequest(QueryId.GET_SETTING_VALUES, SettingId.VIDEO_RESOLUTION, None)
    url = f'{cfg.base_url}/{req.toForwardPath()}'
    http_resp = requests.get(url)
    assert http_resp.status_code == 200
    resp = http_resp.json()
    print(resp)

