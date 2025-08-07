import camera
import pytest
@pytest.mark.parametrize("ids", [
    camera.SettingId.VIDEO_RESOLUTION,
    camera.SettingId.FRAMES_PER_SECOND,
    bytes([
        camera.SettingId.VIDEO_TIMELAPSE_RATE,
        camera.SettingId.PHOTO_TIMELAPSE_RATE,
        camera.SettingId.NIGHTLAPSE_RATE,
    ]), bytes([
        camera.SettingId.WEBCAM_DIGITAL_LENSES,
        camera.SettingId.AUTO_POWER_DOWN,
        camera.SettingId.GPS,
        camera.SettingId.LCD_BRIGHTNESS,
    ]), bytes([
        camera.SettingId.LED,
        camera.SettingId.VIDEO_ASPECT_RATIO,
        camera.SettingId.VIDEO_LENS,
        camera.SettingId.PHOTO_LENS,
        camera.SettingId.TIMELAPSE_DIGITAL_LENSES,
        camera.SettingId.PHOTO_OUTPUT,
        camera.SettingId.MEDIA_FORMAT,
    ]), bytes([
        camera.SettingId.ANTI_FLICKER,
        camera.SettingId.HYPERSMOOTH,
        camera.SettingId.VIDEO_HORIZON_LEVELING,
        camera.SettingId.PHOTO_HORIZON_LEVELING,
        camera.SettingId.VIDEO_DURATION,
        # camera.SettingId.MULTI_SHOT_DURATION,
        # camera.SettingId.MAX_LENS,
    ]), bytes([
        camera.SettingId.HINDSIGHT,
        camera.SettingId.SCHEDULED_CAPTURE,
        camera.SettingId.PHOTO_SINGLE_INTERVAL,
        camera.SettingId.PHOTO_INTERVAL_DURATION,
        # camera.SettingId.VIDEO_PERFORMANCE_MODE,
        camera.SettingId.CONTROL_MODE,
        camera.SettingId.EASY_MODE_SPEED,
        # camera.SettingId.ENABLE_NIGHT_PHOTO,
    ]), bytes([
        camera.SettingId.WIRELESS_BAND,
        camera.SettingId.STAR_TRAILS_LENGTH,
        camera.SettingId.SYSTEM_VIDEO_MODE,
        camera.SettingId.VIDEO_BIT_RATE,
        camera.SettingId.BIT_DEPTH,
        camera.SettingId.PROFILES,
        camera.SettingId.VIDEO_EASY_MODE,
        camera.SettingId.LAPSE_MODE,
        camera.SettingId.MAX_LENS_MOD,
        camera.SettingId.MAX_LENS_MOD_ENABLE,
    ]), bytes([
        camera.SettingId.EASY_NIGHT_PHOTO,
        camera.SettingId.MULTI_SHOT_ASPECT_RATIO,
        camera.SettingId.FRAMING,
        camera.SettingId.CAMERA_VOLUME,
        camera.SettingId.SETUP_SCREEN_SAVER,
        camera.SettingId.SETUP_LANGUAGE,
        camera.SettingId.PHOTO_MODE,
        camera.SettingId.VIDEO_FRAMING,
        camera.SettingId.MULTI_SHOT_FRAMING,
        camera.SettingId.FRAME_RATE,
    ]),
])
def test_setting_values(cfg, ids):
    req = camera.GetSettingValues(ids)
    msg = camera.proceed_agw_test(req, cfg)
    if isinstance(ids, int):
        key = ids
        print_key_value(key, msg['tlv'][key])
    else:
        for key in ids:
            assert key in msg['tlv'], f'{key=:02x}'
            if key in msg['tlv']:
                print_key_value(key, msg['tlv'][key])

def print_key_value(key, value):
    print(f'TLV key={camera.SettingId(key).name}({key}/0x{key:02x}) {value=}')