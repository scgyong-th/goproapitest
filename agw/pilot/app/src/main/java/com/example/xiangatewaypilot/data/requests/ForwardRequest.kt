package com.example.xiangatewaypilot.data.requests

import com.example.xiangatewaypilot.model.main.CharCache

class ForwardRequest(path: String): BleRequest(
    characteristic = CharCache[Regex("""/fw/(\d{4})(?:/|$)""").find(path)?.groupValues?.get(1)!!]!!
) {
}