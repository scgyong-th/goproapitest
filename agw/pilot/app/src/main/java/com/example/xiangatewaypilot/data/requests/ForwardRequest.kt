package com.example.xiangatewaypilot.data.requests

import android.bluetooth.BluetoothGattCharacteristic
import android.util.Log
import com.example.xiangatewaypilot.constants.ID2
import com.example.xiangatewaypilot.model.main.CharCache
import com.example.xiangatewaypilot.util.toHexString

class ForwardRequest(private val path: String, val onResult: (req: ForwardRequest, resp: Response?)->Unit): BleRequest.Write(
    characteristic = CharCache[Regex("""/fw/(\d{4})(?:/|$)""").find(path)?.groupValues?.get(1)!!]!!,
    value = ByteArray(0)
) {
    private lateinit var charId2: String
    private var forwardResponse: Response? = null

    val byteArrayMap = mutableMapOf<Int, ByteArray>()
    init {
        Regex("""/fw/(\d{4})(?:/([^/]+))?$""").find(path)?.groupValues?.let { values ->
            val char = if (values.size >= 2) values[1] else ""
            reads = char !in setOf(ID2.CHAR_Command, ID2.CHAR_Query, ID2.CHAR_Settings)
            if (values.size >= 3) {
                value = values[2].toHexBytes()
                Log.v("ForwardRequest", "char=$char msg=$values[2], values=$values size=${values.size}")
            } else {
                Log.w("ForwardRequest", "No data. changing to read Characteristic")
                reads = true
            }
        }
    }

    override fun handleResponse(
        bytes: ByteArray,
        characteristic: BluetoothGattCharacteristic
    ): Boolean {
        val charUuid = characteristic.uuid.toString()
        charId2 = charUuid.substring(4, 8)

        if (reads) {
            forwardResponse = Response(charId2, listOf(bytes))
            return true
        }
        val assembled = reassembler.append(bytes)
        byteArrayMap[reassembler.lastIndex] = bytes
        if (assembled == null) return false
        this.resultBytes = assembled
        Log.d("ForwardRequest", "Assembled: ${assembled.size} bytes, ${byteArrayMap.size} packets")
        forwardResponse = Response(charId2, byteArrayMap.toSortedMap().values)
        return true
    }

    override fun invokeCallback() {
        onResult.invoke(this, forwardResponse)
    }
    class Response(val charId2: String, val bytesCollection: Collection<ByteArray>) {
        fun toJson(): String {
            val strings = bytesCollection.map { it.toHexString().replace(" ", "") }
            val packets = "[" + strings.joinToString(",") { "\"$it\"" } + "]"

            return """{"id2":"$charId2","packets":$packets,"error":""}"""
        }
    }
}

fun String.toHexBytes(): ByteArray {
    val str = if (length % 2 == 0) this else this + "0"
    return str.chunked(2)
        .map { it.toInt(16).toByte() }
        .toByteArray()
}