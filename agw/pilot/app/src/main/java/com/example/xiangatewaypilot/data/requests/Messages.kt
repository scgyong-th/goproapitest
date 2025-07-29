package com.example.xiangatewaypilot.data.requests

import com.example.xiangatewaypilot.constants.ID2
import com.example.xiangatewaypilot.data.responses.GetHardwareInfoResponse
import com.example.xiangatewaypilot.data.responses.NetworkManagementResponse
import com.example.xiangatewaypilot.data.responses.NotifiedResponse
import com.example.xiangatewaypilot.data.responses.QueryResponse
import com.example.xiangatewaypilot.model.main.CharCache
import open_gopro.NetworkManagement
import open_gopro.NetworkManagement.RequestPairingFinish

class GetHardwareInfo(onResponse: (BleRequest, GetHardwareInfoResponse)->Unit) : BleRequest.Write(
    characteristic = CharCache[ID2.CHAR_Command]!!,
    value = byteArrayOf(0x01, CommandId.GET_HARDWARE_INFO),
    onNotifiedResponse = { req, resp -> onResponse(req, resp as GetHardwareInfoResponse) }
) {
    init {
        tryCount = 10
    }
}

class CommandRequest(commandId: Byte, onResponse: ((BleRequest, NotifiedResponse) -> Unit)? = null) : BleRequest.Write(
    characteristic = CharCache[ID2.CHAR_Command]!!,
    value = byteArrayOf(0x01, commandId),
    onNotifiedResponse = onResponse
)

class KeepAliveRequest(onResponse: ((BleRequest, NotifiedResponse) -> Unit)? = null) : BleRequest.Write(
    characteristic = CharCache[ID2.CHAR_Settings]!!,
    //value = byteArrayOf(0x01, CommandId.KEEP_ALIVE),
    value = byteArrayOf(0x03, CommandId.KEEP_ALIVE, 0x01, 0x42),
    onNotifiedResponse = onResponse
)

class GetWifiApSsid(onResponse: (BleRequest, String)->Unit) : BleRequest.Read(
    characteristic = CharCache[ID2.CHAR_WiFi_AP_SSID]!!,
    onResponse = { req, resp -> onResponse(req, String(resp ?: ByteArray(0), Charsets.UTF_8)) }
)

class GetWifiApPassword(onResponse: (BleRequest, String)->Unit) : BleRequest.Read(
    characteristic = CharCache[ID2.CHAR_WiFi_AP_Password]!!,
    onResponse = { req, resp -> onResponse(req, String(resp ?: ByteArray(0), Charsets.UTF_8)) }
)

class SetApControl(enables: Boolean, onResponse: (BleRequest, NotifiedResponse)->Unit) : BleRequest.Write(
    characteristic = CharCache[ID2.CHAR_Command]!!,
    value = byteArrayOf(0x03, CommandId.SET_AP_CONTROL, 0x01, if (enables) 0x01 else 0x00),
    onNotifiedResponse = onResponse
)

class PairingFinishRequest(onResponse: (BleRequest, NetworkManagementResponse) -> Unit) : BleRequest.Write(
    characteristic = CharCache[ID2.CHAR_Network_Management_Command]!!,
    value = byteArrayOf(),
    onNotifiedResponse = { req, resp -> onResponse(req, resp as NetworkManagementResponse) }
) {
    init {
        val protobuf = RequestPairingFinish.newBuilder()
            .setResult(NetworkManagement.EnumPairingFinishState.SUCCESS)
            .setPhoneName("Thinkware AGW")
            .build()
            .toByteArray()
        val featureID = 0x03.toByte()
        val actionID = 0x01.toByte()
        value = byteArrayOf((protobuf.size + 2).toByte(), featureID, actionID) + protobuf
    }
}

class QueryRequest(queryId: Byte, ids: ByteArray, onResponse: (BleRequest, QueryResponse)->Unit) : BleRequest.Write(
    characteristic = CharCache[ID2.CHAR_Query]!!,
    value = byteArrayOf((ids.size + 1).toByte(), queryId) + ids,
    onNotifiedResponse = { req, resp -> onResponse(req, resp as QueryResponse) }
) {
    constructor(
        queryId: Byte,
        id: Byte,
        onResponse: (BleRequest, QueryResponse) -> Unit
    ) : this(queryId, byteArrayOf(id), onResponse)
}

object QueryId {
    const val GET_SETTING_VALUES: Byte = 0x12
    const val GET_STATUS_VALUES: Byte = 0x13
    const val GET_SETTING_CAPABILITIES: Byte = 0x32

    const val REGISTER_SETTING_VALUE_UPDATES: Byte = 0x52
    const val REGISTER_STATUS_VALUE_UPDATES: Byte = 0x53
    const val REGISTER_SETTING_CAPABILITY_UPDATES: Byte = 0x62

    const val UNREGISTER_SETTING_VALUE_UPDATES: Byte = 0x72
    const val UNREGISTER_STATUS_VALUE_UPDATES: Byte = 0x73
    const val UNREGISTER_SETTING_CAPABILITY_UPDATES: Byte = 0x82.toByte()

    const val ASYNC_SETTING_VALUE_NOTIFICATION: Byte = 0x92.toByte()
    const val ASYNC_STATUS_VALUE_NOTIFICATION: Byte = 0x93.toByte()
    const val ASYNC_SETTING_CAPABILITY_NOTIFICATION: Byte = 0xA2.toByte()
}

object CommandId {
    const val SET_SHUTTER: Byte = 0x01
    const val SLEEP: Byte = 0x05
    const val SET_DATE_TIME: Byte = 0x0D
    const val GET_DATE_TIME: Byte = 0x0E
    const val SET_LOCAL_DATE_TIME: Byte = 0x0F
    const val GET_LOCAL_DATE_TIME: Byte = 0x10
    const val REBOOT_CAMERA: Byte = 0x11
    const val SET_AP_CONTROL: Byte = 0x17
    const val HILIGHT_MOMENT: Byte = 0x18
    const val GET_HARDWARE_INFO: Byte = 0x3C
    const val LOAD_PRESET_GROUP: Byte = 0x3E
    const val LOAD_PRESET: Byte = 0x40
    const val SET_ANALYTICS: Byte = 0x50
    const val GET_OPEN_GOPRO_VERSION: Byte = 0x51
    const val KEEP_ALIVE: Byte = 0x5B
}

object SettingId {
    const val VIDEO_RESOLUTION: Byte         = 0x02
    const val FRAMES_PER_SECOND: Byte        = 0x03
    const val VIDEO_TIMELAPSE_RATE: Byte     = 0x05
    const val PHOTO_TIMELAPSE_RATE: Byte     = 0x1E
    const val NIGHTLAPSE_RATE: Byte          = 0x20
    const val WEBCAM_DIGITAL_LENSES: Byte    = 0x2B
    const val AUTO_POWER_DOWN: Byte          = 0x3B
    const val GPS: Byte                      = 0x53
    const val LCD_BRIGHTNESS: Byte           = 0x58
    const val LED: Byte                      = 0x5B
    const val VIDEO_ASPECT_RATIO: Byte       = 0x6C
    const val VIDEO_LENS: Byte               = 0x79
    const val PHOTO_LENS: Byte               = 0x7A
    const val TIMELAPSE_DIGITAL_LENSES: Byte = 0x7B
    const val PHOTO_OUTPUT: Byte             = 0x7D
    const val MEDIA_FORMAT: Byte             = 0x80.toByte()
    const val ANTI_FLICKER: Byte             = 0x81.toByte()
    const val HYPERSMOOTH: Byte              = 0x82.toByte()
    const val VIDEO_HORIZON_LEVELING: Byte   = 0x84.toByte()
    const val PHOTO_HORIZON_LEVELING: Byte   = 0x86.toByte()
    const val VIDEO_DURATION: Byte           = 0x87.toByte()
    const val MULTI_SHOT_DURATION: Byte      = 0x88.toByte()
    const val MAX_LENS: Byte                 = 0xA2.toByte()
    const val HINDSIGHT: Byte                = 0xA7.toByte()
    const val SCHEDULED_CAPTURE: Byte        = 0xA8.toByte()
    const val PHOTO_SINGLE_INTERVAL: Byte    = 0xAB.toByte()
    const val PHOTO_INTERVAL_DURATION: Byte  = 0xAC.toByte()
    const val VIDEO_PERFORMANCE_MODE: Byte   = 0xAD.toByte()
    const val CONTROL_MODE: Byte             = 0xAF.toByte()
    const val EASY_MODE_SPEED: Byte          = 0xB0.toByte()
    const val ENABLE_NIGHT_PHOTO: Byte       = 0xB1.toByte()
    const val WIRELESS_BAND: Byte            = 0xB2.toByte()
    const val STAR_TRAILS_LENGTH: Byte       = 0xB3.toByte()
    const val SYSTEM_VIDEO_MODE: Byte        = 0xB4.toByte()
    const val VIDEO_BIT_RATE: Byte           = 0xB6.toByte()
    const val BIT_DEPTH: Byte                = 0xB7.toByte()
    const val PROFILES: Byte                 = 0xB8.toByte()
    const val VIDEO_EASY_MODE: Byte          = 0xBA.toByte()
    const val LAPSE_MODE: Byte               = 0xBB.toByte()
    const val MAX_LENS_MOD: Byte             = 0xBD.toByte()
    const val MAX_LENS_MOD_ENABLE: Byte      = 0xBF.toByte()
    const val EASY_NIGHT_PHOTO: Byte         = 0xC0.toByte()
    const val MULTI_SHOT_ASPECT_RATIO: Byte  = 0xC1.toByte()
    const val FRAMING: Byte                  = 0xC3.toByte()
    const val CAMERA_VOLUME: Byte            = 0xD8.toByte()
    const val SETUP_SCREEN_SAVER: Byte       = 0xDB.toByte()
    const val SETUP_LANGUAGE: Byte           = 0xDF.toByte()
    const val PHOTO_MODE: Byte               = 0xE3.toByte()
    const val VIDEO_FRAMING: Byte            = 0xE8.toByte()
    const val MULTI_SHOT_FRAMING: Byte       = 0xE9.toByte()
    const val FRAME_RATE: Byte               = 0xEA.toByte()
}

object StatusId {
    const val BATTERY_PRESENT: Byte = 0x01
    const val BATTERY_LEVEL_BARS: Byte = 0x02
    const val IS_OVERHEATING: Byte = 0x06
    const val IS_BUSY: Byte = 0x08
    const val QUICK_CAPTURE_ENABLED: Byte = 0x09
    const val IS_ENCODING: Byte = 0x0A
    const val LCD_LOCK_ACTIVE: Byte = 0x0B
    const val ENCODING_DURATION: Byte = 0x0D
    const val WIRELESS_ENABLED: Byte = 0x11
    const val LAST_PAIRING_TYPE: Byte = 0x14
    const val LAST_PAIRING_TIME_MS: Byte = 0x15
    const val WIFI_SCAN_STATE: Byte = 0x16
    const val WIFI_SCAN_COMPLETED_MS: Byte = 0x17
    const val WIFI_PROVISIONING_STATE: Byte = 0x18
    const val WIRELESS_REMOTE_VERSION: Byte = 0x1A
    const val WIRELESS_REMOTE_CONNECTED: Byte = 0x1B
    const val WIRELESS_PAIRING_STATE: Byte = 0x1C
    const val CLIENT_WIFI_NAME: Byte = 0x1D
    const val AP_WIFI_NAME: Byte = 0x1E
    const val NUM_CONNECTED_DEVICES: Byte = 0x1F
    const val PREVIEW_STREAM_ENABLED: Byte = 0x20
    const val PHOTO_REMAINING: Byte = 0x22
    const val VIDEO_REMAINING: Byte = 0x23
    const val TOTAL_PHOTOS: Byte = 0x26
    const val TOTAL_VIDEOS: Byte = 0x27
    const val OTA_UPDATE_STATUS: Byte = 0x29
    const val OTA_CANCEL_PENDING: Byte = 0x2A
    const val LOCATE_CAMERA_ACTIVE: Byte = 0x2D
    const val TIMELAPSE_INTERVAL_COUNTDOWN: Byte = 0x31
    const val SDCARD_SPACE_KB: Byte = 0x36
    const val PREVIEW_STREAM_SUPPORTED: Byte = 0x37
    const val WIFI_SIGNAL_BARS: Byte = 0x38
    const val HILIGHT_COUNT: Byte = 0x3A
    const val LAST_HILIGHT_TIME_MS: Byte = 0x3B
    const val STATUS_POLL_INTERVAL_MS: Byte = 0x3C
    const val LIVEVIEW_EXPOSURE_Y1: Byte = 0x42
    const val LIVEVIEW_EXPOSURE_Y2: Byte = 0x43
    const val GPS_LOCKED: Byte = 0x44
    const val AP_MODE_ENABLED: Byte = 0x45
    const val BATTERY_LEVEL_PERCENT: Byte = 0x46
    const val DIGITAL_ZOOM_LEVEL: Byte = 0x4B
    const val DIGITAL_ZOOM_AVAILABLE: Byte = 0x4D
    const val IS_MOBILE_FRIENDLY: Byte = 0x4E
    const val IS_FIRST_TIME_USE: Byte = 0x4F
    const val IS_5GHZ_AVAILABLE: Byte = 0x51
    const val IS_SYSTEM_READY: Byte = 0x52
    const val OTA_BATTERY_OK: Byte = 0x53
    const val TOO_COLD_TO_RECORD: Byte = 0x55
    const val CAMERA_ORIENTATION: Byte = 0x56
    const val ZOOM_WHILE_ENCODING_SUPPORTED: Byte = 0x58
    const val FLATMODE_ID: Byte = 0x59
    const val VIDEO_PRESET_ID: Byte = 0x5D
    const val PHOTO_PRESET_ID: Byte = 0x5E
    const val TIMELAPSE_PRESET_ID: Byte = 0x5F
    const val PRESET_GROUP_ID: Byte = 0x60
    const val CURRENT_PRESET_ID: Byte = 0x61
    const val PRESET_STATUS_FLAG: Byte = 0x62
    const val LIVE_BURST_REMAINING: Byte = 0x63
    const val TOTAL_LIVE_BURSTS: Byte = 0x64
    const val CAPTURE_DELAY_ACTIVE: Byte = 0x65
    const val LINUX_CORE_ACTIVE: Byte = 0x68
    const val LENS_TYPE: Byte = 0x69
    const val VIDEO_HINDSIGHT_ACTIVE: Byte = 0x6A
    const val SCHEDULED_CAPTURE_SET: Byte = 0x6C
    const val BITMASKED_STATUS: Byte = 0x6E
    const val SDCARD_SPEED_ERROR: Byte = 0x6F
    const val SDCARD_SPEED_ERROR_COUNT: Byte = 0x70
    const val TURBO_TRANSFER_ACTIVE: Byte = 0x71
    const val CAMERA_CONTROL_STATUS: Byte = 0x72
    const val USB_CONNECTED: Byte = 0x73
    const val USB_CONTROL_STATE: Byte = 0x74
    const val SDCARD_TOTAL_CAPACITY_KB: Byte = 0x75
}
