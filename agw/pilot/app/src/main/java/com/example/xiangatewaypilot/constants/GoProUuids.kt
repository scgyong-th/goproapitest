package com.example.xiangatewaypilot.constants

import android.content.Context
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import org.json.JSONObject
import java.util.UUID

@Serializable
data class UuidEntry(
    val uuid: String,
    val name: String
)

object GoProUuids {
    lateinit var service: List<UuidEntry>
    lateinit var characteristic: List<UuidEntry>
    lateinit var descriptor: List<UuidEntry>

    private var isInitialized = false

    fun init(context: Context) {
        if (isInitialized) return

        val jsonStr = context.assets.open("uuids.json").bufferedReader().use { it.readText() }
        val json = Json { ignoreUnknownKeys = true }

        // 전체 객체 파싱 (JSONObject → Kotlin Map 처리)
        val root = JSONObject(jsonStr)

        service = json.decodeFromString(root.getJSONArray("service").toString())
        characteristic = json.decodeFromString(root.getJSONArray("characteristic").toString())
        descriptor = json.decodeFromString(root.getJSONArray("descriptor").toString())

        isInitialized = true
    }

    fun findByUuid(uuid: String): UuidEntry? {
        return service.find { it.uuid.equals(uuid, ignoreCase = true) }
            ?: characteristic.find { it.uuid.equals(uuid, ignoreCase = true) }
            ?: descriptor.find { it.uuid.equals(uuid, ignoreCase = true) }
    }

    fun goproUuid(twoBytes: String): String {
        return "b5f9${twoBytes}-aa8d-11e3-9046-0002a5d5c51b"
    }
}


const val GOPRO_UUID = "0000FEA6-0000-1000-8000-00805f9b34fb"
const val GOPRO_BASE_UUID = "b5f9%s-aa8d-11e3-9046-0002a5d5c51b"

enum class GoProUUID(val uuid: UUID) {
    WIFI_AP_PASSWORD(UUID.fromString(GOPRO_BASE_UUID.format("0003"))),
    WIFI_AP_SSID(UUID.fromString(GOPRO_BASE_UUID.format("0002"))),
    CQ_COMMAND(UUID.fromString(GOPRO_BASE_UUID.format("0072"))),
    CQ_COMMAND_RSP(UUID.fromString(GOPRO_BASE_UUID.format("0073"))),
    CQ_SETTING(UUID.fromString(GOPRO_BASE_UUID.format("0074"))),
    CQ_SETTING_RSP(UUID.fromString(GOPRO_BASE_UUID.format("0075"))),
    CQ_QUERY(UUID.fromString(GOPRO_BASE_UUID.format("0076"))),
    CQ_QUERY_RSP(UUID.fromString(GOPRO_BASE_UUID.format("0077")));
}

