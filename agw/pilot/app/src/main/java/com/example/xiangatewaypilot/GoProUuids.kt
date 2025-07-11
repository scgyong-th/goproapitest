package com.example.xiangatewaypilot

import android.content.Context
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import org.json.JSONObject

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
}