package com.example.xiangatewaypilot.model.scan

import android.content.Context
import android.util.Log
import androidx.core.content.edit

data class ScannedDeviceEntry(
    val name: String,
    val address: String,
    val manufacturerData: String
) {
    override fun toString(): String {
        return "$name ($address)\n$manufacturerData"
    }

    fun save(context: Context) {
        Log.v("BleDevice", "Saving: $this")
        val prefs = context.getSharedPreferences("ble_prefs", Context.MODE_PRIVATE)
        prefs.edit() {
            putString("ble_device", this@ScannedDeviceEntry.toString())
            Log.v("BleDevice", this@ScannedDeviceEntry.toString())
        }
    }

    companion object {
        fun fromString(str: String): ScannedDeviceEntry? {
            val lines = str.lines()
            if (lines.size < 2) return null

            val firstLine = lines[0]
            val manufacturerData = lines.drop(1).joinToString("\n") // 여러 줄일 수도 있음

            val nameAddressRegex = Regex("""^(.*)\s+\(([^)]+)\)$""")
            val match = nameAddressRegex.matchEntire(firstLine) ?: return null

            val name = match.groupValues[1].trim()
            val address = match.groupValues[2].trim()

            return ScannedDeviceEntry(name, address, manufacturerData.trim())
        }
        fun load(context: Context): ScannedDeviceEntry? {
            val prefs = context.getSharedPreferences("ble_prefs", Context.MODE_PRIVATE)
            val saved = prefs.getString("ble_device", null) ?: return null
            return fromString(saved)
        }
    }
}