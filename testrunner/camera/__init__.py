from .ble_request import *
from .constants import *
from . import parsers

import requests

def proceed_agw_test(req, cfg):
    url = f'{cfg.base_url}/{req.toForwardPath()}'
    print(f"Request: {url}")

    # 2. HTTP 요청
    http_resp = requests.get(url)
    assert http_resp.status_code == 200

    # 3. JSON 응답 파싱
    resp = http_resp.json()
    req.resp = resp
    print(f"Response: {resp}")
    assert resp["error"] == ""

    # 4. ID2 확인
    resp_id2 = resp["id2"]
    expected_id2 = ID2.response[req.characteristic]
    assert resp_id2 == expected_id2

    # 5. 패킷 조립
    data = parsers.assemble_packets(resp)
    req.data = data
    print(f"Assembled bytes: {data.hex()}")

    # 6. 파서 호출
    parser = parsers.get(resp_id2, data)
    req.parser = parser

    # 7. 파싱
    msg = parser.parse()
    req.msg = msg

    print("Parsed Result:", msg)

    return msg