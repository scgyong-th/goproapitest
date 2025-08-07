from enum import IntEnum, StrEnum

class ID2(StrEnum):
    # Services
    GP_0001 = "0001"  # GoPro Wifi Access Point
    GP_0090 = "0090"  # GoPro Camera Management

    # Characteristics
    GP_0002 = "0002"  # WiFi AP SSID
    GP_0003 = "0003"  # WiFi AP Password
    GP_0004 = "0004"  # WiFi AP Power
    GP_0005 = "0005"  # WiFi AP State

    GP_0091 = "0091"  # Network Management Command
    GP_0092 = "0092"  # Network Management Response

    GP_0072 = "0072"  # Command
    GP_0073 = "0073"  # Command Response
    GP_0074 = "0074"  # Settings
    GP_0075 = "0075"  # Settings Response
    GP_0076 = "0076"  # Query
    GP_0077 = "0077"  # Query Response

    # Characteristic Aliases
    CHAR_WiFi_AP_SSID = GP_0002
    CHAR_WiFi_AP_Password = GP_0003
    CHAR_WiFi_AP_Power = GP_0004
    CHAR_WiFi_AP_State = GP_0005

    CHAR_Network_Management_Command = GP_0091
    CHAR_Network_Management_Response = GP_0092

    CHAR_Command = GP_0072
    CHAR_Command_Response = GP_0073
    CHAR_Settings = GP_0074
    CHAR_Settings_Response = GP_0075
    CHAR_Query = GP_0076
    CHAR_Query_Response = GP_0077

    # Service Aliases
    SERVICE_WiFi_Access_Point = GP_0001
    SERVICE_Camera_Management = GP_0090

# Characteristic to Service Mapping
class ID2_map: pass
ID2_map.service = {
        ID2.GP_0002: ID2.GP_0001,
        ID2.GP_0003: ID2.GP_0001,
        ID2.GP_0004: ID2.GP_0001,
        ID2.GP_0005: ID2.GP_0001,

        ID2.GP_0091: ID2.GP_0090,
        ID2.GP_0092: ID2.GP_0090,
}

ID2_map.response = {
        ID2.GP_0091: ID2.GP_0092,
        ID2.GP_0072: ID2.GP_0073,
        ID2.GP_0074: ID2.GP_0075,
        ID2.GP_0076: ID2.GP_0077,
}

class QueryId(IntEnum):
    GET_SETTING_VALUES = 0x12
    GET_STATUS_VALUES = 0x13
    GET_SETTING_CAPABILITIES = 0x32

    REGISTER_SETTING_VALUE_UPDATES = 0x52
    REGISTER_STATUS_VALUE_UPDATES = 0x53
    REGISTER_SETTING_CAPABILITY_UPDATES = 0x62

    UNREGISTER_SETTING_VALUE_UPDATES = 0x72
    UNREGISTER_STATUS_VALUE_UPDATES = 0x73
    UNREGISTER_SETTING_CAPABILITY_UPDATES = 0x82

    ASYNC_SETTING_VALUE_NOTIFICATION = 0x92
    ASYNC_STATUS_VALUE_NOTIFICATION = 0x93
    ASYNC_SETTING_CAPABILITY_NOTIFICATION = 0xA2

class CommandId(IntEnum):
    SET_SHUTTER = 0x01
    SLEEP = 0x05
    SET_DATE_TIME = 0x0D
    GET_DATE_TIME = 0x0E
    SET_LOCAL_DATE_TIME = 0x0F
    GET_LOCAL_DATE_TIME = 0x10
    REBOOT_CAMERA = 0x11
    SET_AP_CONTROL = 0x17
    HILIGHT_MOMENT = 0x18
    GET_HARDWARE_INFO = 0x3C
    LOAD_PRESET_GROUP = 0x3E
    LOAD_PRESET = 0x40
    SET_ANALYTICS = 0x50
    GET_OPEN_GOPRO_VERSION = 0x51
    KEEP_ALIVE = 0x5B

class SettingId(IntEnum):
    VIDEO_RESOLUTION = 0x02
    FRAMES_PER_SECOND = 0x03
    VIDEO_TIMELAPSE_RATE = 0x05
    PHOTO_TIMELAPSE_RATE = 0x1E
    NIGHTLAPSE_RATE = 0x20
    WEBCAM_DIGITAL_LENSES = 0x2B
    AUTO_POWER_DOWN = 0x3B
    GPS = 0x53
    LCD_BRIGHTNESS = 0x58
    LED = 0x5B
    VIDEO_ASPECT_RATIO = 0x6C
    VIDEO_LENS = 0x79
    PHOTO_LENS = 0x7A
    TIMELAPSE_DIGITAL_LENSES = 0x7B
    PHOTO_OUTPUT = 0x7D
    MEDIA_FORMAT = 0x80
    ANTI_FLICKER = 0x81
    HYPERSMOOTH = 0x82
    VIDEO_HORIZON_LEVELING = 0x84
    PHOTO_HORIZON_LEVELING = 0x86
    VIDEO_DURATION = 0x87
    MULTI_SHOT_DURATION = 0x88
    MAX_LENS = 0xA2
    HINDSIGHT = 0xA7
    SCHEDULED_CAPTURE = 0xA8
    PHOTO_SINGLE_INTERVAL = 0xAB
    PHOTO_INTERVAL_DURATION = 0xAC
    VIDEO_PERFORMANCE_MODE = 0xAD
    CONTROL_MODE = 0xAF
    EASY_MODE_SPEED = 0xB0
    ENABLE_NIGHT_PHOTO = 0xB1
    WIRELESS_BAND = 0xB2
    STAR_TRAILS_LENGTH = 0xB3
    SYSTEM_VIDEO_MODE = 0xB4
    VIDEO_BIT_RATE = 0xB6
    BIT_DEPTH = 0xB7
    PROFILES = 0xB8
    VIDEO_EASY_MODE = 0xBA
    LAPSE_MODE = 0xBB
    MAX_LENS_MOD = 0xBD
    MAX_LENS_MOD_ENABLE = 0xBF
    EASY_NIGHT_PHOTO = 0xC0
    MULTI_SHOT_ASPECT_RATIO = 0xC1
    FRAMING = 0xC3
    CAMERA_VOLUME = 0xD8
    SETUP_SCREEN_SAVER = 0xDB
    SETUP_LANGUAGE = 0xDF
    PHOTO_MODE = 0xE3
    VIDEO_FRAMING = 0xE8
    MULTI_SHOT_FRAMING = 0xE9
    FRAME_RATE = 0xEA

Setting_paramBytes = { # 여기에 없는 key 들은 모두 1 byte
    SettingId.PHOTO_TIMELAPSE_RATE: 8,
    SettingId.NIGHTLAPSE_RATE: 8,
    SettingId.SCHEDULED_CAPTURE: 8,
}

class StatusId(IntEnum):
    BATTERY_PRESENT = 0x01
    BATTERY_LEVEL_BARS = 0x02
    IS_OVERHEATING = 0x06
    IS_BUSY = 0x08
    QUICK_CAPTURE_ENABLED = 0x09
    IS_ENCODING = 0x0A
    LCD_LOCK_ACTIVE = 0x0B
    ENCODING_DURATION = 0x0D
    WIRELESS_ENABLED = 0x11
    LAST_PAIRING_TYPE = 0x14
    LAST_PAIRING_TIME_MS = 0x15
    WIFI_SCAN_STATE = 0x16
    WIFI_SCAN_COMPLETED_MS = 0x17
    WIFI_PROVISIONING_STATE = 0x18
    WIRELESS_REMOTE_VERSION = 0x1A
    WIRELESS_REMOTE_CONNECTED = 0x1B
    WIRELESS_PAIRING_STATE = 0x1C
    CLIENT_WIFI_NAME = 0x1D
    AP_WIFI_NAME = 0x1E
    NUM_CONNECTED_DEVICES = 0x1F
    PREVIEW_STREAM_ENABLED = 0x20
    PHOTO_REMAINING = 0x22
    VIDEO_REMAINING = 0x23
    TOTAL_PHOTOS = 0x26
    TOTAL_VIDEOS = 0x27
    OTA_UPDATE_STATUS = 0x29
    OTA_CANCEL_PENDING = 0x2A
    LOCATE_CAMERA_ACTIVE = 0x2D
    TIMELAPSE_INTERVAL_COUNTDOWN = 0x31
    SDCARD_SPACE_KB = 0x36
    PREVIEW_STREAM_SUPPORTED = 0x37
    WIFI_SIGNAL_BARS = 0x38
    HILIGHT_COUNT = 0x3A
    LAST_HILIGHT_TIME_MS = 0x3B
    STATUS_POLL_INTERVAL_MS = 0x3C
    LIVEVIEW_EXPOSURE_Y1 = 0x42
    LIVEVIEW_EXPOSURE_Y2 = 0x43
    GPS_LOCKED = 0x44
    AP_MODE_ENABLED = 0x45
    BATTERY_LEVEL_PERCENT = 0x46
    DIGITAL_ZOOM_LEVEL = 0x4B
    DIGITAL_ZOOM_AVAILABLE = 0x4D
    IS_MOBILE_FRIENDLY = 0x4E
    IS_FIRST_TIME_USE = 0x4F
    IS_5GHZ_AVAILABLE = 0x51
    IS_SYSTEM_READY = 0x52
    OTA_BATTERY_OK = 0x53
    TOO_COLD_TO_RECORD = 0x55
    CAMERA_ORIENTATION = 0x56
    ZOOM_WHILE_ENCODING_SUPPORTED = 0x58
    FLATMODE_ID = 0x59
    VIDEO_PRESET_ID = 0x5D
    PHOTO_PRESET_ID = 0x5E
    TIMELAPSE_PRESET_ID = 0x5F
    PRESET_GROUP_ID = 0x60
    CURRENT_PRESET_ID = 0x61
    PRESET_STATUS_FLAG = 0x62
    LIVE_BURST_REMAINING = 0x63
    TOTAL_LIVE_BURSTS = 0x64
    CAPTURE_DELAY_ACTIVE = 0x65
    LINUX_CORE_ACTIVE = 0x68
    LENS_TYPE = 0x69
    VIDEO_HINDSIGHT_ACTIVE = 0x6A
    SCHEDULED_CAPTURE_SET = 0x6C
    BITMASKED_STATUS = 0x6E
    SDCARD_SPEED_ERROR = 0x6F
    SDCARD_SPEED_ERROR_COUNT = 0x70
    TURBO_TRANSFER_ACTIVE = 0x71
    CAMERA_CONTROL_STATUS = 0x72
    USB_CONNECTED = 0x73
    USB_CONTROL_STATE = 0x74
    SDCARD_TOTAL_CAPACITY_KB = 0x75

# generated from util/possible_setting_value_extractor.py
SettingId_possible_values = {
    0x02: {  # Video Resolution (2)
        1,  # 4K  HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        4,  # 2.7K    HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        6,  # 2.7K 4:3    HERO11BlackMini HERO11Black HERO10Black HERO9Black
        7,  # 1440    HERO9Black
        9,  # 1080    HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        12,  # 720 HERO13Black
        18,  # 4K 4:3  HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        24,  # 5K  HERO9Black
        25,  # 5K 4:3  HERO10Black
        26,  # 5.3K 8:7    HERO11BlackMini HERO11Black
        27,  # 5.3K 4:3    HERO11BlackMini HERO11Black
        28,  # 4K 8:7  HERO11BlackMini HERO11Black
        35,  # 5.3K 21:9   HERO13Black
        36,  # 4K 21:9 HERO13Black
        37,  # 4K 1:1  HERO13Black
        38,  # 900 HERO13Black
        100,  # 5.3K    HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black
        107,  # 5.3K 8:7 V2 HERO13Black HERO12Black
        108,  # 4K 8:7 V2   HERO13Black HERO12Black
        109,  # 4K 9:16 V2  HERO13Black HERO12Black
        110,  # 1080 9:16 V2    HERO13Black HERO12Black
        111,  # 2.7K 4:3 V2 HERO13Black HERO12Black
        112,  # 4K 4:3 V2   HERO13Black
        113,  # 5.3K 4:3 V2 HERO13Black
    },
    0x03: {  # Frames Per Second (3)
        0,  # 240.0   HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        1,  # 120.0   HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        2,  # 100.0   HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        5,  # 60.0    HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        6,  # 50.0    HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        8,  # 30.0    HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        9,  # 25.0    HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        10,  # 24.0    HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        13,  # 200.0   HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        15,  # 400.0   HERO13Black
        16,  # 360.0   HERO13Black
        17,  # 300.0   HERO13Black
    },
    0x05: {  # Video Timelapse Rate (5)
        0,  # 0.5 Seconds HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        1,  # 1 Second    HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        2,  # 2 Seconds   HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        3,  # 5 Seconds   HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        4,  # 10 Seconds  HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        5,  # 30 Seconds  HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        6,  # 60 Seconds  HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        7,  # 2 Minutes   HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        8,  # 5 Minutes   HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        9,  # 30 Minutes  HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        10,  # 60 Minutes  HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        11,  # 3 Seconds   HERO13Black HERO12Black
    },
    0x1E: {  # Photo Timelapse Rate (30)
        11,  # 3 Seconds   HERO13Black HERO12Black
        100,  # 60 Minutes  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        101,  # 30 Minutes  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        102,  # 5 Minutes   HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        103,  # 2 Minutes   HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        104,  # 60 Seconds  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        105,  # 30 Seconds  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        106,  # 10 Seconds  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        107,  # 5 Seconds   HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        108,  # 2 Seconds   HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        109,  # 1 Second    HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        110,  # 0.5 Seconds HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
    },
    0x20: {  # Nightlapse Rate (32)
        4,  # 4 Seconds   HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        5,  # 5 Seconds   HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        10,  # 10 Seconds  HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        15,  # 15 Seconds  HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        20,  # 20 Seconds  HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        30,  # 30 Seconds  HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        100,  # 60 Seconds  HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        120,  # 2 Minutes   HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        300,  # 5 Minutes   HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        1800,  # 30 Minutes  HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        3600,  # 60 Minutes  HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        3601,  # Auto    HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
    },
    0x2B: {  # Webcam Digital Lenses (43)
        0,  # Wide    HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        2,  # Narrow  HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        3,  # Superview   HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        4,  # Linear  HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
    },
    0x3B: {  # Auto Power Down (59)
        0,  # Never   HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        1,  # 1 Min   HERO13Black HERO12Black HERO11BlackMini HERO11Black
        4,  # 5 Min   HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        6,  # 15 Min  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        7,  # 30 Min  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        11,  # 8 Seconds   HERO11BlackMini
        12,  # 30 Seconds  HERO11BlackMini
    },
    0x53: {  # GPS (83)
        0,  # Off HERO13Black HERO11Black HERO10Black HERO9Black
        1,  # On  HERO13Black HERO11Black HERO10Black HERO9Black
    },
    0x58: {  # LCD Brightness (88)
    },
    0x5B: {  # LED (91)
        0,  # Off HERO11BlackMini
        2,  # On  HERO11BlackMini
        3,  # All On  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        4,  # All Off HERO12Black HERO11Black HERO10Black HERO9Black
        5,  # Front Off Only  HERO12Black HERO11Black HERO10Black HERO9Black
        100,  # Back Only   HERO13Black
    },
    0x6C: {  # Video Aspect Ratio (108)
        0,  # 4:3 HERO13Black HERO12Black
        1,  # 16:9    HERO13Black HERO12Black
        3,  # 8:7 HERO13Black HERO12Black
        4,  # 9:16    HERO13Black HERO12Black
        5,  # 21:9    HERO13Black
        6,  # 1:1 HERO13Black
    },
    0x79: {  # Video Lens (121)
        0,  # Wide    HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        2,  # Narrow  HERO13Black HERO10Black HERO9Black
        3,  # Superview   HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        4,  # Linear  HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        7,  # Max SuperView   HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        8,  # Linear + Horizon Leveling   HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        9,  # HyperView   HERO13Black HERO12Black HERO11BlackMini HERO11Black
        10,  # Linear + Horizon Lock   HERO13Black HERO12Black HERO11BlackMini HERO11Black
        11,  # Max HyperView   HERO12Black
        12,  # Ultra SuperView HERO13Black
        13,  # Ultra Wide  HERO13Black
        14,  # Ultra Linear    HERO13Black
        104,  # Ultra HyperView HERO13Black
    },
    0x7A: {  # Photo Lens (122)
        0,  # Wide 12 MP  HERO13Black
        10,  # Linear 12 MP    HERO13Black
        19,  # Narrow  HERO10Black HERO9Black
        27,  # Wide 23 MP  HERO13Black
        28,  # Linear 23 MP    HERO13Black
        31,  # Wide 27 MP  HERO13Black
        32,  # Linear 27 MP    HERO13Black
        38,  # 13MP Linear HERO13Black
        39,  # 13MP Wide   HERO13Black
        40,  # 13MP Ultra Wide HERO13Black
        41,  # Ultra Wide 12 MP    HERO13Black
        44,  # 13MP Ultra Linear   HERO13Black
        100,  # Max SuperView   HERO12Black HERO11Black HERO10Black HERO9Black
        101,  # Wide    HERO12Black HERO11Black HERO10Black HERO9Black
        102,  # Linear  HERO12Black HERO11Black HERO10Black HERO9Black
    },
    0x7B: {  # Time Lapse Digital Lenses (123)
        19,  # Narrow  HERO10Black HERO9Black
        31,  # Wide 27 MP  HERO13Black
        32,  # Linear 27 MP    HERO13Black
        100,  # Max SuperView   HERO10Black
        101,  # Wide    HERO12Black HERO11Black HERO10Black HERO9Black
        102,  # Linear  HERO12Black HERO11Black HERO10Black HERO9Black
    },
    0x7D: {  # Photo Output (125)
        0,  # Standard    HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        1,  # Raw HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        2,  # HDR HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        3,  # SuperPhoto  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
    },
    0x80: {  # Media Format (128)
        13,  # Time Lapse Video    HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        20,  # Time Lapse Photo    HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        21,  # Night Lapse Photo   HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        26,  # Night Lapse Video   HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
    },
    0x86: {  # Anti-Flicker (134)
        0,  # NTSC    HERO13Black
        1,  # PAL HERO13Black
        2,  # 60Hz    HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        3,  # 50Hz    HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
    },
    0x87: {  # Hypersmooth (135)
        0,  # Off HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO10Black HERO9Black
        1,  # Low HERO13Black HERO12Black HERO11BlackMini HERO11Black HERO9Black
        2,  # High    HERO10Black HERO9Black
        3,  # Boost   HERO11BlackMini HERO11Black HERO10Black HERO9Black
        4,  # Auto Boost  HERO13Black HERO12Black HERO11BlackMini HERO11Black
        100,  # Standard    HERO10Black
    },
    0x96: {  # Video Horizon Leveling (150)
        0,  # Off HERO11Black
        2,  # Locked  HERO11Black
    },
    0x97: {  # Photo Horizon Leveling (151)
        0,  # Off HERO11Black
        2,  # Locked  HERO11Black
    },
    0x9C: {  # Video Duration (156)
        1,  # 15 Seconds  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        2,  # 30 Seconds  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        3,  # 1 Minute    HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        4,  # 5 Minutes   HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        5,  # 15 Minutes  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        6,  # 30 Minutes  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        7,  # 1 Hour  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        8,  # 2 Hours HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        9,  # 3 Hours HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        10,  # 5 Seconds   HERO13Black
        100,  # No Limit    HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
    },
    0x9D: {  # Multi Shot Duration (157)
        1,  # 15 Seconds  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        2,  # 30 Seconds  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        3,  # 1 Minute    HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        4,  # 5 Minutes   HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        5,  # 15 Minutes  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        6,  # 30 Minutes  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        7,  # 1 Hour  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        8,  # 2 Hours HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        9,  # 3 Hours HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        100,  # No Limit    HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
    },
    0xA2: {  # Max Lens (162)
        0,  # Off HERO11Black HERO10Black HERO9Black
        1,  # On  HERO11Black HERO10Black HERO9Black
    },
    0xA7: {  # HindSight (167)
        2,  # 15 Seconds  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        3,  # 30 Seconds  HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
        4,  # Off HERO13Black HERO12Black HERO11Black HERO10Black HERO9Black
    },
    0xA8: {  # Scheduled Capture (168)
        0,  # Is Scheduled Capture Enabled?   1
        1,  # Is 24 hour format?  1
    },
    0xAB: {  # Photo Single Interval (171)
        0,  # Off HERO13Black HERO12Black
        2,  # 0.5s    HERO13Black HERO12Black
        3,  # 1s  HERO13Black HERO12Black
        4,  # 2s  HERO13Black HERO12Black
        5,  # 5s  HERO13Black HERO12Black
        6,  # 10s HERO13Black HERO12Black
        7,  # 30s HERO13Black HERO12Black
        8,  # 60s HERO13Black HERO12Black
        9,  # 120s    HERO13Black HERO12Black
        10,  # 3s  HERO13Black HERO12Black
    },
    0xAC: {  # Photo Interval Duration (172)
        0,  # Off HERO13Black HERO12Black
        1,  # 15 Seconds  HERO13Black HERO12Black
        2,  # 30 Seconds  HERO13Black HERO12Black
        3,  # 1 Minute    HERO13Black HERO12Black
        4,  # 5 Minutes   HERO13Black HERO12Black
        5,  # 15 Minutes  HERO13Black HERO12Black
        6,  # 30 Minutes  HERO13Black HERO12Black
        7,  # 1 Hour  HERO13Black HERO12Black
        8,  # 2 Hours HERO13Black HERO12Black
        9,  # 3 Hours HERO13Black HERO12Black
    },
    0xAD: {  # Video Performance Mode (173)
        0,  # Maximum Video Performance   HERO10Black
        1,  # Extended Battery    HERO10Black
        2,  # Tripod / Stationary Video   HERO10Black
    },
    0xAF: {  # Control Mode (175)
        0,  # Easy    HERO13Black HERO12Black HERO11Black
        1,  # Pro HERO13Black HERO12Black HERO11Black
    },
    0xB0: {  # Easy Mode Speed (176)
        0,  # 8X Ultra Slo-Mo HERO11Black
        1,  # 4X Super Slo-Mo HERO11Black
        2,  # 2X Slo-Mo   HERO11Black
        3,  # 1X Speed (Low Light)    HERO11Black
        4,  # 4X Super Slo-Mo (Ext. Batt.)    HERO11Black
        5,  # 2X Slo-Mo (Ext. Batt.)  HERO11Black
        6,  # 1X Speed (Ext. Batt.) (Low Light)   HERO11Black
        7,  # 8X Ultra Slo-Mo (50Hz)  HERO11Black
        8,  # 4X Super Slo-Mo (50Hz)  HERO11Black
        9,  # 2X Slo-Mo (50Hz)    HERO11Black
        10,  # 1X Speed (50Hz) (Low Light) HERO11Black
        11,  # 4X Super Slo-Mo (50Hz) (Ext. Batt.) HERO11Black
        12,  # 2X Slo-Mo (50Hz) (Ext. Batt.)   HERO11Black
        13,  # 1X Speed (50Hz) (Ext. Batt.) (Low Light)    HERO11Black
        14,  # 8X Ultra Slo-Mo (Ext. Batt.)    HERO11Black
        15,  # 8X Ultra Slo-Mo (50Hz) (Ext. Batt.) HERO11Black
        16,  # 8X Ultra Slo-Mo (Long. Batt.)   HERO11Black
        17,  # 4X Super Slo-Mo (Long. Batt.)   HERO11Black
        18,  # 2X Slo-Mo (Long. Batt.) HERO11Black
        19,  # 1X Speed (Long. Batt.) (Low Light)  HERO11Black
        20,  # 8X Ultra Slo-Mo (50Hz) (Long. Batt.)    HERO11Black
        21,  # 4X Super Slo-Mo (50Hz) (Long. Batt.)    HERO11Black
        22,  # 2X Slo-Mo (50Hz) (Long. Batt.)  HERO11Black
        23,  # 1X Speed (50Hz) (Long. Batt.) (Low Light)   HERO11Black
        24,  # 2X Slo-Mo (4K)  HERO11Black
        25,  # 4X Super Slo-Mo (2.7K)  HERO11Black
        26,  # 2X Slo-Mo (4K) (50Hz)   HERO11Black
        27,  # 4X Super Slo-Mo (2.7K) (50Hz)   HERO11Black
        100,  # 8X Ultra Slo-Mo (V2)    HERO13Black HERO12Black
        101,  # 4X Super Slo-Mo (V2)    HERO13Black HERO12Black
        102,  # 2X Slo-Mo (V2)  HERO13Black HERO12Black
        103,  # 1X Speed (Low Light) (V2)   HERO13Black HERO12Black
        104,  # 8X Ultra Slo-Mo (50Hz) (V2) HERO13Black HERO12Black
        105,  # 4X Super Slo-Mo (50Hz) (V2) HERO13Black HERO12Black
        106,  # 2X Slo-Mo (50Hz) (V2)   HERO13Black HERO12Black
        107,  # 1X Speed (50Hz) (Low Light) (V2)    HERO13Black HERO12Black
        108,  # 8X Ultra Slo-Mo (Long. Batt.) (V2)  HERO13Black HERO12Black
        109,  # 4X Super Slo-Mo (Long. Batt.) (V2)  HERO13Black HERO12Black
        110,  # 2X Slo-Mo (Long. Batt.) (V2)    HERO13Black HERO12Black
        111,  # 1X Speed (Long. Batt.) (Low Light) (V2) HERO13Black HERO12Black
        112,  # 8X Ultra Slo-Mo (50Hz) (Long. Batt.) (V2)   HERO13Black HERO12Black
        113,  # 4X Super Slo-Mo (50Hz) (Long. Batt.) (V2)   HERO13Black HERO12Black
        114,  # 2X Slo-Mo (50Hz) (Long. Batt.) (V2) HERO13Black HERO12Black
        115,  # 1X Speed (50Hz) (Long. Batt.) (Low Light) (V2)  HERO13Black HERO12Black
        116,  # 2X Slo-Mo (4K) (V2) HERO13Black HERO12Black
        117,  # 2X Slo-Mo (4K) (50Hz) (V2)  HERO13Black HERO12Black
        118,  # 1X Speed (Low Light) (V2) (Vertical)    HERO13Black HERO12Black
        119,  # 1X Speed (50Hz) (Low Light) (V2) (Vertical) HERO13Black HERO12Black
        120,  # 2X Slo-Mo (V2) (Vertical)   HERO13Black HERO12Black
        121,  # 2X Slo-Mo (50Hz) (V2) (Vertical)    HERO13Black HERO12Black
        122,  # 1X Speed (Full Frame) (Low Light) (V2)  HERO13Black HERO12Black
        123,  # 1X Speed (50Hz) (Full Frame) (Low Light) (V2)   HERO13Black HERO12Black
        124,  # 2X Slo-Mo (Full Frame) (V2) HERO13Black HERO12Black
        125,  # 2X Slo-Mo (50Hz) (Full Frame) (V2)  HERO13Black HERO12Black
        126,  # 1X Speed (4K) (Low Light) (V2)  HERO13Black HERO12Black
        127,  # 1X Speed (4K) (50Hz) (Low Light) (V2)   HERO13Black HERO12Black
        128,  # 1X Speed (2.7K) (Low Light) (V2)    HERO12Black
        129,  # 1X Speed (2.7K) (50Hz) (Low Light) (V2) HERO12Black
        130,  # 2X Slo-Mo (2.7K) (V2)   HERO12Black
        131,  # 2X Slo-Mo (2.7K) (50Hz) (V2)    HERO12Black
        132,  # 2X Slo-Mo (Long. Batt.) (V2) (Vertical) HERO13Black HERO12Black
        133,  # 2X Slo-Mo (50Hz) (Long. Batt.) (V2) (Vertical)  HERO13Black HERO12Black
        134,  # 1X Speed (Long. Batt.) (Low Light) (V2) (Vertical)  HERO13Black HERO12Black
        135,  # 1X Speed (50Hz) (Long. Batt.) (Low Light) (V2) (Vertical)   HERO13Black HERO12Black
        136,  # 1X Speed (4K) (Full Frame) (Low Light) (V2) HERO13Black HERO12Black
        137,  # 1X Speed (4K) (50Hz) (Full Frame) (Low Light) (V2)  HERO13Black HERO12Black
        138,  # 1X Normal Speed (1:1) (30 Fps) (4K) (V2)    HERO13Black
        139,  # 1X Normal Speed (1:1) (25 Fps) (4K) (V2)    HERO13Black
        140,  # 2X Slo-Mo Speed (1:1) (4K) (60 Fps) (V2)    HERO13Black
        141,  # 2X Slo-Mo Speed (1:1) (4K) (50 Fps) (V2)    HERO13Black
        142,  # 1X Normal Speed (21:9) (30 Fps) (5.3K) (V2) HERO13Black
        143,  # 1X Normal Speed (21:9) (25 Fps) (5.3K) (V2) HERO13Black
        144,  # 2X Slo-Mo Speed (21:9) (5.3K) (60 Fps) (V2) HERO13Black
        145,  # 2X Slo-Mo Speed (21:9) (5.3K) (50 Fps) (V2) HERO13Black
        146,  # 1X Normal Speed (21:9) (30 Fps) (4K) (V2)   HERO13Black
        147,  # 1X Normal Speed (21:9) (25 Fps) (4K) (V2)   HERO13Black
        148,  # 2X Slo-Mo Speed (21:9) (4K) (60 Fps) (V2)   HERO13Black
        149,  # 2X Slo-Mo Speed (21:9) (4K) (50 Fps) (V2)   HERO13Black
        150,  # 120 4X Super Slo-Mo Speed (21:9) (4K) (V2)  HERO13Black
        151,  # 100 4X Super Slo-Mo Speed (21:9) (4K) (V2)  HERO13Black
        152,  # 1X Normal Speed (30 Fps) (4:3) (5.3K) (V2)  HERO13Black
        153,  # 1X Normal Speed (25 Fps) (4:3) (5.3K) (V2)  HERO13Black
        154,  # 1X Normal Speed (30 Fps) (4:3) (4K) (V2)    HERO13Black
        155,  # 1X Normal Speed (25 Fps) (4:3) (4K) (V2)    HERO13Black
        156,  # 2X Slo-Mo Speed (4:3) (4K) (60 Fps) (V2)    HERO13Black
        157,  # 2X Slo-Mo Speed (4:3) (4K) (50 Fps) (V2)    HERO13Black
        158,  # 120 4X Super Slo-Mo Speed (2.7K) (4:3) (V2) HERO13Black
        159,  # 100 4X Super Slo-Mo Speed (2.7K) (4:3) (V2) HERO13Black
    },
    0xB1: {  # Enable Night Photo (177)
        0,  # Off HERO11Black
        1,  # On  HERO11Black
    },
    0xB2: {  # Wireless Band (178)
        0,  # 2.4GHz  HERO13Black HERO12Black HERO11BlackMini HERO11Black
        1,  # 5GHz    HERO13Black HERO12Black HERO11BlackMini HERO11Black
    },
    0xB3: {  # Star Trails Length (179)
        1,  # Short   HERO13Black HERO12Black HERO11BlackMini HERO11Black
        2,  # Long    HERO13Black HERO12Black HERO11BlackMini HERO11Black
        3,  # Max HERO13Black HERO12Black HERO11BlackMini HERO11Black
    },
    0xB4: {  # System Video Mode (180)
        0,  # Highest Quality HERO13Black HERO11Black
        101,  # Extended Battery    HERO11Black
        102,  # Longest Battery HERO11Black
        111,  # Standard Quality    HERO13Black
        112,  # Basic Quality   HERO13Black
    },
    0xB6: {  # Video Bit Rate (182)
        0,  # Standard    HERO13Black HERO12Black
        1,  # High    HERO13Black HERO12Black
    },
    0xB7: {  # Bit Depth (183)
        0,  # 8-Bit   HERO13Black HERO12Black
        2,  # 10-Bit  HERO13Black HERO12Black
    },
    0xB8: {  # Profiles (184)
        0,  # Standard    HERO13Black HERO12Black
        1,  # HDR HERO13Black HERO12Black
        2,  # Log HERO13Black HERO12Black
        101,  # HLG HDR HERO13Black
    },
    0xBA: {  # Video Easy Mode (186)
        0,  # Highest Quality HERO12Black
        1,  # Standard Quality    HERO12Black
        2,  # Basic Quality   HERO12Black
        3,  # Standard Video  HERO13Black
        4,  # HDR Video   HERO13Black
    },
    0xBB: {  # Lapse Mode (187)
        0,  # TimeWarp    HERO13Black HERO12Black
        1,  # Star Trails HERO13Black HERO12Black
        2,  # Light Painting  HERO13Black HERO12Black
        3,  # Vehicle Lights  HERO13Black HERO12Black
        4,  # Max TimeWarp    HERO12Black
        5,  # Max Star Trails HERO12Black
        6,  # Max Light Painting  HERO12Black
        7,  # Max Vehicle Lights  HERO12Black
        8,  # Time Lapse Video    HERO13Black
        9,  # Night Lapse Video   HERO13Black
    },
    0xBD: {  # Max Lens Mod (189)
        0,  # None    HERO12Black
        1,  # Max Lens 1.0    HERO12Black
        2,  # Max Lens 2.0    HERO13Black HERO12Black
        3,  # Max Lens 2.5    HERO13Black
        4,  # Macro   HERO13Black
        5,  # Anamorphic  HERO13Black
        6,  # ND 4    HERO13Black
        7,  # ND 8    HERO13Black
        8,  # ND 16   HERO13Black
        9,  # ND 32   HERO13Black
        10,  # Standard Lens   HERO13Black
        100,  # Auto Detect HERO13Black
    },
    0xBE: {  # Max Lens Mod Enable (190)
        0,  # Off HERO12Black
        1,  # On  HERO12Black
    },
    0xBF: {  # Easy Night Photo (191)
        0,  # Super Photo HERO13Black HERO12Black
        1,  # Night Photo HERO13Black HERO12Black
        2,  # Burst   HERO13Black
    },
    0xC0: {  # Multi Shot Aspect Ratio (192)
        0,  # 4:3 HERO13Black HERO12Black
        1,  # 16:9    HERO13Black HERO12Black
        3,  # 8:7 HERO13Black HERO12Black
        4,  # 9:16    HERO13Black
    },
    0xC1: {  # Framing (193)
        0,  # Widescreen  HERO12Black
        1,  # Vertical    HERO12Black
        2,  # Full Frame  HERO12Black
        100,  # Traditional 4:3 v2  HERO13Black
        101,  # Widescreen 16:9 v2  HERO13Black
        103,  # Full Frame 8:7 v2   HERO13Black
        104,  # Vertical 9:16 v2    HERO13Black
        105,  # Ultra Widescreen 21:9 v2    HERO13Black
        106,  # Full Frame 1:1 v2   HERO13Black
    },
    0xD8: {  # Camera Volume (216)
        70,  # Low HERO13Black
        85,  # Medium  HERO13Black
        100,  # High    HERO13Black
    },
    0xDB: {  # Setup Screen Saver (219)
        1,  # 1 Min   HERO13Black
        2,  # 2 Min   HERO13Black
        3,  # 3 Min   HERO13Black
        4,  # 5 Min   HERO13Black
    },
    0xDF: {  # Setup Language (223)
        0,  # English - US    HERO13Black
        1,  # English - UK    HERO13Black
        2,  # English - AUS   HERO13Black
        3,  # German  HERO13Black
        4,  # French  HERO13Black
        5,  # Italian HERO13Black
        6,  # Spanish HERO13Black
        7,  # Spanish - NA    HERO13Black
        8,  # Chinese HERO13Black
        9,  # Japanese    HERO13Black
        10,  # Korean  HERO13Black
        11,  # Portuguese  HERO13Black
        12,  # Russian HERO13Black
        13,  # English - IND   HERO13Black
        14,  # Swedish HERO13Black
    },
    0xE3: {  # Photo Mode (227)
        0,  # SuperPhoto  HERO13Black
        1,  # Night Photo HERO13Black
        2,  # Burst   HERO13Black
    },
    0xE8: {  # Video Framing (232)
        0,  # 4:3 HERO13Black
        1,  # 16:9    HERO13Black
        3,  # 8:7 HERO13Black
        4,  # 9:16    HERO13Black
        5,  # 21:9    HERO13Black
        6,  # 1:1 HERO13Black
    },
    0xE9: {  # Multi Shot Framing (233)
        0,  # 4:3 HERO13Black
        1,  # 16:9    HERO13Black
        3,  # 8:7 HERO13Black
        4,  # 9:16    HERO13Black
    },
    0xEA: {  # Frame Rate (234)
        0,  # 240.0   HERO13Black
        1,  # 120.0   HERO13Black
        2,  # 100.0   HERO13Black
        5,  # 60.0    HERO13Black
        6,  # 50.0    HERO13Black
        8,  # 30.0    HERO13Black
        9,  # 25.0    HERO13Black
        10,  # 24.0    HERO13Black
        13,  # 200.0   HERO13Black
        15,  # 400.0   HERO13Black
        16,  # 360.0   HERO13Black
        17,  # 300.0   HERO13Black
    },
}

# generated from util/possible_value_extractor.py
StatusId_possible_values = {
    0x01: {  # Battery Present (1)
        0,  # False
        1,  # True
    },
    0x02: {  # Internal Battery Bars (2)
        0,  # Zero
        1,  # One
        2,  # Two
        3,  # Three
        4,  # Charging
    },
    0x06: {  # Overheating (6)
        0,  # False
        1,  # True
    },
    0x08: {  # Busy (8)
        0,  # False
        1,  # True
    },
    0x09: {  # Quick Capture (9)
        0,  # False
        1,  # True
    },
    0x0A: {  # Encoding (10)
        0,  # False
        1,  # True
    },
    0x0B: {  # LCD Lock (11)
        0,  # False
        1,  # True
    },
    0x11: {  # Wireless Connections Enabled (17)
        0,  # False
        1,  # True
    },
    0x13: {  # Pairing State (19)
        0,  # Never Started
        1,  # Started
        2,  # Aborted
        3,  # Cancelled
        4,  # Completed
    },
    0x14: {  # Last Pairing Type (20)
        0,  # Not Pairing
        1,  # Pairing App
        2,  # Pairing Remote Control
        3,  # Pairing Bluetooth Device
    },
    0x16: {  # Wifi Scan State (22)
        0,  # Never started
        1,  # Started
        2,  # Aborted
        3,  # Canceled
        4,  # Completed
    },
    0x18: {  # Wifi Provisioning State (24)
        0,  # Never started
        1,  # Started
        2,  # Aborted
        3,  # Canceled
        4,  # Completed
    },
    0x1B: {  # Remote Connected (27)
        0,  # False
        1,  # True
    },
    0x20: {  # Preview Stream (32)
        0,  # False
        1,  # True
    },
    0x21: {  # Primary Storage (33)
        -1,  # Unknown
        0,  # OK
        1,  # SD Card Full
        2,  # SD Card Removed
        3,  # SD Card Format Error
        4,  # SD Card Busy
        8,  # SD Card Swapped
    },
    0x29: {  # OTA (41)
        0,  # Idle
        1,  # Downloading
        2,  # Verifying
        3,  # Download Failed
        4,  # Verify Failed
        5,  # Ready
        6,  # GoPro App Downloading
        7,  # GoPro App Verifying
        8,  # GoPro App Download Failed
        9,  # GoPro App Verify Failed
        10,  # GoPro App Ready
    },
    0x2A: {  # Pending FW Update Cancel (42)
        0,  # False
        1,  # True
    },
    0x2D: {  # Locate (45)
        0,  # False
        1,  # True
    },
    0x37: {  # Preview Stream Available (55)
        0,  # False
        1,  # True
    },
    0x41: {  # Liveview Exposure Select Mode (65)
        0,  # Disabled
        1,  # Auto
        2,  # ISO Lock
        3,  # Hemisphere
    },
    0x44: {  # GPS Lock (68)
        0,  # False
        1,  # True
    },
    0x45: {  # AP Mode (69)
        0,  # False
        1,  # True
    },
    0x4A: {  # Microphone Accessory (74)
        0,  # Accessory not connected
        1,  # Accessory connected
        2,  # Accessory connected and a microphone is plugged into the accessory
    },
    0x4C: {  # Wireless Band (76)
        0,  # 2.4 GHz
        1,  # 5 GHz
    },
    0x4D: {  # Zoom Available (77)
        0,  # False
        1,  # True
    },
    0x4E: {  # Mobile Friendly (78)
        0,  # False
        1,  # True
    },
    0x4F: {  # FTU (79)
        0,  # False
        1,  # True
    },
    0x51: {  # 5GHZ Available (81)
        0,  # False
        1,  # True
    },
    0x52: {  # Ready (82)
        0,  # False
        1,  # True
    },
    0x53: {  # OTA Charged (83)
        0,  # False
        1,  # True
    },
    0x55: {  # Cold (85)
        0,  # False
        1,  # True
    },
    0x56: {  # Rotation (86)
        0,  # 0 degrees (upright)
        1,  # 180 degrees (upside down)
        2,  # 90 degrees (laying on right side)
        3,  # 270 degrees (laying on left side)
    },
    0x58: {  # Zoom while Encoding (88)
        0,  # False
        1,  # True
    },
    0x65: {  # Capture Delay Active (101)
        0,  # False
        1,  # True
    },
    0x66: {  # Media Mod State (102)
        0,  # Microphone removed
        2,  # Microphone only
        3,  # Microphone with external microphone
    },
    0x67: {  # Time Warp Speed (103)
        0,  # 15x
        1,  # 30x
        2,  # 60x
        3,  # 150x
        4,  # 300x
        5,  # 900x
        6,  # 1800x
        7,  # 2x
        8,  # 5x
        9,  # 10x
        10,  # Auto
        11,  # 1x (realtime)
        12,  # 1/2x (slow-motion)
    },
    0x68: {  # Linux Core (104)
        0,  # False
        1,  # True
    },
    0x69: {  # Lens Type (105)
        0,  # Default
        1,  # Max Lens
        2,  # Max Lens 2.0
        3,  # Max Lens 2.5
        4,  # Macro Lens
        5,  # Anamorphic Lens
        6,  # Neutral Density 4
        7,  # Neutral Density 8
        8,  # Neutral Density 16
        9,  # Neutral Density 32
    },
    0x6A: {  # Hindsight (106)
        0,  # False
        1,  # True
    },
    0x6C: {  # Scheduled Capture (108)
        0,  # False
        1,  # True
    },
    0x6E: {  # Display Mod Status (110)
        0,  # 000 = Display Mod: 0, HDMI: 0, Display Mod Connected: False
        1,  # 001 = Display Mod: 0, HDMI: 0, Display Mod Connected: True
        2,  # 010 = Display Mod: 0, HDMI: 1, Display Mod Connected: False
        3,  # 011 = Display Mod: 0, HDMI: 1, Display Mod Connected: True
        4,  # 100 = Display Mod: 1, HDMI: 0, Display Mod Connected: False
        5,  # 101 = Display Mod: 1, HDMI: 0, Display Mod Connected: True
        6,  # 110 = Display Mod: 1, HDMI: 1, Display Mod Connected: False
        7,  # 111 = Display Mod: 1, HDMI: 1, Display Mod Connected: True
    },
    0x6F: {  # SD Card Write Speed Error (111)
        0,  # False
        1,  # True
    },
    0x71: {  # Turbo Transfer (113)
        0,  # False
        1,  # True
    },
    0x72: {  # Camera Control ID (114)
        0,  # Camera Idle: No one is attempting to change camera settings
        1,  # Camera Control: Camera is in a menu or changing settings. To intervene, app must request control
        2,  # Camera External Control: An outside entity (app) has control and is in a menu or modifying settings
    },
    0x73: {  # USB Connected (115)
        0,  # False
        1,  # True
    },
    0x74: {  # USB Controlled (116)
        0,  # Disabled
        1,  # Enabled
    },
}
