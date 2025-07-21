import requests
import camera

def test_command_get_hardware_info(cfg):
    # 1. 요청 객체 생성
    req = camera.GetHardwareInfo(None)
    msg = camera.proceed_agw_test(req, cfg)

    # Response ID 확인
    assert msg['responseId'] == camera.CommandId.GET_HARDWARE_INFO

    # Status 확인
    assert msg['status'] == 0

    # Result 범위 확인 - TBD

    # Parsed Result: {
    #     'responseId': 60, 
    #     'status': 0, 
    #     'modelNumber': 
    #     'HERO13 Black', 
    #     'modelName': '0x05', 
    #     'firmwareVersion': 'H24.01.02.02.00', 
    #     'serialNumber': 'C3531325151895', 
    #     'apSsid': 'GP25151895', 
    #     'apMacAddress': '0657475f7a7a', 
    #     'reserved': '01 00 01 01 01 00 02 5B 5D 01 01'
    # }
