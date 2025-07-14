package com.example.xiangatewaypilot.model.main

import android.bluetooth.BluetoothGatt
import android.bluetooth.BluetoothGattCharacteristic
import com.example.xiangatewaypilot.constants.GOPRO_UUID
import com.example.xiangatewaypilot.constants.ID2
import java.util.UUID

object CharCache {
    private val map = mutableMapOf<String, BluetoothGattCharacteristic>()

    lateinit var gatt: BluetoothGatt  // 외부에서 초기화 필요
    private var serviceUuid: UUID = UUID.fromString(GOPRO_UUID)

    /**
     * [key]는 4글자 short code ("0072") 형태
     */
    operator fun get(key: String): BluetoothGattCharacteristic? {
        return map[key] ?: run {
            val serviceUuidPart = ID2.service[key]
            val uuid: UUID
            if (serviceUuidPart != null) {
                uuid = goproUuid(serviceUuidPart)
            } else {
                uuid = serviceUuid
            }
            val fullCharUuid = goproUuid(key)
            val char = gatt.getService(uuid)?.getCharacteristic(fullCharUuid)
            if (char != null) {
                map[key] = char
            }
            char
        }
    }

    fun get(service: String, char: String): BluetoothGattCharacteristic? {
        val charUuid = goproUuid(char)
        var characteristic = this[char]
        characteristic?.let {
            return it
        }
        characteristic = gatt.getService(goproUuid(service)).getCharacteristic(charUuid)
        characteristic?.let {
            map[char] = it
            return it
        }
        return null
    }

    fun clear() {
        map.clear()
    }

    private fun goproUuid(shortCode: String): UUID {
        return UUID.fromString("b5f9${shortCode}-aa8d-11e3-9046-0002a5d5c51b")
    }
}