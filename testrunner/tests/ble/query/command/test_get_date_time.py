import requests
import camera

from types import SimpleNamespace

def test_message(cfg):
    # 1. 요청 객체 생성
    req = camera.GetDateTime(None)
    msg = camera.proceed_agw_test(req, cfg)

    # 7. 날짜/시각 확인
    dt = SimpleNamespace(**msg)
    assert 2000 <= dt.year <= 3000, f'Invalid year: {dt.year}'
    assert 1 <= dt.month <= 12, f'Invalid month: {dt.month}'
    assert 1 <= dt.day <= 31, f'Invalid day: {dt.day}'
    assert 0 <= dt.hour <= 23, f'Invalid hour: {dt.hour}'
    assert 0 <= dt.minute <= 59, f'Invalid minute: {dt.minute}'
    assert 0 <= dt.second <= 59, f'Invalid second: {dt.second}'
    assert 0 <= dt.weekday <= 6, f'Invalid weekday: {dt.weekday}'

