import requests
from camera import QueryRequest, QueryId, SettingId
import camera

def test_message(cfg):
    req = QueryRequest(QueryId.GET_SETTING_VALUES, SettingId.VIDEO_RESOLUTION, None)
    msg = camera.proceed_agw_test(req, cfg)




