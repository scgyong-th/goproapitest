import requests
import camera

from types import SimpleNamespace

def test_message(cfg):
    # 1. 요청 객체 생성
    req = camera.GetDateTime(None)
    url = f"{cfg.base_url}/{req.toForwardPath()}"
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

    # 7. 날짜/시각 확인
    dt = SimpleNamespace(**msg)
    assert dt.year >= 2000, f'Invalid year: {dt.year}'
    assert 1 <= dt.month <= 12, f'Invalid month: {dt.month}'
    assert 1 <= dt.day <= 31, f'Invalid day: {dt.day}'
    assert 0 <= dt.hour <= 23, f'Invalid hour: {dt.hour}'
    assert 0 <= dt.minute <= 59, f'Invalid minute: {dt.minute}'
    assert 0 <= dt.second <= 59, f'Invalid second: {dt.second}'
    assert 0 <= dt.weekday <= 6, f'Invalid weekday: {dt.weekday}'

