package com.example.xiangatewaypilot.data.responses

import android.util.Log
import org.json.JSONObject

class GetHardwareInfoResponse(bytes: ByteArray) : CommandResponse(bytes) {
    val modelNumber: String
    val modelName: String
    //val deprecated: ByteArray
    val firmwareVersion: String
    val serialNumber: String
    val apSsid: String
    val apMacAddress: String
    val reserved: ByteArray

    init {
        Log.v("GetHardwareResponse", "Offset=$offset")

        modelNumber = nextString()
        modelName = nextString()
        //deprecated = nextBytes()
        firmwareVersion = nextString()
        serialNumber = nextString()
        apSsid = nextString()
        apMacAddress = nextString()
        reserved = bytes.copyOfRange(offset, bytes.size)
    }
    override fun toJson(): String {
        val json = JSONObject()
        json.put("modelNumber", modelNumber)
        json.put("modelName", modelName)
        //json.put("deprecated", deprecated.joinToString(" ") { "%02X".format(it) })
        json.put("firmwareVersion", firmwareVersion)
        json.put("serialNumber", serialNumber)
        json.put("apSsid", apSsid)
        json.put("apMacAddress", apMacAddress)
        json.put("reserved", reserved.joinToString(" ") { "%02X".format(it) })
        return json.toString(2)
    }
}
