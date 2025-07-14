package com.example.xiangatewaypilot.constants

object ID2 {
    // Services

    const val GP_0001 = "0001" // GoPro Wifi Access Point
    const val GP_0090 = "0090" // GoPro Camera Management

    // Characteristics

    const val GP_0002 = "0002" // WiFi AP SSID
    const val GP_0003 = "0003" // WiFi AP Password
    const val GP_0004 = "0004" // WiFi AP Power
    const val GP_0005 = "0005" // WiFi AP State

    const val GP_0091 = "0091" // Network Management Command
    const val GP_0092 = "0092" // Network Management Response

    const val GP_0072 = "0072" // Command
    const val GP_0073 = "0073" // Command Response
    const val GP_0074 = "0074" // Settings
    const val GP_0075 = "0075" // Settings Response
    const val GP_0076 = "0076" // Query
    const val GP_0077 = "0077" // Query Response

    const val CHAR_WiFi_AP_SSID = GP_0002
    const val CHAR_WiFi_AP_Password = GP_0003
    const val CHAR_WiFi_AP_Power = GP_0004
    const val CHAR_WiFi_AP_State = GP_0005

    const val CHAR_Network_Management_Command = GP_0091
    const val CHAR_Network_Management_Response = GP_0092

    const val CHAR_Command = GP_0072
    const val CHAR_Command_Response = GP_0073
    const val CHAR_Settings = GP_0074
    const val CHAR_Settings_Response = GP_0075
    const val CHAR_Query = GP_0076
    const val CHAR_Query_Response = GP_0077

    const val SERVICE_WiFi_Access_Point = GP_0001
    const val SERVICE_Camera_Management = GP_0090

    val service = mapOf(
        GP_0002 to GP_0001,
        GP_0003 to GP_0001,
        GP_0004 to GP_0001,
        GP_0005 to GP_0001,

        GP_0091 to GP_0090,
        GP_0092 to GP_0090,
    )
}