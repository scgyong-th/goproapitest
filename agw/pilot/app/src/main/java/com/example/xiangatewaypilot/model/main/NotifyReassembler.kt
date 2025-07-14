package com.example.xiangatewaypilot.model.main

import android.util.Log

class NotifyReassembler(private val timeoutMillis: Long = 2000) {
    private val fragments = mutableMapOf<Int, ByteArray>()
    private var expectedPacketCount: Int? = null
    private var totalPayloadLength: Int? = null
    private var lastReceivedTime: Long = 0

    fun append(fragment: ByteArray): ByteArray? {
        if (fragment.isEmpty()) return null
        val seq = fragment[0].toInt() and 0xFF
        if (seq < 0x20) {
            return fragment
        }

        val now = System.currentTimeMillis()

        // 타임아웃 초과되었으면 초기화
        if (lastReceivedTime > 0 && now - lastReceivedTime > timeoutMillis) {
            fragments.clear()
            expectedPacketCount = null
            totalPayloadLength = null
        }

        lastReceivedTime = now

        val body = fragment.copyOfRange(1, fragment.size)

        fragments[seq] = body

        if (seq == 0x20 && body.size > 0) {
            // 메시지 총 길이 추출 (두 번째 바이트가 전체 길이)
            val totalLen = body[0].toInt() and 0xFF
            totalPayloadLength = totalLen + 1

            // BLE 패킷은 최대 20바이트 → 1바이트는 seq, 19바이트 payload
            val firstBodyPayloadSize = body.size
            val remainingPayload = totalLen - firstBodyPayloadSize
            val packetsNeeded = kotlin.math.ceil(remainingPayload / 19.0).toInt()

            expectedPacketCount = 1 + packetsNeeded

            Log.v("BLE", "$totalLen, $firstBodyPayloadSize, $remainingPayload, $packetsNeeded, $expectedPacketCount")
        }

        if (expectedPacketCount != null && fragments.size >= expectedPacketCount!!) {
            val fullPayload = fragments.toSortedMap().values.flattenBytes()

            // 일부 BLE 기기는 1~2 byte 더 보낼 수도 있어서 길이 기준으로 잘라줌
            val actualLength = totalPayloadLength ?: fullPayload.size
            val result = fullPayload.take(actualLength).toByteArray()

            // 초기화
            fragments.clear()
            expectedPacketCount = null
            totalPayloadLength = null

            return result
        }

        return null
    }

    private fun Collection<ByteArray>.flattenBytes(): ByteArray {
        val totalLength = sumOf { it.size }
        val result = ByteArray(totalLength)
        var offset = 0
        for (array in this) {
            array.copyInto(result, offset)
            offset += array.size
        }
        return result
    }
}