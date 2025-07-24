package com.example.xiangatewaypilot.httpd

import android.content.Context
import android.os.Build
import android.util.Log
import com.example.xiangatewaypilot.data.requests.ForwardRequest
import com.example.xiangatewaypilot.model.main.MainModel
import fi.iki.elonen.NanoHTTPD
import kotlinx.serialization.json.Json
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

class SimpleHttpServer(private val context: Context, port: Int, val vm: MainModel) : NanoHTTPD(port) {
    private val TAG = this::class.java.simpleName

    private val infoJson: String get(){
        val pkgInfo = context.packageManager.getPackageInfo(context.packageName, 0)
        val versionCode = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P)
            pkgInfo.longVersionCode
        else
            @Suppress("DEPRECATION") pkgInfo.versionCode.toLong()

        val appName = context.applicationInfo.loadLabel(context.packageManager).toString()
        return Json.encodeToString(
            mapOf(
                "appName" to appName,
                "appVersionName" to pkgInfo.versionName,
                "appVersionCode" to versionCode.toString(),
                "osVersion" to Build.VERSION.RELEASE,
                "osSdkInt" to Build.VERSION.SDK_INT.toString(),
                "osCodename" to Build.VERSION.CODENAME,
                "deviceName" to Build.MODEL,
            )
        )
    }

    override fun serve(session: IHTTPSession): Response {
        val uri = session.uri
        val method = session.method

        Log.d("Nano", "Request: uri=$uri, method=$method")

        return when {
            uri == "/app/info" && method == Method.GET -> {
                newFixedLengthResponse(infoJson)
            }
            uri == "/app/connect" && method == Method.GET -> {
                if (vm.isConnected) {
                    return newFixedLengthResponse("""{"connected":true}""")
                }
                vm.connect()
                newFixedLengthResponse("""
                    {
                        "connected": false,
                        "trying": true
                    }
                """.trimIndent())
            }
            uri == "/app/get_hardware_info" && method == Method.GET -> {
                newFixedLengthResponse(vm.deviceJson)
            }
            uri == "/app/wifi/connect" && method == Method.GET -> {
                vm.connectToWifi()
                newFixedLengthResponse("Trying to connect to Wifi...")
            }
            uri.startsWith("/app/status/ap_mode") && method == Method.GET -> {
                val latch = CountDownLatch(1)
                var enabled = "timeout"
                vm.queryApMode { apEnabled ->
                    enabled = if (apEnabled) "true" else "false"
                    latch.countDown()
                }

                // 최대 2초 기다리기
                val completed = latch.await(2000, TimeUnit.MILLISECONDS)

                newFixedLengthResponse("Enabled: $enabled")
            }
            uri.startsWith("/app/set/ap_mode/") && method == Method.GET -> {
                val latch = CountDownLatch(2)
                var result = "timeout"
                var enabled = "timeout"
                val enables = uri.substring(17) == "true"
                vm.setApMode(enables) { success ->
                    result = if (success) "success" else "failure"
                    latch.countDown()
                }

                vm.queryApMode { apEnabled ->
                    enabled = if (apEnabled) "true" else "false"
                    latch.countDown()
                }

                // 최대 2초 기다리기
                val completed = latch.await(2000, TimeUnit.MILLISECONDS)

                newFixedLengthResponse("result: $result, enabled: $enabled")
            }
            uri.startsWith("/fw/") -> {
                val latch = CountDownLatch(1)
                var json = """{"error":"timeout"}"""

                vm.enqueueRequest(ForwardRequest(uri) { req, resp ->
                    resp?.let { json = it.toJson() }
                    Log.d("httpd", "$uri -> $json")
                    latch.countDown()
                })

                // 최대 2초 기다리기
                val completed = latch.await(2000, TimeUnit.MILLISECONDS)
                Log.d("httpd", "$uri -> $json")

                newFixedLengthResponse(json)
            }
            uri == "/test" && method == Method.POST -> {
                val body = session.inputStream.bufferedReader().readText()
                println("Received POST body: $body")
                newFixedLengthResponse("OK: $body")
            }

            else -> {
                newFixedLengthResponse(Response.Status.NOT_FOUND, MIME_PLAINTEXT, "404 Not Found")
            }
        }
    }
}
