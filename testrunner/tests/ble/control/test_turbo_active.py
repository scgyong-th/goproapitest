import pytest
import time
import camera
import proto

@pytest.mark.parametrize("enables", [True, False])
def test_turbo_active(cfg, enables):
    param = proto.RequestSetTurboActive()
    param.active = enables
    req = camera.SetTurboActive(param)
    msg = camera.proceed_agw_test(req, cfg)

    assert type(msg) == proto.ResponseGeneric
    assert msg.result == proto.EnumResultGeneric.RESULT_SUCCESS

    # 바로 요청하는 경우 제대로 된 응답이 오지 않아서 1초 쉬었다가 query 하도록 수정.
    print(f'SetTurboActive Result={msg.result}. Sleeping 1 sec.')
    time.sleep(1)
    print(f'After Sleeping 1 sec.')

    req = camera.GetStatusValues(camera.StatusId.TURBO_TRANSFER_ACTIVE)
    msg = camera.proceed_agw_test(req, cfg)

    # Response ID 확인
    assert msg['responseId'] == camera.QueryId.GET_STATUS_VALUES
    assert msg['status'] == 0

    tlv = msg['tlv']
    assert tlv
    assert camera.StatusId.TURBO_TRANSFER_ACTIVE in tlv

    enabled = True if tlv[camera.StatusId.TURBO_TRANSFER_ACTIVE] else False
    print(f'Enabled: {enabled}')
    assert enables == enabled, f'{enables=} != {enabled=}'

    
