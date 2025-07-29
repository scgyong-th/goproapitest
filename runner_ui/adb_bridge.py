import subprocess
import re

from types import SimpleNamespace

class AdbBridge:
    adb_path = '/Users/scgyong/Library/Android/sdk/platform-tools/adb'

    def __init__(self):
        self.device = None
        self.connect()

    def connect(self):
        self.device = None
        self.model = ''
        result = self.run_sync(['devices', '-l'])
        if result.stderr:
            print(f'Error: {result.stderr}')
            return
        lines = result.stdout.strip().splitlines()
        for line in lines[1:]:
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) < 2 or parts[1] != "device":
                continue
            device_id = parts[0]
            if device_id.startswith('emulator-'):
                continue

            self.device = device_id

            match = re.search(r'^(\S+)\s+device.*\bmodel:(\S+)', line)
            if match:
                self.model = match.group(2)
            break

        if not self.device:
            print('Device not found')
            return
        
        result = self.run_sync([
            '-s', self.device,
            'forward', 'tcp:6502', 'tcp:6502'
        ])
        print(f'Forward result: {result}')

    def run_gateway(self):
        self.run_sync([
            '-s', self.device,
            'shell', 'monkey', '-p', 'com.example.xiangatewaypilot',
            '-c', 'android.intent.category.LAUNCHER', '1'
        ])
        pass

    def run_sync(self, args):
        try:
            print(f'Running {self.adb_path} with {args}')
            completed = subprocess.run(
                [self.adb_path] + args,
                capture_output=True,
                text=True
            )
            return SimpleNamespace({
                "stdout": completed.stdout,
                "stderr": completed.stderr,
                "returncode": completed.returncode
            })
        except Exception as e:
            return SimpleNamespace({
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            })

if __name__ == '__main__':
    AdbBridge()