import camera
import pytest

@pytest.mark.parametrize("enables", [False, True])
def test_ap_control(cfg, enables):
    print(f'Enables AP = {enables}')
    req = camera.SetApControl(enables=enables)
    msg = camera.proceed_agw_test(req, cfg)

    # Response ID 확인
    assert msg['responseId'] == camera.CommandId.SET_AP_CONTROL
    assert msg['status'] == 0
    
