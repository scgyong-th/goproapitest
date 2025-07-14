package com.example.xiangatewaypilot.data.responses

import android.util.Log
import com.example.xiangatewaypilot.util.toHexString

open class CommandResponse(protected val bytes: ByteArray) {
    val commandId: Int get() = bytes.getOrNull(1)?.toInt() ?: -1
    val status: Int get() = bytes.getOrNull(2)?.toInt() ?: -1

    protected var offset = 3  // 기본적으로 [0]=len, [1]=commandId, [2]=status
    protected var optionalResponse: ByteArray? = null

    init {
        offset = 3
        if (offset < bytes.size) {
            optionalResponse = nextBytes()
            if (optionalResponse?.isEmpty() == true) {
                optionalResponse = null
            }
        }
    }
    fun nextString(): String {
        val len = bytes[offset++].toInt() and 0xFF
        val str = bytes.copyOfRange(offset, offset + len).toString(Charsets.UTF_8)
        offset += len

        Log.v("CmdResp", "String: $str")
        return str
    }

    fun nextBytes(): ByteArray {
        val len = bytes[offset++].toInt() and 0xFF
        val data = bytes.copyOfRange(offset, offset + len)
        offset += len

        Log.v("CmdResp", "Bytes:<$len> ${data.joinToString(" ") { "%02X".format(it) }}")

        return data
    }

    open fun toJson(): String {
        return """{"command":${commandId},"status":${status},"value":"${bytes.toHexString()}"}"""
    }
}
