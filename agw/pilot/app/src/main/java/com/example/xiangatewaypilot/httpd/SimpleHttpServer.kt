package com.example.xiangatewaypilot.httpd

import android.content.Context
import android.content.Intent
import android.util.Log
import fi.iki.elonen.NanoHTTPD

class SimpleHttpServer(private val context: Context, port: Int) : NanoHTTPD(port) {

    override fun serve(session: IHTTPSession): Response {
        val uri = session.uri
        val method = session.method

        Log.d("Nano", "Request: uri=$uri, method=$method")

        return when {
            uri == "/hello" && method == Method.GET -> {
                newFixedLengthResponse("Hello from NanoHTTPD!\n")
            }

            uri.startsWith("/app/") && method == Method.GET -> {
                val intent = Intent("com.thinkware.xian.msg.web").apply {
                    putExtra("path", uri.substring(5))
                }
                context.sendBroadcast(intent)
                newFixedLengthResponse("Hello from NanoHTTPD!")
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
