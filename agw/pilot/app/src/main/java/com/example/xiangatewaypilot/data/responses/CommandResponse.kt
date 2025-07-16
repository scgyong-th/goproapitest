package com.example.xiangatewaypilot.data.responses

import com.example.xiangatewaypilot.util.toHexString

open class CommandResponse(bytes: ByteArray) : NotifiedResponse(bytes) {
    init {
        if (offset < bytes.size) {
            optionalResponse = nextBytes()
            if (optionalResponse?.isEmpty() == true) {
                optionalResponse = null
            }
        }
    }
    override fun toJson(): String {
        return """{"command":${responseId},"status":${status},"value":"${bytes.toHexString()}"}"""
    }
}
