import camera

def test_keep_alive(cfg):
    req = camera.KeepAliveRequest()
    msg = camera.proceed_agw_test(req, cfg)

    # Response ID 확인
    assert msg['responseId'] == camera.CommandId.KEEP_ALIVE
    assert msg['status'] == 0
    
