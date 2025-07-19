import requests
import camera

def test_message(cfg):
    req = camera.GetHardwareInfo(None)
    url = f'{cfg.base_url}/{req.toForwardPath()}'
    http_resp = requests.get(url)
    assert http_resp.status_code == 200
    resp = http_resp.json()
    print("Response:", resp)
    assert resp['error'] == ''
    msg = camera.parsers.assemble_packets(resp)
    print(f'Msg: {msg.hex()}')

