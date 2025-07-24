import requests

class WebApi:
    def log(self, *logs):
        print(f'Web: {logs}')
    def get_device_id(self):
        return self.adb.device
    def connect_agw(self):
        self.adb.connect()
        if self.adb.device:
            print(f'Device: {self.adb.device}')
            self.adb.run_gateway()
        else:
            print('No device')

        return self.adb.device

    def connect_ble(self):
        resp = requests.get('http://localhost:6502/app/connect')
        print(f'Response from SimeHttpServer: {resp}')
        resp = requests.get('http://localhost:6502/app/get_hardware_info')
        return resp.json()
    # def run_adb(self, args):
    #     try:
    #         completed = subprocess.run(
    #             [self.adb_path] + args,
    #             capture_output=True,
    #             text=True
    #         )
    #         return {
    #             "stdout": completed.stdout,
    #             "stderr": completed.stderr,
    #             "returncode": completed.returncode
    #         }
    #     except Exception as e:
    #         return {
    #             "stdout": "",
    #             "stderr": str(e),
    #             "returncode": -1
    #         }
