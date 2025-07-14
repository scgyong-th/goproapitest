package com.example.xiangatewaypilot.data.responses

object ResponseFactory {
    private val parserMap: Map<Int, (ByteArray) -> CommandResponse> = mapOf(
        0x3C to ::GetHardwareInfoResponse
        // 0x3D to ::OtherResponse,
        // ...
    )

    fun parse(bytes: ByteArray): CommandResponse? {
        val cmdId = bytes.getOrNull(1)?.toInt() ?: return null
        val parser = parserMap[cmdId]
        return parser?.invoke(bytes) ?: CommandResponse(bytes)
    }
}
