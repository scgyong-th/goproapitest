import requests
from camera import QueryRequest, QueryId, SettingId
import camera

def test_query_setting_video_resolution(cfg):
    req = QueryRequest(QueryId.GET_SETTING_VALUES, SettingId.VIDEO_RESOLUTION, None)
    msg = camera.proceed_agw_test(req, cfg)

    # Response ID 확인
    assert msg['responseId'] == camera.QueryId.GET_SETTING_VALUES

    # Status 확인
    assert msg['status'] == 0

    # TLV Response 확인
    assert SettingId.VIDEO_RESOLUTION in msg['tlv']

    value = msg['tlv'][SettingId.VIDEO_RESOLUTION][0] # byte array 이기 때문에 [0] 을 붙여야 한다
    print(f'VIDEO_RESOLUTION={value}')

    # value 확인
    assert value in [1, 4, 6, 7, 9, 12, 18, 24, 25, 26, 27, 28, 35, 36, 37, 38, 100, 107, 108, 109, 110, 111, 112, 113]

    # 모델별 지원 해상도 확인 - TBD

    # ID  Option Name Supported Cameras
    # 1   4K
    # 4   2.7K
    # 6   2.7K 4:3
    # 7   1440
    # 9   1080
    # 12  720
    # 18  4K 4:3
    # 24  5K
    # 25  5K 4:3
    # 26  5.3K 8:7
    # 27  5.3K 4:3
    # 28  4K 8:7
    # 35  5.3K 21:9
    # 36  4K 21:9
    # 37  4K 1:1
    # 38  900
    # 100 5.3K
    # 107 5.3K 8:7 V2
    # 108 4K 8:7 V2
    # 109 4K 9:16 V2
    # 110 1080 9:16 V2
    # 111 2.7K 4:3 V2
    # 112 4K 4:3 V2
    # 113 5.3K 4:3 V2
