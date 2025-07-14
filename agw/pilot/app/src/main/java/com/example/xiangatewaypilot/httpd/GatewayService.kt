package com.example.xiangatewaypilot.httpd

import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.util.Log
import java.io.IOException

class GatewayService : Service() {

    private val TAG = this::class.java.simpleName

    private lateinit var server: SimpleHttpServer

    override fun onCreate() {
        super.onCreate()
        val port = 6502
        server = SimpleHttpServer(port)
        try {
            server.start()
            Log.d(TAG, "NanoHTTPD started on port $port")
        } catch (e: IOException) {
            Log.e(TAG, "Failed to start NanoHTTPD", e)
        }
    }

    override fun onDestroy() {
        server.stop()
        Log.d("HttpServerService", "HTTP 서버 종료됨")
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    //override fun onBind(intent: Intent): IBinder {
    //    TODO("Return the communication channel to the service.")
    //}
}