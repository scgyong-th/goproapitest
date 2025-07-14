package com.example.xiangatewaypilot.util

fun ByteArray.toHexString(): String =
    joinToString(" ") { "%02X".format(it) }

