package com.example.xiangatewaypilot.data.responses

import android.util.Log
import com.example.xiangatewaypilot.constants.ID2
import com.example.xiangatewaypilot.model.main.CommandId
import com.example.xiangatewaypilot.model.main.QueryId

object ResponseFactory {
    private val parserMap: Map<String, Map<Byte, (ByteArray) -> NotifiedResponse>> = mapOf(
        ID2.CHAR_Command_Response to mapOf(
            CommandId.GET_HARDWARE_INFO to ::GetHardwareInfoResponse,
            CommandId.SET_AP_CONTROL to ::QueryRequestResult,
            // 0x3D to ::OtherResponse,
            // ...
        ),
        ID2.CHAR_Query_Response to mapOf(
            QueryId.GET_STATUS_VALUES to ::QueryRequestResult
        )
    )

    fun parse(charUuid: String, assembled: ByteArray): NotifiedResponse? {
        val cmdId = assembled.getOrNull(0) ?: return null
        val id2 = charUuid.substring(4, 8)
        parserMap[id2]?.let { map ->
            map[cmdId]?.let { parser ->
                Log.d("ResponseFactory", "Invoking $parser for <$id2/$cmdId>")
                return parser.invoke(assembled)
            }
        }
        Log.v("ResponseFactory", "Parser not found. Just creating NotifiedResponse for <$id2/$cmdId>")
        return NotifiedResponse(assembled)
    }
}
