package com.example.xiangatewaypilot.model.main

import android.bluetooth.BluetoothGattCharacteristic
import com.example.xiangatewaypilot.data.responses.CommandResponse
import com.example.xiangatewaypilot.data.responses.NotifiedResponse

sealed class BleRequest(var tryCount: Int = 3) {
    open class Read(
        val characteristic: BluetoothGattCharacteristic,
        val onReturn: ((ByteArray)->Unit)? = null
    ) : BleRequest() {
        private var value: ByteArray? = null
        val valueString: String get() = String(value ?: ByteArray(0), Charsets.UTF_8)
        fun setResponse(resp: ByteArray) {
            value = resp
            onReturn?.invoke(resp)
        }
    }
    open class Write(
        val characteristic: BluetoothGattCharacteristic,
        val value: ByteArray,
        val waitForResponse: Boolean = true, // 👈 response 여부 제어
        val onReturn: ((NotifiedResponse)->Unit)? = null
    ) : BleRequest() {
        private var response: NotifiedResponse? = null

        fun setResponse(resp: NotifiedResponse) {
            response = resp;
            onReturn?.invoke(resp)
        }
    }
}
