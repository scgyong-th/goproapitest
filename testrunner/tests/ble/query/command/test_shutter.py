import camera
import time
from types import SimpleNamespace

def test_shutter(cfg):
    req = camera.SetShutter(True)
    msg = camera.proceed_agw_test(req, cfg)

    print(f'Set Shutter On Result={msg}. Sleeping 1 sec.')
    time.sleep(1)
    print(f'After Sleeping 1 sec.')

    req = camera.SetShutter(False)
    msg = camera.proceed_agw_test(req, cfg)

    print(f'Set Shutter Off Result={msg}')


    req = camera.GetLastCapturedMedia()
    msg = camera.proceed_agw_test(req, cfg)
    print(f'Last Captured Media={type(msg)}\n{msg}')
