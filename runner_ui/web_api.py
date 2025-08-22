import requests
import threading
import webbrowser
import os, sys, subprocess, shlex

window = None

class WebApi:
    # pytest_path = '/Users/scgyong/myenv/bin/pytest'
    def __init__(self):
        # self.window = None
        pass
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
    
    def run_pytest(self):
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
        html_path = os.path.abspath("../testrunner/results/report.html")  # 절대경로로 변환
        webbrowser.open(f"file://{html_path}")