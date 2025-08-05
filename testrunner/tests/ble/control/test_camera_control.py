import camera
import proto
import pytest

ECC = proto.EnumCameraControlStatus
RG = proto.EnumResultGeneric

@pytest.mark.parametrize("status,expected", [
    (ECC.CAMERA_IDLE, RG.RESULT_SUCCESS),
    (ECC.CAMERA_CONTROL, RG.RESULT_UNKNOWN),
    (ECC.CAMERA_EXTERNAL_CONTROL, RG.RESULT_SUCCESS),
    (ECC.CAMERA_COF_SETUP, RG.RESULT_SUCCESS),
])
def test_camera_control(cfg, status, expected):
    status_name = ECC.Name(status)
    expected_name = proto.EnumResultGeneric.Name(expected)
    print(f'Testing status={status_name}({status}) Expedted result={expected_name}({expected})')
    ccs = proto.RequestSetCameraControlStatus()
    ccs.camera_control_status = status
    req = camera.SetCameraControl(ccs)
    msg = camera.proceed_agw_test(req, cfg)

    print(f'Result = {msg.result}({RG.Name(msg.result)})')

    assert msg.result == expected


