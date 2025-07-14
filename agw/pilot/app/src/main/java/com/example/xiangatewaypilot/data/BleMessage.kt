package com.example.xiangatewaypilot.data

import com.example.xiangatewaypilot.constants.GoProUUID
import java.util.UUID

//@OptIn(ExperimentalUnsignedTypes::class)
class BleMessage {
    lateinit var uuid: UUID
    var bytes: ByteArray? = null
    companion object {
        fun getHardwareInfo(): BleMessage {
            val m = BleMessage()
            m.uuid = GoProUUID.CQ_COMMAND.uuid
            m.bytes = byteArrayOf(0x01, 0x3C)
            return m
        }
    }
}


