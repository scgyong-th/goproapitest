import webview
import os

import web_api
from adb_bridge import AdbBridge

# Python 쪽에서 파일 선택 다이얼로그 열기
def select_adb():
    result = webview.windows[0].create_file_dialog(webview.OPEN_DIALOG, file_types=['*.exe'])
    return result[0] if result else "선택 취소됨"

# Python → JS API 등록
webApi = web_api.WebApi()
webApi.adb = AdbBridge()

html_path = os.path.abspath('res/main.html')
print(html_path)

window = webview.create_window(
    "Android Gateway", url=f'file://{html_path}', js_api=webApi, 
    width=1280, height=800)
web_api.window = window
webview.start()