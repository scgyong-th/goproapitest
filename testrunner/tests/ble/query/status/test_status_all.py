import requests
import camera

statusId = 0xFF

def test_query_status_all(cfg):
    # 1. 요청 객체 생성
    req = camera.QueryRequest(
        camera.QueryId.GET_STATUS_VALUES, 
        statusId,
        None)
    msg = camera.proceed_agw_test(req, cfg)

    # Response ID 확인
    assert msg['responseId'] == camera.QueryId.GET_STATUS_VALUES

    # Status 확인
    assert msg['status'] == 0

    for t, v in msg['tlv'].items():
        name = get_status_name(t)
        print(f'StatusId[{name}({t}/0x{t:02X})] = {v}')

def get_status_name(value):
    for k, v in vars(camera.StatusId).items():
        if not k.startswith("__") and v == value:
            return k
    return None

# run output on 25/07/21 23:12:23
# StatusId[BATTERY_PRESENT(1/0x01)] = 1
# StatusId[BATTERY_LEVEL_BARS(2/0x02)] = 1
# StatusId[None(3/0x03)] = 0
# StatusId[None(4/0x04)] = 255
# StatusId[IS_OVERHEATING(6/0x06)] = 0
# StatusId[IS_BUSY(8/0x08)] = 0
# StatusId[QUICK_CAPTURE_ENABLED(9/0x09)] = 0
# StatusId[IS_ENCODING(10/0x0A)] = 0
# StatusId[LCD_LOCK_ACTIVE(11/0x0B)] = 0
# StatusId[ENCODING_DURATION(13/0x0D)] = 0
# StatusId[None(14/0x0E)] = 0
# StatusId[WIRELESS_ENABLED(17/0x11)] = 1
# StatusId[None(19/0x13)] = 0
# StatusId[LAST_PAIRING_TYPE(20/0x14)] = 0
# StatusId[WIFI_SCAN_STATE(22/0x16)] = 0
# StatusId[WIFI_SCAN_COMPLETED_MS(23/0x17)] = 0
# StatusId[WIFI_PROVISIONING_STATE(24/0x18)] = 0
# StatusId[WIRELESS_REMOTE_CONNECTED(27/0x1B)] = 0
# StatusId[CLIENT_WIFI_NAME(29/0x1D)] = b''
# StatusId[AP_WIFI_NAME(30/0x1E)] = GP25151895
# StatusId[NUM_CONNECTED_DEVICES(31/0x1F)] = 0
# StatusId[None(33/0x21)] = 0
# StatusId[PHOTO_REMAINING(34/0x22)] = 909
# StatusId[VIDEO_REMAINING(35/0x23)] = 2339
# StatusId[TOTAL_PHOTOS(38/0x26)] = 0
# StatusId[TOTAL_VIDEOS(39/0x27)] = 0
# StatusId[OTA_UPDATE_STATUS(41/0x29)] = 0
# StatusId[OTA_CANCEL_PENDING(42/0x2A)] = 0
# StatusId[LOCATE_CAMERA_ACTIVE(45/0x2D)] = 0
# StatusId[TIMELAPSE_INTERVAL_COUNTDOWN(49/0x31)] = 0
# StatusId[SDCARD_SPACE_KB(54/0x36)] = 15434776
# StatusId[PREVIEW_STREAM_SUPPORTED(55/0x37)] = 1
# StatusId[WIFI_SIGNAL_BARS(56/0x38)] = 4
# StatusId[HILIGHT_COUNT(58/0x3A)] = 0
# StatusId[LAST_HILIGHT_TIME_MS(59/0x3B)] = 0
# StatusId[STATUS_POLL_INTERVAL_MS(60/0x3C)] = 500
# StatusId[None(61/0x3D)] = 2
# StatusId[None(65/0x41)] = 0
# StatusId[LIVEVIEW_EXPOSURE_Y1(66/0x42)] = 0
# StatusId[LIVEVIEW_EXPOSURE_Y2(67/0x43)] = 0
# StatusId[GPS_LOCKED(68/0x44)] = 0
# StatusId[AP_MODE_ENABLED(69/0x45)] = 1
# StatusId[BATTERY_LEVEL_PERCENT(70/0x46)] = 39
# StatusId[None(74/0x4A)] = 0
# StatusId[DIGITAL_ZOOM_LEVEL(75/0x4B)] = 0
# StatusId[None(76/0x4C)] = 0
# StatusId[DIGITAL_ZOOM_AVAILABLE(77/0x4D)] = 0
# StatusId[IS_5GHZ_AVAILABLE(81/0x51)] = 1
# StatusId[IS_SYSTEM_READY(82/0x52)] = 1
# StatusId[OTA_BATTERY_OK(83/0x53)] = 1
# StatusId[TOO_COLD_TO_RECORD(85/0x55)] = 0
# StatusId[CAMERA_ORIENTATION(86/0x56)] = 2
# StatusId[ZOOM_WHILE_ENCODING_SUPPORTED(88/0x58)] = 0
# StatusId[FLATMODE_ID(89/0x59)] = 12
# StatusId[None(90/0x5A)] = 1
# StatusId[None(91/0x5B)] = 0
# StatusId[VIDEO_PRESET_ID(93/0x5D)] = 655360
# StatusId[PHOTO_PRESET_ID(94/0x5E)] = 786432
# StatusId[TIMELAPSE_PRESET_ID(95/0x5F)] = 851968
# StatusId[PRESET_GROUP_ID(96/0x60)] = 1000
# StatusId[CURRENT_PRESET_ID(97/0x61)] = 655360
# StatusId[PRESET_STATUS_FLAG(98/0x62)] = 150994943
# StatusId[CAPTURE_DELAY_ACTIVE(101/0x65)] = 0
# StatusId[None(102/0x66)] = 0
# StatusId[None(103/0x67)] = 0
# StatusId[VIDEO_HINDSIGHT_ACTIVE(106/0x6A)] = 0
# StatusId[None(107/0x6B)] = 3409224
# StatusId[SCHEDULED_CAPTURE_SET(108/0x6C)] = 0
# StatusId[None(109/0x6D)] = 0
# StatusId[BITMASKED_STATUS(110/0x6E)] = 0
# StatusId[SDCARD_SPEED_ERROR(111/0x6F)] = 1
# StatusId[SDCARD_SPEED_ERROR_COUNT(112/0x70)] = 0
# StatusId[TURBO_TRANSFER_ACTIVE(113/0x71)] = 0
# StatusId[CAMERA_CONTROL_STATUS(114/0x72)] = 0
# StatusId[USB_CONNECTED(115/0x73)] = 0
# StatusId[USB_CONTROL_STATE(116/0x74)] = 0
# StatusId[SDCARD_TOTAL_CAPACITY_KB(117/0x75)] = 15502147
# StatusId[None(118/0x76)] = 0
# StatusId[None(119/0x77)] = 10
