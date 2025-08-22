import requests
import threading
import webbrowser
import os, sys, subprocess, shlex
import pytest
# from pytest_html import plugin as pytest_html_plugin
# from pytest_metadata.plugin import MetadataPlugin

import pytest_html.plugin as pytest_html_plugin
import pytest_metadata.plugin as metadata_plugin

window = None

class Tee:
    def __init__(self, window, orig):
        self.window = window
        self.orig = orig
        # pytest가 참조할 수 있는 속성들
        self.encoding = getattr(orig, "encoding", "utf-8")
        self.errors   = getattr(orig, "errors", "replace")

    # 필수: 텍스트 출력
    def write(self, s):
        if not s:
            return 0
        # 원래 콘솔에도 그대로 출력
        self.orig.write(s)
        # 줄 단위로 UI에 전달
        for line in s.splitlines():
            if line.strip():
                self.window.evaluate_js(f"appendLog({line!r})")
        return len(s)

    def flush(self):
        try:
            self.orig.flush()
        except Exception:
            pass

    # pytest/컬러 처리용 TTY 속성들
    def isatty(self):
        try:
            return self.orig.isatty()
        except Exception:
            return False

    def fileno(self):
        # 일부 라이브러리가 fileno()를 호출
        return self.orig.fileno()

    # io.TextIOBase 호환성 (선택적이지만 도움이 됨)
    def readable(self):  return False
    def writable(self):  return True
    def seekable(self):  return False
    def close(self):     pass


class WebApi:
    # pytest_path = '/Users/scgyong/myenv/bin/pytest'
    def __init__(self, tests_path):
        self.tests_path = tests_path
        print(f'{tests_path=}')
    def log(self, *logs):
        print(f'Web: {logs}')
    def get_device_id(self):
        if not self.adb.device:
            return ''
        return f'{self.adb.device} model:{self.adb.model}'
    def connect_agw(self):
        print('connect_agw')
        self.adb.connect()
        if self.adb.device:
            print(f'Device: {self.adb.device} {self.adb.model}')
            self.adb.run_gateway()
        else:
            print('No device')

        return self.get_device_id()
    def get_app_info(self):
        print('in get_app_info()')
        try:
            resp = requests.get('http://localhost:6502/app/info')
            self.app = resp.json()
        except:
            return {"error":"app not ready"}
        print(f'Response of app/info: {resp.json()}')
        return resp.json()

    def connect_ble(self):
        print('in connect_ble()')
        try:
            resp = requests.get('http://localhost:6502/app/connect')
            print(f'Response from SimeHttpServer: {resp.text}')
            resp = requests.get('http://localhost:6502/app/get_hardware_info')
            self.cam = resp.json()
            print(f'Response of get_hardware_info: {resp.json()}')
            return resp.json()
        except:
            return {"error":"app not ready"}
    
    def run_pytest_inprocess(self):
        def target():
            orig_out, orig_err = sys.stdout, sys.stderr
            # stdout/stderr를 Tee로 교체
            orig_out, orig_err = sys.stdout, sys.stderr
            args = [
                self.tests_path,
                "--rootdir", self.tests_path,
                "--confcutdir", self.tests_path,
                "-q", "-v",
                "-p", "pytest_html",
                "-p", "pytest_metadata",
                "--html=results/report.html",
                "--self-contained-html",
                '--metadata', 'Cam Info', str(self.cam),
                '--metadata', 'App Info', str(self.app),
            ]

            print(args)

            sys.stdout = Tee(window, orig_out)
            sys.stderr = Tee(window, orig_err)
            try:
                rc = pytest.main(args, plugins=[
                    pytest_html_plugin,
                    metadata_plugin
                ])
            finally:
                sys.stdout, sys.stderr = orig_out, orig_err
                window.evaluate_js(f"appendLog('[exit code] {rc}')")

        threading.Thread(target=target, daemon=True).start()

    def run_pytest(self):
        self.run_pytest_inprocess()

    def run_pytest_subprocess(self):
        def target():
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            env['PYTHONPATH'] = '.'
            cmd = [
                sys.executable, '-u', '-m', 'pytest', '-q',
                '-v', '--html=results/report.html',
                '--metadata', 'Cam Info', str(self.cam),
                '--metadata', 'App Info', str(self.app),
            ]
            print(f'Command Line: {cmd}')
            process = subprocess.Popen(
                cmd,
                cwd='../testrunner/',
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            for line in process.stdout:
                if window:
                    window.evaluate_js(f"appendLog({repr(line.strip())})")
            process.stdout.close()
            process.wait()
            if window:
                window.evaluate_js(f"appendLog('[exit code] {process.returncode}')")
        threading.Thread(target=target, daemon=True).start()
   
    def show_report(self):
        html_path = os.path.abspath("results/report.html")  # 절대경로로 변환
        webbrowser.open(f"file://{html_path}")