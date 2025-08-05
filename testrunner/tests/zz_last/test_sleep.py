import camera

def test_sleep(cfg):
    req = camera.SleepRequest()
    msg = camera.proceed_agw_test(req, cfg)

    # Response ID 확인
    assert msg['responseId'] == camera.CommandId.SLEEP
    assert msg['status'] == 0
    
