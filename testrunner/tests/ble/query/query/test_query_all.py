import camera

def test_all_setting_values(cfg):
    req = camera.GetSettingValues(0)
    msg = camera.proceed_agw_test(req, cfg)
    tlv = msg['tlv']
    for key in tlv:
        print_key_value(key, tlv[key], camera.SettingId)

def test_all_status_values(cfg):
    req = camera.GetStatusValues(0)
    msg = camera.proceed_agw_test(req, cfg)
    tlv = msg['tlv']
    for key in tlv:
        print_key_value(key, tlv[key], camera.StatusId)

def print_key_value(key, value, clazz):
    try:
        name = clazz(key).name
    except:
        name = 'Unknown'
    print(f'TLV key={name}({key}/0x{key:02x}) {value=}')


# 2025/08/07 16:35
# Parsed Result: {'responseId': 18, 'status': 0, 'tlv': {2: 1, 3: 8, 5: 0, 6: 1, 13: 9, 19: 0, 24: 0, 30: 110, 31: 0, 32: 10, 37: 0, 41: 12, 42: 8, 43: 0, 44: 9, 45: 8, 47: 7, 54: 1, 59: 7, 62: 1200000, 64: 4, 75: 0, 76: 0, 83: 1, 84: 7, 86: 1, 88: 50, 91: 3, 102: 9, 103: 3, 105: 0, 108: 1, 111: 10, 112: 100, 114: 1, 115: 0, 116: 2, 117: 1, 118: 4, 121: 0, 122: 0, 123: 31, 125: 0, 126: 0, 128: 13, 129: 112, 130: 0, 131: 0, 132: 114, 134: 0, 135: 1, 139: 3, 144: 12, 145: 0, 146: 0, 147: 0, 153: 100, 154: 2, 156: 100, 157: 100, 159: 4, 161: 100, 164: 100, 165: 0, 166: 0, 167: 4, 168: 0, 171: 0, 172: 0, 175: 0, 176: 126, 178: 0, 179: 3, 180: 111, 182: 0, 183: 0, 184: 0, 186: 3, 187: 0, 189: 100, 191: 0, 192: 1, 193: 101, 195: 0, 198: 2, 199: 0, 200: 0, 201: 1, 202: 0, 203: 0, 205: 0, 206: 1, 207: 1, 208: 1, 209: 0, 210: 2, 211: 0, 212: 1, 213: 0, 214: 2, 215: 1, 216: 100, 217: 100, 218: 0, 219: 4, 220: 1, 221: 1, 222: 1, 223: 10, 224: 50, 225: 7, 226: 0, 227: 0, 228: 2, 229: 0, 230: 0, 231: 31, 232: 1, 233: 1, 234: 8}}
# TLV key=VIDEO_RESOLUTION(2/0x02) value=1
# TLV key=FRAMES_PER_SECOND(3/0x03) value=8
# TLV key=VIDEO_TIMELAPSE_RATE(5/0x05) value=0
# TLV key=Unknown(6/0x06) value=1
# TLV key=Unknown(13/0x0d) value=9
# TLV key=Unknown(19/0x13) value=0
# TLV key=Unknown(24/0x18) value=0
# TLV key=PHOTO_TIMELAPSE_RATE(30/0x1e) value=110
# TLV key=Unknown(31/0x1f) value=0
# TLV key=NIGHTLAPSE_RATE(32/0x20) value=10
# TLV key=Unknown(37/0x25) value=0
# TLV key=Unknown(41/0x29) value=12
# TLV key=Unknown(42/0x2a) value=8
# TLV key=WEBCAM_DIGITAL_LENSES(43/0x2b) value=0
# TLV key=Unknown(44/0x2c) value=9
# TLV key=Unknown(45/0x2d) value=8
# TLV key=Unknown(47/0x2f) value=7
# TLV key=Unknown(54/0x36) value=1
# TLV key=AUTO_POWER_DOWN(59/0x3b) value=7
# TLV key=Unknown(62/0x3e) value=1200000
# TLV key=Unknown(64/0x40) value=4
# TLV key=Unknown(75/0x4b) value=0
# TLV key=Unknown(76/0x4c) value=0
# TLV key=GPS(83/0x53) value=1
# TLV key=Unknown(84/0x54) value=7
# TLV key=Unknown(86/0x56) value=1
# TLV key=LCD_BRIGHTNESS(88/0x58) value=50
# TLV key=LED(91/0x5b) value=3
# TLV key=Unknown(102/0x66) value=9
# TLV key=Unknown(103/0x67) value=3
# TLV key=Unknown(105/0x69) value=0
# TLV key=VIDEO_ASPECT_RATIO(108/0x6c) value=1
# TLV key=Unknown(111/0x6f) value=10
# TLV key=Unknown(112/0x70) value=100
# TLV key=Unknown(114/0x72) value=1
# TLV key=Unknown(115/0x73) value=0
# TLV key=Unknown(116/0x74) value=2
# TLV key=Unknown(117/0x75) value=1
# TLV key=Unknown(118/0x76) value=4
# TLV key=VIDEO_LENS(121/0x79) value=0
# TLV key=PHOTO_LENS(122/0x7a) value=0
# TLV key=TIMELAPSE_DIGITAL_LENSES(123/0x7b) value=31
# TLV key=PHOTO_OUTPUT(125/0x7d) value=0
# TLV key=Unknown(126/0x7e) value=0
# TLV key=MEDIA_FORMAT(128/0x80) value=13
# TLV key=ANTI_FLICKER(129/0x81) value=112
# TLV key=HYPERSMOOTH(130/0x82) value=0
# TLV key=Unknown(131/0x83) value=0
# TLV key=VIDEO_HORIZON_LEVELING(132/0x84) value=114
# TLV key=PHOTO_HORIZON_LEVELING(134/0x86) value=0
# TLV key=VIDEO_DURATION(135/0x87) value=1
# TLV key=Unknown(139/0x8b) value=3
# TLV key=Unknown(144/0x90) value=12
# TLV key=Unknown(145/0x91) value=0
# TLV key=Unknown(146/0x92) value=0
# TLV key=Unknown(147/0x93) value=0
# TLV key=Unknown(153/0x99) value=100
# TLV key=Unknown(154/0x9a) value=2
# TLV key=Unknown(156/0x9c) value=100
# TLV key=Unknown(157/0x9d) value=100
# TLV key=Unknown(159/0x9f) value=4
# TLV key=Unknown(161/0xa1) value=100
# TLV key=Unknown(164/0xa4) value=100
# TLV key=Unknown(165/0xa5) value=0
# TLV key=Unknown(166/0xa6) value=0
# TLV key=HINDSIGHT(167/0xa7) value=4
# TLV key=SCHEDULED_CAPTURE(168/0xa8) value=0
# TLV key=PHOTO_SINGLE_INTERVAL(171/0xab) value=0
# TLV key=PHOTO_INTERVAL_DURATION(172/0xac) value=0
# TLV key=CONTROL_MODE(175/0xaf) value=0
# TLV key=EASY_MODE_SPEED(176/0xb0) value=126
# TLV key=WIRELESS_BAND(178/0xb2) value=0
# TLV key=STAR_TRAILS_LENGTH(179/0xb3) value=3
# TLV key=SYSTEM_VIDEO_MODE(180/0xb4) value=111
# TLV key=VIDEO_BIT_RATE(182/0xb6) value=0
# TLV key=BIT_DEPTH(183/0xb7) value=0
# TLV key=PROFILES(184/0xb8) value=0
# TLV key=VIDEO_EASY_MODE(186/0xba) value=3
# TLV key=LAPSE_MODE(187/0xbb) value=0
# TLV key=MAX_LENS_MOD(189/0xbd) value=100
# TLV key=MAX_LENS_MOD_ENABLE(191/0xbf) value=0
# TLV key=EASY_NIGHT_PHOTO(192/0xc0) value=1
# TLV key=MULTI_SHOT_ASPECT_RATIO(193/0xc1) value=101
# TLV key=FRAMING(195/0xc3) value=0
# TLV key=Unknown(198/0xc6) value=2
# TLV key=Unknown(199/0xc7) value=0
# TLV key=Unknown(200/0xc8) value=0
# TLV key=Unknown(201/0xc9) value=1
# TLV key=Unknown(202/0xca) value=0
# TLV key=Unknown(203/0xcb) value=0
# TLV key=Unknown(205/0xcd) value=0
# TLV key=Unknown(206/0xce) value=1
# TLV key=Unknown(207/0xcf) value=1
# TLV key=Unknown(208/0xd0) value=1
# TLV key=Unknown(209/0xd1) value=0
# TLV key=Unknown(210/0xd2) value=2
# TLV key=Unknown(211/0xd3) value=0
# TLV key=Unknown(212/0xd4) value=1
# TLV key=Unknown(213/0xd5) value=0
# TLV key=Unknown(214/0xd6) value=2
# TLV key=Unknown(215/0xd7) value=1
# TLV key=CAMERA_VOLUME(216/0xd8) value=100
# TLV key=Unknown(217/0xd9) value=100
# TLV key=Unknown(218/0xda) value=0
# TLV key=SETUP_SCREEN_SAVER(219/0xdb) value=4
# TLV key=Unknown(220/0xdc) value=1
# TLV key=Unknown(221/0xdd) value=1
# TLV key=Unknown(222/0xde) value=1
# TLV key=SETUP_LANGUAGE(223/0xdf) value=10
# TLV key=Unknown(224/0xe0) value=50
# TLV key=Unknown(225/0xe1) value=7
# TLV key=Unknown(226/0xe2) value=0
# TLV key=PHOTO_MODE(227/0xe3) value=0
# TLV key=Unknown(228/0xe4) value=2
# TLV key=Unknown(229/0xe5) value=0
# TLV key=Unknown(230/0xe6) value=0
# TLV key=Unknown(231/0xe7) value=31
# TLV key=VIDEO_FRAMING(232/0xe8) value=1
# TLV key=MULTI_SHOT_FRAMING(233/0xe9) value=1
# TLV key=FRAME_RATE(234/0xea) value=8

# Parsed Result: {'responseId': 19, 'status': 0, 'tlv': {1: 1, 2: 4, 3: 0, 4: 255, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 13: 0, 14: 0, 17: 1, 19: 0, 20: 0, 22: 0, 23: 0, 24: 0, 27: 0, 29: '', 30: 'GP25151895', 31: 1, 33: 0, 34: 515, 35: 1324, 38: 0, 39: 19, 41: 0, 42: 0, 45: 0, 49: 0, 54: 8735358, 55: 1, 56: 4, 58: 0, 59: 0, 60: 500, 61: 2, 65: 0, 66: 0, 67: 0, 68: 1, 69: 1, 70: 93, 74: 0, 75: 0, 76: 0, 77: 0, 81: 1, 82: 1, 83: 1, 85: 0, 86: 0, 88: 0, 89: 12, 90: 1, 91: 0, 93: 655360, 94: 786432, 95: 851968, 96: 1000, 97: 655360, 98: 150994943, 101: 0, 102: 0, 103: 0, 106: 0, 107: 3409224, 108: 0, 109: 0, 110: 0, 111: 1, 112: 0, 113: 0, 114: 0, 115: 0, 116: 0, 117: 15502147, 118: 0, 119: 10}}
# TLV key=BATTERY_PRESENT(1/0x01) value=1
# TLV key=BATTERY_LEVEL_BARS(2/0x02) value=4
# TLV key=Unknown(3/0x03) value=0
# TLV key=Unknown(4/0x04) value=255
# TLV key=IS_OVERHEATING(6/0x06) value=0
# TLV key=IS_BUSY(8/0x08) value=0
# TLV key=QUICK_CAPTURE_ENABLED(9/0x09) value=0
# TLV key=IS_ENCODING(10/0x0a) value=0
# TLV key=LCD_LOCK_ACTIVE(11/0x0b) value=0
# TLV key=ENCODING_DURATION(13/0x0d) value=0
# TLV key=Unknown(14/0x0e) value=0
# TLV key=WIRELESS_ENABLED(17/0x11) value=1
# TLV key=Unknown(19/0x13) value=0
# TLV key=LAST_PAIRING_TYPE(20/0x14) value=0
# TLV key=WIFI_SCAN_STATE(22/0x16) value=0
# TLV key=WIFI_SCAN_COMPLETED_MS(23/0x17) value=0
# TLV key=WIFI_PROVISIONING_STATE(24/0x18) value=0
# TLV key=WIRELESS_REMOTE_CONNECTED(27/0x1b) value=0
# TLV key=CLIENT_WIFI_NAME(29/0x1d) value=''
# TLV key=AP_WIFI_NAME(30/0x1e) value='GP25151895'
# TLV key=NUM_CONNECTED_DEVICES(31/0x1f) value=1
# TLV key=Unknown(33/0x21) value=0
# TLV key=PHOTO_REMAINING(34/0x22) value=515
# TLV key=VIDEO_REMAINING(35/0x23) value=1324
# TLV key=TOTAL_PHOTOS(38/0x26) value=0
# TLV key=TOTAL_VIDEOS(39/0x27) value=19
# TLV key=OTA_UPDATE_STATUS(41/0x29) value=0
# TLV key=OTA_CANCEL_PENDING(42/0x2a) value=0
# TLV key=LOCATE_CAMERA_ACTIVE(45/0x2d) value=0
# TLV key=TIMELAPSE_INTERVAL_COUNTDOWN(49/0x31) value=0
# TLV key=SDCARD_SPACE_KB(54/0x36) value=8735358
# TLV key=PREVIEW_STREAM_SUPPORTED(55/0x37) value=1
# TLV key=WIFI_SIGNAL_BARS(56/0x38) value=4
# TLV key=HILIGHT_COUNT(58/0x3a) value=0
# TLV key=LAST_HILIGHT_TIME_MS(59/0x3b) value=0
# TLV key=STATUS_POLL_INTERVAL_MS(60/0x3c) value=500
# TLV key=Unknown(61/0x3d) value=2
# TLV key=Unknown(65/0x41) value=0
# TLV key=LIVEVIEW_EXPOSURE_Y1(66/0x42) value=0
# TLV key=LIVEVIEW_EXPOSURE_Y2(67/0x43) value=0
# TLV key=GPS_LOCKED(68/0x44) value=1
# TLV key=AP_MODE_ENABLED(69/0x45) value=1
# TLV key=BATTERY_LEVEL_PERCENT(70/0x46) value=93
# TLV key=Unknown(74/0x4a) value=0
# TLV key=DIGITAL_ZOOM_LEVEL(75/0x4b) value=0
# TLV key=Unknown(76/0x4c) value=0
# TLV key=DIGITAL_ZOOM_AVAILABLE(77/0x4d) value=0
# TLV key=IS_5GHZ_AVAILABLE(81/0x51) value=1
# TLV key=IS_SYSTEM_READY(82/0x52) value=1
# TLV key=OTA_BATTERY_OK(83/0x53) value=1
# TLV key=TOO_COLD_TO_RECORD(85/0x55) value=0
# TLV key=CAMERA_ORIENTATION(86/0x56) value=0
# TLV key=ZOOM_WHILE_ENCODING_SUPPORTED(88/0x58) value=0
# TLV key=FLATMODE_ID(89/0x59) value=12
# TLV key=Unknown(90/0x5a) value=1
# TLV key=Unknown(91/0x5b) value=0
# TLV key=VIDEO_PRESET_ID(93/0x5d) value=655360
# TLV key=PHOTO_PRESET_ID(94/0x5e) value=786432
# TLV key=TIMELAPSE_PRESET_ID(95/0x5f) value=851968
# TLV key=PRESET_GROUP_ID(96/0x60) value=1000
# TLV key=CURRENT_PRESET_ID(97/0x61) value=655360
# TLV key=PRESET_STATUS_FLAG(98/0x62) value=150994943
# TLV key=CAPTURE_DELAY_ACTIVE(101/0x65) value=0
# TLV key=Unknown(102/0x66) value=0
# TLV key=Unknown(103/0x67) value=0
# TLV key=VIDEO_HINDSIGHT_ACTIVE(106/0x6a) value=0
# TLV key=Unknown(107/0x6b) value=3409224
# TLV key=SCHEDULED_CAPTURE_SET(108/0x6c) value=0
# TLV key=Unknown(109/0x6d) value=0
# TLV key=BITMASKED_STATUS(110/0x6e) value=0
# TLV key=SDCARD_SPEED_ERROR(111/0x6f) value=1
# TLV key=SDCARD_SPEED_ERROR_COUNT(112/0x70) value=0
# TLV key=TURBO_TRANSFER_ACTIVE(113/0x71) value=0
# TLV key=CAMERA_CONTROL_STATUS(114/0x72) value=0
# TLV key=USB_CONNECTED(115/0x73) value=0
# TLV key=USB_CONTROL_STATE(116/0x74) value=0
# TLV key=SDCARD_TOTAL_CAPACITY_KB(117/0x75) value=15502147
# TLV key=Unknown(118/0x76) value=0
# TLV key=Unknown(119/0x77) value=10