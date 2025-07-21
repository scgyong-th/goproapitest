import requests
import camera

def test_message(cfg):
    # 1. 요청 객체 생성
    req = camera.GetHardwareInfo(None)
    msg = camera.proceed_agw_test(req, cfg)

