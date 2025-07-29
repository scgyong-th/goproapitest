import requests
import camera
from datetime import datetime, timedelta

from types import SimpleNamespace

def get_date_time(cfg):
    req = camera.GetDateTime(None)
    msg = camera.proceed_agw_test(req, cfg)

    # Response ID 확인
    assert msg['responseId'] == camera.CommandId.GET_DATE_TIME

    # Status 확인
    assert msg['status'] == 0

    # 날짜/시각 확인
    return SimpleNamespace(**msg)



def test_command_set_date_time(cfg):

    # 현재 시각 요청
    dt = get_date_time(cfg)
    dtobj = datetime(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=dt.hour,
        minute=dt.minute,
        second=dt.second
    )
    print(f'Current Camera Date={dtobj}, {dt.__dict__}')

    diff_seconds = 10_000_000
    earlier = dtobj - timedelta(seconds=diff_seconds)
    print(f'{diff_seconds} seconds earlier={earlier}')

    req = camera.SetDateTime(earlier, None)
    msg = camera.proceed_agw_test(req, cfg)

    # Response ID 확인
    assert msg['responseId'] == camera.CommandId.SET_DATE_TIME

    # Status 확인
    assert msg['status'] == 0


    # 업데이트된 시각 요청
    dt2 = get_date_time(cfg)
    print(f'Updated Camera Date={dt2} {dt2.__dict__}')

    assert dt2.year == earlier.year
    assert dt2.month == earlier.month
    assert dt2.day == earlier.day
    assert dt2.hour == earlier.hour
    assert dt2.minute == earlier.minute
    # assert dt2.second == earlier.second

    # 원래 값으로 업데이트
    req = camera.SetDateTime(dt, None)
    msg = camera.proceed_agw_test(req, cfg)
    
    # Response ID 확인
    assert msg['responseId'] == camera.CommandId.SET_DATE_TIME

    # Status 확인
    assert msg['status'] == 0

    # 업데이트된 시각 요청
    dt3 = get_date_time(cfg)
    print(f'Final Camera Date={dt3} {dt3.__dict__}')
