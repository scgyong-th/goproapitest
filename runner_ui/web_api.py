import webview
import subprocess
import sys
import os

class WebApi:
    def log(self, *logs):
        print(f'Web: {logs}')
    def get_device_id(self):
        return self.adb.device


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
