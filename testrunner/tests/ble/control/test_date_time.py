import requests
import camera
from datetime import datetime, timedelta, timezone

from types import SimpleNamespace

def get_date_time(cfg):
    req = camera.GetDateTime()
    msg = camera.proceed_agw_test(req, cfg)

    # Response ID 확인
    assert msg['responseId'] == camera.CommandId.GET_DATE_TIME

    # Status 확인
    assert msg['status'] == 0

    # 날짜/시각 확인
    return SimpleNamespace(**msg)

def get_local_time(cfg):
    req = camera.GetLocalDateTime()
    msg = camera.proceed_agw_test(req, cfg)

    # Response ID 확인
    assert msg['responseId'] == camera.CommandId.GET_LOCAL_DATE_TIME

    # Status 확인
    assert msg['status'] == 0

    # 날짜/시각 확인
    return SimpleNamespace(**msg)

    # 0D 1000 0A07E9071D0E1A28021C00

def set_date_time(cfg, dt):
    req = camera.SetDateTime(dt)
    msg = camera.proceed_agw_test(req, cfg)

    # Response ID 확인
    assert msg['responseId'] == camera.CommandId.SET_DATE_TIME

    # Status 확인
    assert msg['status'] == 0

def set_local_time(cfg, dt):
    if isinstance(dt, datetime):
        dt = dt.astimezone()  # ensure tz-aware

        offset = int(dt.utcoffset().total_seconds() / 60)
        is_dst = 1 if dt.dst() else 0

        dt = SimpleNamespace(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            second=dt.second,
            offset=offset,
            is_dst=is_dst
        )

    req = camera.SetLocalDateTime(dt)
    msg = camera.proceed_agw_test(req, cfg)

    # Response ID 확인
    assert msg['responseId'] == camera.CommandId.SET_LOCAL_DATE_TIME

    # Status 확인
    assert msg['status'] == 0


def namespace_to_datetime(ns):
    if hasattr(ns, 'offset'):
        return datetime(
            year=ns.year, month=ns.month, day=ns.day,
            hour=ns.hour, minute=ns.minute, second=ns.second,
            tzinfo=timezone(timedelta(minutes=ns.offset))
        ).astimezone()
    else:
        return datetime(
            year=ns.year, month=ns.month, day=ns.day,
            hour=ns.hour, minute=ns.minute, second=ns.second
        ).astimezone()

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

    set_date_time(cfg, earlier)

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
    set_date_time(cfg, dt)

    # 업데이트된 시각 요청
    dt3 = get_date_time(cfg)
    print(f'Final Camera Date={dt3} {dt3.__dict__}')


def test_utc_vs_local_time_difference(cfg):
    utc_now = datetime.now(timezone.utc)
    print(f'{utc_now=}')
    local_now = utc_now.astimezone()  # 시스템 로컬 타임존으로 변환 (aware)
    print(f'{local_now=}')

    offset = (local_now - utc_now).total_seconds()
    print(f'UTC/Local {offset=}')

    set_date_time(cfg, utc_now)
    set_local_time(cfg, local_now)

    utc_from_device = namespace_to_datetime(get_date_time(cfg))
    print(f'GetDateTime={utc_from_device}')
    local_from_device = namespace_to_datetime(get_local_time(cfg))
    print(f'GetLocalTime={local_from_device}')

    measured_offset = (local_from_device - utc_from_device).total_seconds()
    print(f'{measured_offset=} Diff={measured_offset - offset}')
    assert abs(measured_offset - offset) < 2

