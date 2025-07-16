package com.example.xiangatewaypilot.data.responses

import android.util.Log
import com.example.xiangatewaypilot.util.toHexString
import org.json.JSONObject

class QueryRequestResult(bytes: ByteArray) : NotifiedResponse(bytes) {
    private val map = mutableMapOf<Byte, ByteArray>();
    init {
        Log.v("QueryRequestResult", "Offset=$offset")
        while (offset + 1 < bytes.size) {
            val key = bytes[offset++]
            val len = bytes[offset++].toInt() and 0xFF
            if (offset + len <= bytes.size) {
                val arr = bytes.copyOfRange(offset, offset + len)
                map[key] = arr
                offset += len
            } else {
                Log.w("QueryRequestResult", "Invalid len=$len at offset=$offset")
                break
            }
        }
    }
    val byteValue: Int get() = map.entries.firstOrNull()?.value?.firstOrNull()?.toInt() ?: -1
    val bytesValue: ByteArray get() = map.entries.firstOrNull()?.value ?: ByteArray(0)
    operator fun get(key: Byte): Int { return map[key]?.firstOrNull()?.toInt() ?: -1 }
    fun bytes(key: Byte): ByteArray? { return map[key] }

    override fun toJson(): String {
        val json = JSONObject()
        for ((key, value) in map) {
            json.put("0x${"%02X".format(key)}($key)}", value.toHexString())
        }
        return json.toString(2)
    }
}
