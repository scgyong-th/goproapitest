package com.example.xiangatewaypilot.data.responses

import android.util.Log
import com.example.xiangatewaypilot.util.toHexString

open class NotifiedResponse(protected val bytes: ByteArray) {
    val responseId: Int get() = bytes.getOrNull(0)?.toInt() ?: -1
    val status: Int get() = bytes.getOrNull(1)?.toInt() ?: -1

    protected var offset = 2  // 기본적으로 [0]=commandId, [1]=status
    protected var optionalResponse: ByteArray? = null

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
        return """{"response":${responseId},"status":${status},"value":"${bytes.toHexString()}"}"""
    }
}