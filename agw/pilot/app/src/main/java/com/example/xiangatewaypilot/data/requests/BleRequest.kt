package com.example.xiangatewaypilot.data.requests

import android.bluetooth.BluetoothGattCharacteristic
import android.util.Log
import com.example.xiangatewaypilot.data.responses.NotifiedResponse
import com.example.xiangatewaypilot.data.NotifyReassembler
import com.example.xiangatewaypilot.data.ResponseFactory
import com.example.xiangatewaypilot.util.toHexString

sealed class BleRequest(val characteristic: BluetoothGattCharacteristic,
                        var tryCount: Int = 3,
                        var reads: Boolean = true,
                        val onResponse: ((BleRequest, ByteArray)->Unit)? = null) {
    var resultBytes: ByteArray? = null
    val valueString: String get() = String(resultBytes ?: ByteArray(0), Charsets.UTF_8)
    open fun handleResponse(bytes: ByteArray, characteristic: BluetoothGattCharacteristic): Boolean {
        this.resultBytes = bytes
        return true
    }

    open fun invokeCallback() {
        resultBytes?.let {
            onResponse?.invoke(this, it)
        }
    }

    open class Read(
        characteristic: BluetoothGattCharacteristic,
        onResponse: ((BleRequest, ByteArray)->Unit)? = null
    ) : BleRequest(characteristic, onResponse = onResponse)

    open class Write(
        characteristic: BluetoothGattCharacteristic,
        var value: ByteArray,
        val waitForResponse: Boolean = true, // 👈 response 여부 제어
        private val onNotifiedResponse: ((BleRequest, NotifiedResponse)->Unit)? = null
    ) : BleRequest(characteristic, reads = false) {
        private var response: NotifiedResponse? = null
        private val reassembler = NotifyReassembler()

        // called in BLE callback thread
        override fun handleResponse(
            bytes: ByteArray,
            characteristic: BluetoothGattCharacteristic
        ): Boolean {
            val assembled = reassembler.append(bytes) ?: return false
            this.resultBytes = assembled
            Log.d("BleRequest.Write", "Assembled: ${assembled.size} bytes")
            response = ResponseFactory.parse(characteristic.uuid.toString(), assembled)
            if (response == null) {
                Log.w("BleRequest.Write", "parse failed: ${assembled.toHexString()}")
                return false
            }
            return true
        }

        // called in main thread
        override fun invokeCallback() {
            val response = response ?: return
            Log.d("BleRequest.Write", "JSON: ${response.toJson()}")
            onNotifiedResponse?.invoke(this, response)
        }
    }
}
