package com.example.xiangatewaypilot.httpd

import android.content.Context
import android.content.Intent
import android.util.Log
import com.example.xiangatewaypilot.model.main.BleModel
import fi.iki.elonen.NanoHTTPD
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

class SimpleHttpServer(private val context: Context, port: Int, val vm: BleModel) : NanoHTTPD(port) {
    private val TAG = this::class.java.simpleName

    override fun serve(session: IHTTPSession): Response {
        val uri = session.uri
        val method = session.method

        Log.d("Nano", "Request: uri=$uri, method=$method")

        return when {
            uri == "/hello" && method == Method.GET -> {
                newFixedLengthResponse("Hello from NanoHTTPD!\n")
            }

            uri.startsWith("/app/connect") && method == Method.GET -> {
//                val intent = Intent("com.thinkware.xian.msg.web").apply {
//                    putExtra("path", uri.substring(5))
//                }
//                context.sendBroadcast(intent)
                Log.d(TAG, "Trying to connect")
                vm.connect()
                newFixedLengthResponse("Hello from NanoHTTPD!")
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
                val latch = CountDownLatch(1)
                var result = "timeout"
                val enables = uri.substring(17) == "true"
                vm.setApMode(enables) { enabled ->
                    result = if (enabled) "success" else "failure"
                    latch.countDown()
                }

                // 최대 2초 기다리기
                val completed = latch.await(2000, TimeUnit.MILLISECONDS)

                newFixedLengthResponse("result: $result")
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
