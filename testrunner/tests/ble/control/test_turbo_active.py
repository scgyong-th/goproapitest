import pytest
import camera
import proto

@pytest.mark.parametrize("enables", [False, True])
def test_turbo_active(cfg, enables):
    param = proto.RequestSetTurboActive()
    param.active = 
    req = camera.SetTurboActive()
    msg = camera.proceed_agw_test(req, cfg)

    # Response ID 확인
    assert msg['responseId'] == camera.CommandId.KEEP_ALIVE
    assert msg['status'] == 0
    
