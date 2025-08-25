import webview
import os, sys
from pathlib import Path
import json
from types import SimpleNamespace

import traceback, datetime

def _exhook(exctype, value, tb):
    log = Path(os.getenv("LOCALAPPDATA", ".")) / "DashcamRunner_error.log"
    with open(log, "a", encoding="utf-8") as f:
        w.write(f"\n=== {datetime.datetime.now()} ===\n")
        w.write(f"MEIPASS: {getattr(sys, '_MEIPASS', None)}\n")
        w.write("sys.path:\n" + "\n ".join(exctype, value, tb, flie=f))
    traceback.print_exception(exctype, value, tb)

try:
    import web_api
except Exception as e:
    print("import web_api failed:", repr(e))
    traceback.print_exc()
    raise

from adb_bridge import AdbBridge

def load_cfg():
    exe_dir = Path(os.path.dirname(sys.executable))
    src_dir = Path(__file__).resolve().parents[1] /'testrunner/tests/'
    frozen = getattr(sys, 'frozen', False)
    base_dir = exe_dir if frozen else src_dir
    config_path = str((base_dir / 'test_config.json').resolve())
    if not os.path.exists(config_path):
        if frozen:
            from shutil import copy
            src_path = sys._MEIPASS + '/testrunner/tests/test_config.json'
            copy(src_path, config_path)
        else:
            print(f'File not found: {config_path}')
            sys.exit()

    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return SimpleNamespace(**data)
    return {}

cfg = load_cfg()
# print(cfg)
AdbBridge.adb_path = cfg.adb
web_api.config = cfg

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