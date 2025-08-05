import camera
import pytest
@pytest.mark.parametrize("ids", [
    camera.StatusId.BATTERY_PRESENT,
    camera.StatusId.BATTERY_LEVEL_BARS,
    bytes([camera.StatusId.WIFI_SCAN_STATE, camera.StatusId.BATTERY_LEVEL_BARS]),
    bytes([
        camera.StatusId.USB_CONNECTED,
        camera.StatusId.PHOTO_REMAINING
    ]),
    bytes([
        camera.StatusId.TOTAL_PHOTOS,
        camera.StatusId.TOTAL_VIDEOS,
        camera.StatusId.TIMELAPSE_INTERVAL_COUNTDOWN,
        camera.StatusId.SDCARD_SPACE_KB,
    ]),
    bytes([
        camera.StatusId.PREVIEW_STREAM_SUPPORTED,
        camera.StatusId.WIFI_SIGNAL_BARS,
        camera.StatusId.VIDEO_HINDSIGHT_ACTIVE,
        camera.StatusId.GPS_LOCKED,
        camera.StatusId.AP_MODE_ENABLED,
    ]),
    bytes([
        camera.StatusId.BATTERY_LEVEL_PERCENT,
        camera.StatusId.DIGITAL_ZOOM_LEVEL,
        camera.StatusId.DIGITAL_ZOOM_AVAILABLE,
        camera.StatusId.IS_5GHZ_AVAILABLE,
    ]),
    bytes([
        camera.StatusId.IS_SYSTEM_READY,
        camera.StatusId.OTA_BATTERY_OK,
        camera.StatusId.TOO_COLD_TO_RECORD,
        camera.StatusId.CAMERA_ORIENTATION,
        camera.StatusId.ZOOM_WHILE_ENCODING_SUPPORTED,
        camera.StatusId.FLATMODE_ID,
        camera.StatusId.VIDEO_PRESET_ID,
    ]),
])
def test_status_values(cfg, ids):
    req = camera.GetStatusValues(ids)
    msg = camera.proceed_agw_test(req, cfg)
    if isinstance(ids, int):
        key = ids
    else:
        for key in ids:
            assert key in msg['tlv'], f'{key=:02x}'
            if key in msg['tlv']:
                print_key_value(key, msg['tlv'][key])

def print_key_value(key, value):
    print(f'TLV {key=:02x} {value=}')