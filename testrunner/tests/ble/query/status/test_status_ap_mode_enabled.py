import requests
import camera

def test_message(cfg):
    # 1. 요청 객체 생성
    req = camera.QueryRequest(
        camera.QueryId.GET_STATUS_VALUES, 
        camera.StatusId.AP_MODE_ENABLED,
        None)
    msg = camera.proceed_agw_test(req, cfg)


