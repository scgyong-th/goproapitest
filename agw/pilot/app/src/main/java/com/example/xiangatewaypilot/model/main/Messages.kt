package com.example.xiangatewaypilot.model.main

import com.example.xiangatewaypilot.constants.ID2
import com.example.xiangatewaypilot.data.responses.CommandResponse
import com.example.xiangatewaypilot.data.responses.GetHardwareInfoResponse

class GetHardwareInfo(onReturn: (GetHardwareInfoResponse)->Unit) : BleRequest.Write(
    characteristic = CharCache[ID2.CHAR_Command]!!,
    value = byteArrayOf(0x01, 0x3C),
    onReturn = { it -> onReturn(it as GetHardwareInfoResponse) }
) {
    init {
        tryCount = 10
    }
}


class GetWifiApSsid(onReturn: (String)->Unit) : BleRequest.Read(
    characteristic = CharCache[ID2.CHAR_WiFi_AP_SSID]!!,
    onReturn = { it -> onReturn(String(it ?: ByteArray(0), Charsets.UTF_8)) }
)

class GetWifiApPassword(onReturn: (String)->Unit) : BleRequest.Read(
    characteristic = CharCache[ID2.CHAR_WiFi_AP_Password]!!,
    onReturn = { it -> onReturn(String(it ?: ByteArray(0), Charsets.UTF_8)) }
)

class SetApControl(enables: Boolean, onReturn: (CommandResponse)->Unit) : BleRequest.Write(
    characteristic = CharCache[ID2.CHAR_Command]!!,
    value = byteArrayOf(0x03, 0x17, 0x01, if (enables) 0x01 else 0x00),
    onReturn = onReturn
)