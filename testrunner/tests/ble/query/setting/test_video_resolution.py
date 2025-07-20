import requests
from camera import QueryRequest, QueryId, SettingId
import camera

def test_message(cfg):
    req = QueryRequest(QueryId.GET_SETTING_VALUES, SettingId.VIDEO_RESOLUTION, None)
    url = f'{cfg.base_url}/{req.toForwardPath()}'
    print(f"Request: {url}")

    # 2. HTTP 요청
    http_resp = requests.get(url)
    assert http_resp.status_code == 200

    # 3. JSON 응답 파싱
    resp = http_resp.json()
    print(f"Response: {resp}")
    assert resp["error"] == ""

    # 4. ID2 확인
    resp_id2 = camera.ID2.response[req.characteristic]
    assert resp["id2"] == resp_id2

    # 5. 패킷 조립
    data = camera.parsers.assemble_packets(resp)
    print(f"Assembled bytes: {data.hex()}")

    # 6. 파서 호출
    (parser, msg) = camera.parsers.parse(resp_id2, data)
    print("Parsed Result:", msg)

def test_hello(cfg):
    print("hello")



