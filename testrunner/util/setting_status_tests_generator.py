import json
import os
import shutil

import sys, os
sys.path.insert(0, 
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from special_cases import cases

import camera
# 1. camera 모듈의 Enum 정의를 가져오기 (예: JSON 또는 직접 import)
from camera import SettingId, StatusId

# 2. ID 목록 수집
settings = {name.lower(): name for name in dir(SettingId) if not name.startswith("_")}
statuses = {name.lower(): name for name in dir(StatusId) if not name.startswith("_")}

# 3. 템플릿
setting_template = """import pytest
import camera
from camera import SettingId, QueryRequest, QueryId

def test_setting_{name}(cfg):
    req = QueryRequest(QueryId.GET_SETTING_VALUES, SettingId.{const}, None)
    msg = camera.proceed_agw_test(req, cfg)

    assert msg["responseId"] == QueryId.GET_SETTING_VALUES
    assert msg["status"] == 0
    assert SettingId.{const} in msg["tlv"]

    value = msg["tlv"][SettingId.{const}][0]
    #assert len(msg['tlv'][SettingId.{const}]) == 1
    print("Setting {const} =", value)

    # TODO: Add valid value checks specific to {const}
"""

status_template = """import pytest
import camera
from camera import StatusId, QueryRequest, QueryId

def test_status_{name}(cfg):
    req = QueryRequest(QueryId.GET_STATUS_VALUES, StatusId.{const}, None)
    msg = camera.proceed_agw_test(req, cfg)

    assert msg["responseId"] == QueryId.GET_STATUS_VALUES
    assert msg["status"] == 0
    assert StatusId.{const} in msg["tlv"]

    value = msg["tlv"][StatusId.{const}][0]
    #assert len(msg['tlv'][StatusId.{const}]) == 1
    print("Status {const} =", value)

    # TODO: Add valid value checks specific to {const}
"""

# 4. 디렉토리 생성
base_dir = "../tests/ble/query/generated"

# 디렉토리 전체 삭제 (안에 뭐가 있든 전부)
if os.path.exists(base_dir):
    shutil.rmtree(base_dir)

# 하위 디렉토리 생성
settings_dir = os.path.join(base_dir, "settings")
statuses_dir = os.path.join(base_dir, "statuses")
os.makedirs(settings_dir, exist_ok=True)
os.makedirs(statuses_dir, exist_ok=True)

file_created = 0

# 5. 파일 생성
for name, const in settings.items():
    if const in cases.settings.excludes:
        print(f'excluded: SettingId.{const}')
        continue
    fn = os.path.join(settings_dir, f"test_setting_{name}.py")
    with open(fn, "w", encoding="utf-8") as f:
        f.write(setting_template.format(name=name, const=const))
        file_created += 1

for name, const in statuses.items():
    if const in cases.statuses.excludes:
        print(f'excluded: StatusId.{const}')
        continue
    fn = os.path.join(statuses_dir, f"test_status_{name}.py")
    with open(fn, "w", encoding="utf-8") as f:
        f.write(status_template.format(name=name, const=const))
        file_created += 1

print(f'{file_created} files created')