import camera

def test_open_gopro_version(cfg):
    req = camera.GetOpenGoproVersion()
    msg = camera.proceed_agw_test(req, cfg)

    # Response ID 확인
    assert msg['responseId'] == camera.CommandId.GET_OPEN_GOPRO_VERSION
    assert msg['status'] == 0
    
