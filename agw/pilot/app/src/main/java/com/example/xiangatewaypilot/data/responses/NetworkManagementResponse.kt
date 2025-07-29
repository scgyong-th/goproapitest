package com.example.xiangatewaypilot.data.responses

import open_gopro.ResponseGenericOuterClass
import open_gopro.ResponseGenericOuterClass.ResponseGeneric

class NetworkManagementResponse(bytes: ByteArray): NotifiedResponse(bytes) {
    val featureId: Int get() = bytes.getOrNull(0)?.toInt() ?: -1
    val actionId: Int get() = bytes.getOrNull(1)?.toInt() ?: -1
    lateinit var responseGeneric: ResponseGeneric
    val isSuccessful: Boolean get() = responseGeneric.result == ResponseGenericOuterClass.EnumResultGeneric.RESULT_SUCCESS
    val responseGenericResult: Int get() = responseGeneric.result.ordinal
    init {
        offset = 2
        responseGeneric = ResponseGeneric.parser().parseFrom(bytes.copyOfRange(2, bytes.size))
        responseGeneric.result
    }
}