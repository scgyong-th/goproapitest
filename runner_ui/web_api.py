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
    def get_app_info(self):
        print('in get_app_info()')
        try:
            resp = requests.get('http://localhost:6502/app/info')
        except:
            return """{"error":"app not ready"}"""
        print(f'Response of app/info: {resp.json()}')
        return resp.json()

    def connect_ble(self):
        print('in connect_ble()')
        resp = requests.get('http://localhost:6502/app/connect')
        print(f'Response from SimeHttpServer: {resp.text}')
        resp = requests.get('http://localhost:6502/app/get_hardware_info')
        print(f'Response of get_hardware_info: {resp.json()}')
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
