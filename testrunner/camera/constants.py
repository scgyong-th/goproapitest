
class ID2:
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
    service = {
        GP_0002: GP_0001,
        GP_0003: GP_0001,
        GP_0004: GP_0001,
        GP_0005: GP_0001,

        GP_0091: GP_0090,
        GP_0092: GP_0090,
    }

    response = {
        GP_0091: GP_0092,
        GP_0072: GP_0073,
        GP_0074: GP_0075,
        GP_0076: GP_0077,
    }

class QueryId:
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

class CommandId:
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

class SettingId:
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

class StatusId:
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


# generated from util/possible_value_extractor.py
StatusId.possible_values = {
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
