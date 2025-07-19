import requests
import camera

def test_message(cfg):
    req = camera.GetHardwareInfo(None)
    url = f'{cfg.base_url}/{req.toForwardPath()}'
    print(f"Request: {url}")
    http_resp = requests.get(url)
    assert http_resp.status_code == 200
    resp = http_resp.json()
    print(f"Response: {resp}")
    assert resp['error'] == ''
    resp_id2 = camera.ID2.response[req.characteristic]
    assert resp['id2'] == resp_id2
    data = camera.parsers.assemble_packets(resp)
    print(f'Assembled bytes: {data.hex()}')

    msg = camera.parsers.parse_response_data(data)

