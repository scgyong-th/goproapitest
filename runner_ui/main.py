import webview
import os, sys

import web_api
from adb_bridge import AdbBridge

def resource_path(rel_path):
    """PyInstaller 환경/개발 환경 둘 다에서 파일 경로 얻기"""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)

# Python 쪽에서 파일 선택 다이얼로그 열기
def select_adb():
    result = webview.windows[0].create_file_dialog(webview.OPEN_DIALOG, file_types=['*.exe'])
    return result[0] if result else "선택 취소됨"

# Python → JS API 등록
webApi = web_api.WebApi()
webApi.adb = AdbBridge()

# html_path = os.path.abspath('res/main.html')
html_path = resource_path("res/main.html")
print(html_path)

window = webview.create_window(
    "Android Gateway", url=f'file://{html_path}', js_api=webApi, 
    width=1280, height=800)
web_api.window = window
webview.start()