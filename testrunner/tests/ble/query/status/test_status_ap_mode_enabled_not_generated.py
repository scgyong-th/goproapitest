import requests
import camera

statusId = camera.StatusId.AP_MODE_ENABLED

def test_query_status_ap_mode_enabled(cfg):
    # 1. 요청 객체 생성
    req = camera.QueryRequest(
        camera.QueryId.GET_STATUS_VALUES, 
        statusId,
        None)
    msg = camera.proceed_agw_test(req, cfg)

    # Response ID 확인
    assert msg['responseId'] == camera.QueryId.GET_STATUS_VALUES

    # Status 확인
    assert msg['status'] == 0

    # TLV Response 확인
    assert statusId in msg['tlv']

    value = msg['tlv'][statusId][0] # byte array 이기 때문에 [0] 을 붙여야 한다
    print(f'AP_MODE_ENABLED={value}')

    # value 확인
    assert value in [0, 1]

