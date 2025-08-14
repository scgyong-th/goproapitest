import camera

def test_camera_state(cfg):
    req = camera.HttpGetRequest('/gopro/camera/state')
    msg = camera.proceed_http_test(req, cfg)

    assert type(msg) == dict

    assert 'status' in msg
    assert 'settings' in msg

    all_status = msg['status']
    all_settings = msg['settings']

    assert len(all_status) > 20
    assert len(all_settings) > 20
    

