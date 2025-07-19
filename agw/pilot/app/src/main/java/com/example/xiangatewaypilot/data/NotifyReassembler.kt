package com.example.xiangatewaypilot.data

import android.util.Log
import com.example.xiangatewaypilot.util.toHexString
import kotlin.math.ceil


class NotifyReassembler(private val timeoutMillis: Long = 2000) {
    companion object {
        const val PAYLOAD_MASK = 0xE0
        const val PAYLOAD_GENERAL = 0x00
        const val PAYLOAD_EXT_13BIT = 0x20
        const val PAYLOAD_EXT_16BIT = 0x40
        const val PAYLOAD_CONTINUATION = 0x80
        const val EXT_13BIT_LENGTH_MASK = 0x1F
        const val SEQ_CONTINUATION_MASK = 0x0F
    }


    //private val fragments = mutableMapOf<Int, ByteArray>()
    private val indexSet = mutableSetOf<Int>()
    private var fullMessage = ByteArray(0)
    private var remainingPacketCount: Int = 0
    private var totalPayloadLength: Int = 0
    private var firstBodyPayloadSize: Int = 0
    private var downloadedBytes: Int = 0
    private var lastReceivedTime: Long = 0
    var lastIndex: Int = 0

    fun append(fragment: ByteArray): ByteArray? {
        if (fragment.size < 3) {
            Log.w("NotifyReassembler", "Notify Message is too short: (${fragment.toHexString()})")
            return null
        }
        val seq = fragment[0].toInt() and 0xFF
        val payloadType = seq and PAYLOAD_MASK
        if (payloadType == PAYLOAD_GENERAL) {
            return fragment.copyOfRange(1, fragment.size)
        }

        val now = System.currentTimeMillis()
        // 타임아웃 초과되었으면 초기화
        if (lastReceivedTime > 0 && now - lastReceivedTime > timeoutMillis) {
            reset()
        }

        lastReceivedTime = now

        when (payloadType) {
            PAYLOAD_EXT_13BIT -> {
                val msb = fragment[0].toInt() and EXT_13BIT_LENGTH_MASK
                val lsb = fragment[1].toInt() and 0xFF
                val len = (msb shl 8) or lsb
                setFirstPacket(len, fragment, 2)
            }

            PAYLOAD_EXT_16BIT -> {
                val msb = fragment[1].toInt() and 0xFF
                val lsb = fragment[2].toInt() and 0xFF
                val len = (msb shl 8) or lsb
                setFirstPacket(len, fragment, 3)
            }

            PAYLOAD_CONTINUATION -> {
                return appendContinuationPacket(fragment)
            }
        }

        return null
    }

    private fun setFirstPacket(messageLength: Int, fragment: ByteArray, offset: Int) {
        indexSet.clear()
        indexSet.add(0)

        fullMessage = ByteArray(messageLength)

        firstBodyPayloadSize = fragment.size - offset
        System.arraycopy(fragment, offset, fullMessage, 0, firstBodyPayloadSize)
        totalPayloadLength = messageLength
        downloadedBytes = firstBodyPayloadSize
        remainingPacketCount = ceil((messageLength - firstBodyPayloadSize) / 19.0).toInt()

        lastIndex = 0
    }

    private fun reset() {
        indexSet.clear()
        fullMessage = ByteArray(0)
        remainingPacketCount = 0
        totalPayloadLength = 0
        firstBodyPayloadSize = 0
        downloadedBytes = 0
    }

    private fun appendContinuationPacket(fragment: ByteArray) : ByteArray? {
        val seq = fragment[0].toInt() and SEQ_CONTINUATION_MASK
        val index = getIndexFor(seq)
        lastIndex = index
        indexSet.add(index)
        val offset = firstBodyPayloadSize + (index - 1) * 19
        if (offset > fullMessage.size) {
            Log.e("NotifyReassembler", "more packets than expected")
            return null
        }
        var len = fragment.size - 1
        if (offset + len > fullMessage.size) {
            len = fullMessage.size - offset
        }
        //Log.v("NotifyReassembler", "seq=$seq, index=$index, offset=$offset, len=$len, frag.size=${fragment.size}")
        System.arraycopy(fragment, 1, fullMessage, offset, len)

        remainingPacketCount -= 1
        downloadedBytes += len
        //Log.v("NotifyReassembler", "remainingPacketCount=$remainingPacketCount, downloadedBytes=$downloadedBytes")

        if (remainingPacketCount > 0) return null

        val bytes = fullMessage
        reset()
        return bytes
    }

    private fun getIndexFor(seq: Int): Int {
        var index = seq + 1
        while (indexSet.contains(index)) {
            index += 16
        }
        return index
    }
}