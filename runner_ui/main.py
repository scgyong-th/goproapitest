import webview
import os, sys
from pathlib import Path

import web_api
from adb_bridge import AdbBridge

def project_root() -> Path:
    # dev: xian/ (runner_ui/main.py의 부모의 부모)
    dev_base = Path(__file__).resolve().parents[1]
    # exe: _MEIPASS (PyInstaller 임시 풀림 폴더)
    return Path(getattr(sys, "_MEIPASS", dev_base))

def resource_path(rel: str) -> str:
    # 항상 절대·정규화 경로를 반환
    return str((project_root() / rel).resolve())

TR_DIR = resource_path('testrunner')
print(f'{TR_DIR=}')
if TR_DIR not in sys.path:
  sys.path.insert(0, TR_DIR)

# Python 쪽에서 파일 선택 다이얼로그 열기
def select_adb():
    result = webview.windows[0].create_file_dialog(webview.OPEN_DIALOG, file_types=['*.exe'])
    return result[0] if result else "선택 취소됨"

# Python → JS API 등록
webApi = web_api.WebApi(resource_path(f'{TR_DIR}/tests'))
webApi.adb = AdbBridge()

# html_path = os.path.abspath('res/main.html')
html_path = resource_path("runner_ui/res/main.html")
print(html_path)

window = webview.create_window(
    "Android Gateway", url=f'file://{html_path}', js_api=webApi, 
    width=640, height=800)
web_api.window = window
webview.start()