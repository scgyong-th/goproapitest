package com.example.xiangatewaypilot.httpd

import android.util.Log
import fi.iki.elonen.NanoHTTPD

class SimpleHttpServer(port: Int) : NanoHTTPD(port) {

    override fun serve(session: IHTTPSession): Response {
        val uri = session.uri
        val method = session.method

        Log.d("Nano", "Request: uri=$uri, method=$method")

        return when {
            uri == "/hello" && method == Method.GET -> {
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
