import camera

def test_analytics(cfg):
    req = camera.SetAnalytics()
    msg = camera.proceed_agw_test(req, cfg)

    # Response ID 확인
    assert msg['responseId'] == camera.CommandId.SET_ANALYTICS
    assert msg['status'] == 0
    
