package com.example.xiangatewaypilot.model.main

import android.content.Context
import android.net.ConnectivityManager
import android.net.Network
import android.net.NetworkCapabilities
import android.net.NetworkRequest
import android.net.wifi.WifiConfiguration
import android.net.wifi.WifiManager
import android.net.wifi.WifiNetworkSpecifier
import android.os.Build
import android.util.Log
import androidx.annotation.RequiresApi
import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.engine.cio.CIO
import io.ktor.client.engine.okhttp.OkHttp
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.request.get
import io.ktor.client.request.post
import io.ktor.client.request.setBody
import io.ktor.http.ContentType
import io.ktor.http.contentType
import io.ktor.serialization.kotlinx.json.json
import kotlinx.serialization.json.Json

class WifiHttpClient(val context: Context) {

    companion object {
        const val BASE_URL = "http://10.5.5.9:8080"
    }
    private val client = HttpClient(OkHttp) {
        install(ContentNegotiation) {
            json(Json { ignoreUnknownKeys = true })
        }
    }
    suspend fun sendKeepAlive(): String {
        try {
            val response = client.get("$BASE_URL/gopro/camera/keep_alive")
            val body = response.body<String>()
            Log.d("GoProHTTP", "✅ KeepAlive response: $body")
            return body
        } catch (e: Exception) {
            Log.e("GoProHTTP", "❌ Failed to send KeepAlive: ${e.message}", e)
            return "error: ${e.message}"
        }
    }

    suspend fun sendAPIMessage(url: String): String {
        try {
            val response = client.get("$BASE_URL/$url")
            val body = response.body<String>()
            Log.d("GoProHTTP", "✅ KeepAlive response: $body")
            return body
        } catch (e: Exception) {
            Log.e("GoProHTTP", "❌ Failed to send $url: ${e.message}", e)
            return "error: ${e.message}"
        }
    }

    fun connect(ssid: String, password: String) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            connectUsingNetworkSpecifier(ssid, password)
        } else {
            connectUsingWifiManagerLegacy(ssid, password)
        }
    }
    @RequiresApi(Build.VERSION_CODES.Q)
    fun connectUsingNetworkSpecifier(ssid: String, password: String) {
        val specifier = WifiNetworkSpecifier.Builder()
            .setSsid(ssid)
            .setWpa2Passphrase(password)
            .build()

        val request = NetworkRequest.Builder()
            .addTransportType(NetworkCapabilities.TRANSPORT_WIFI)
            .setNetworkSpecifier(specifier)
            .build()

        val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager

        connectivityManager.requestNetwork(request, object : ConnectivityManager.NetworkCallback() {
            override fun onAvailable(network: Network) {
                connectivityManager.bindProcessToNetwork(network)
                Log.d("WIFI", "Connected to $ssid")
            }

            override fun onUnavailable() {
                Log.e("WIFI", "Failed to connect to $ssid")
            }
        })
    }
    @Suppress("DEPRECATION")
    private fun connectUsingWifiManagerLegacy(ssid: String, password: String) {
        val wifiConfig = WifiConfiguration().apply {
            SSID = "\"$ssid\""
            preSharedKey = "\"$password\""
        }

        Log.v("WifiHttpClient", "connecting $ssid/$password $wifiConfig")
        val wifiManager = context.applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
        val netId = wifiManager.addNetwork(wifiConfig)
        Log.v("WifiHttpClient", "netId:$netId")
        if (netId != -1) {
            wifiManager.disconnect()
            wifiManager.enableNetwork(netId, true)
            wifiManager.reconnect()
        }
    }
}