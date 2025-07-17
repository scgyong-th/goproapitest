package com.example.xiangatewaypilot.model.main

import android.Manifest
import android.annotation.SuppressLint
import android.app.Application
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothGatt
import android.bluetooth.BluetoothGattCallback
import android.bluetooth.BluetoothGattCharacteristic
import android.bluetooth.BluetoothGattDescriptor
import android.bluetooth.BluetoothManager
import android.bluetooth.BluetoothProfile
import android.content.Context
import android.os.Handler
import android.os.Looper
import android.util.Log
import androidx.annotation.RequiresPermission
import androidx.compose.runtime.mutableStateMapOf
import androidx.lifecycle.AndroidViewModel
import com.example.xiangatewaypilot.constants.GoProUuids
import com.example.xiangatewaypilot.data.ResponseFactory
import com.example.xiangatewaypilot.data.requests.BleRequest
import com.example.xiangatewaypilot.data.requests.CommandId
import com.example.xiangatewaypilot.data.requests.CommandRequest
import com.example.xiangatewaypilot.data.requests.GetHardwareInfo
import com.example.xiangatewaypilot.data.requests.GetWifiApPassword
import com.example.xiangatewaypilot.data.requests.GetWifiApSsid
import com.example.xiangatewaypilot.data.requests.QueryId
import com.example.xiangatewaypilot.data.requests.QueryRequest
import com.example.xiangatewaypilot.data.requests.SetApControl
import com.example.xiangatewaypilot.data.requests.StatusId
import com.example.xiangatewaypilot.model.scan.ScannedDeviceEntry
import com.example.xiangatewaypilot.util.toHexString
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.UUID

class MainModel(app: Application): AndroidViewModel(app) {
    //var device = BleDevice("", "", "xxx")
    private val _selectedDevice = MutableStateFlow<ScannedDeviceEntry?>(null)
    val selectedDevice: StateFlow<ScannedDeviceEntry?> = _selectedDevice
    var gatt: BluetoothGatt? = null

    val properties = mutableStateMapOf<String, String>()

    val notifyReassembler: NotifyReassembler = NotifyReassembler()

    private val handler: Handler by lazy { Handler(Looper.getMainLooper()) }
    val notifyCharacteristics = mutableListOf<BluetoothGattCharacteristic>()

    private val httpClient: WifiHttpClient by lazy { WifiHttpClient(app) }

    private val bluetoothAdapter: BluetoothAdapter? by lazy {
        val manager = app.getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager?
        manager?.adapter
    }

    init {
        _selectedDevice.value = ScannedDeviceEntry.load(app)
        properties.clear()
    }
    fun selectDevice(device: ScannedDeviceEntry) {
        _selectedDevice.value = device
    }
    @SuppressLint("MissingPermission")
    fun connect() {
        //Log.v("BleModel", "connect() is called")
        if (_selectedDevice.value == null) {
            Log.w("BleModel", "No selected device")
            return
        }
        val macAddress = _selectedDevice.value?.address ?: ""
        val dev = bluetoothAdapter!!.getRemoteDevice(macAddress)
        val app = getApplication<Application>()
        dev.connectGatt(app.applicationContext, false, gattCallback)
    }

    private val gattCallback = object : BluetoothGattCallback() {
        @RequiresPermission(Manifest.permission.BLUETOOTH_CONNECT)
        override fun onConnectionStateChange(gatt: BluetoothGatt?, status: Int, newState: Int) {
            Log.i("BLE", "onConnectionStateChange: status=$status, newState=$newState")

            when (newState) {
                BluetoothProfile.STATE_CONNECTED -> {
                    Log.i("BLE", "Connected to ${gatt?.device?.address}")
                    handler.post {
                        Log.d("BLE", """Setting "connected" to true""")
                        properties["connected"] = "true"
                    }
                    gatt?.discoverServices()
                }
                BluetoothProfile.STATE_DISCONNECTED -> {
                    Log.d("BLE", """Setting "connected" to false""")
                    properties["connected"] = "false"
                    Log.w("BLE", "Disconnected from ${gatt?.device?.address}")
                }
            }
        }

        override fun onServicesDiscovered(gatt: BluetoothGatt?, status: Int) {
            if (status == BluetoothGatt.GATT_SUCCESS) {
                //Log.i("BLE", "Services: ${gatt?.services}")
                val notifyFlag = BluetoothGattCharacteristic.PROPERTY_NOTIFY

                this@MainModel.gatt = gatt
                CharCache.gatt = gatt!!
                Log.i("BLE", "🔍 Discovered GATT Services:")
                gatt.services?.let { services ->
                    for (service in services) {
                        val serviceName = GoProUuids.findByUuid(service.uuid.toString())?.name ?: "Unknown"
                        //Log.i("BLE", "📦 Service UUID: ${service.uuid} [${serviceName}]")

                        for (characteristic in service.characteristics) {
                            //val props = logCharacteristicProperties(characteristic)
                            val charName = GoProUuids.findByUuid(characteristic.uuid.toString())?.name ?: "Unknown"
                            //Log.i("BLE", "  └─ 🧬 Characteristic UUID: ${characteristic.uuid} ${props} [${charName}]")
                            if (characteristic.properties and BluetoothGattCharacteristic.PROPERTY_NOTIFY != 0) {
                                notifyCharacteristics.add(characteristic)
                            }
                        }
                    }
                }


                handler.postDelayed({
                    subscribeNextNotification()
                }, 100)
            }
        }

        override fun onCharacteristicWrite(
            gatt: BluetoothGatt,
            characteristic: BluetoothGattCharacteristic,
            status: Int
        ) {
            if (status == BluetoothGatt.GATT_SUCCESS) {
                Log.i("BLE", "Write succeeded to ${characteristic.uuid}")
            } else {
                Log.e("BLE", "Write failed to ${characteristic.uuid}, status=$status")
            }
        }

        @Deprecated("Deprecated by Android API", ReplaceWith("newer callback if exists"))
        override fun onCharacteristicChanged(gatt: BluetoothGatt, characteristic: BluetoothGattCharacteristic) {
            val data = characteristic.value
            Log.v("BLE", "CharChange: (${data.size}) ${data.toHexString()} on char=${characteristic.uuid}")
            val assembled = notifyReassembler.append(data)
            if (assembled == null) {
                //Log.i("BLE", "🔔 Notify from ${characteristic.uuid}: ${data.toHexString()}")
                return
            }

            Log.d("BLE", "Assembled: ${assembled.toHexString()}")
            val resp = ResponseFactory.parse(characteristic.uuid.toString(), assembled)
            resp?.let {
                Log.d("BLE", "JSON: ${it.toJson()}")
                handler.post {
                    val request = requestForNotify
                    if (requestForNotify != null) {
                        requestForNotify = null
                        finishRequest()
                    }

                    request?.setResponse(resp)
                }
            }
        }

        @Deprecated("Deprecated in Java")
        override fun onCharacteristicRead(
            gatt: BluetoothGatt,
            characteristic: BluetoothGattCharacteristic,
            status: Int
        ) {
            val value = characteristic.value
            Log.d("BLE", "onCharRead: char=${characteristic.uuid}, value=${value.toHexString()}, status=${status}")

            handler.post {
                val request = requestForRead
                if (requestForRead != null) {
                    requestForRead = null
                    finishRequest()
                }
                request?.setResponse(value)
            }
        }

        override fun onDescriptorWrite(
            gatt: BluetoothGatt?,
            descriptor: BluetoothGattDescriptor?,
            status: Int
        ) {
            Log.v("BLE", "onDescriptorWrite status=$status uuid=${descriptor?.uuid}")
            handler.post {
                subscribeNextNotification()
            }
        }
    }

    private fun startHandshake() {
        Log.d("BLE", "startHandshake()")
        enqueueRequest(GetHardwareInfo() { resp ->
            Log.d("BLE", "resp: ${resp.toJson()}")
            properties["deviceJson"] = resp.toJson()
        })
        enqueueRequest(GetWifiApSsid() { ssid ->
            Log.d("BLE", "SSID: $ssid")
            properties["wifi_ssid"] = ssid
        })
        enqueueRequest(GetWifiApPassword() { password ->
            Log.d("BLE", "Password: $password")
            properties["wifi_password"] = password
        })
        queryApMode { enabled ->
            Log.d("BLE", "AP_MODE_ENABLED (before enabling) resp: $enabled")
        }
        enqueueRequest(SetApControl(true) { resp ->
            Log.d("BLE", "resp: ${resp.toJson()}")
        })
        queryApMode { enabled ->
            Log.d("BLE", "AP_MODE_ENABLED (after enabling) resp: $enabled")
            connectToWifi()
        }
    }

    fun queryApMode(onResult: ((Boolean)->Unit)?) {
        enqueueRequest(QueryRequest(QueryId.GET_STATUS_VALUES, StatusId.AP_MODE_ENABLED) { resp->
            Log.d("BLE", "AP_MODE_ENABLED resp: ${resp.byteValue}")
            properties["ap_mode"] = if (resp.byteValue == 1) "enabled" else "disabled"
            onResult?.invoke(resp.byteValue == 1)
        })
    }

    fun setApMode(enables: Boolean, onResult: ((Boolean)->Unit)?) {
        enqueueRequest(SetApControl(enables) { resp ->
            onResult?.invoke((resp.status == 0))
        })
    }

    fun connectToWifi() {
        val ssid = properties["wifi_ssid"] ?: ""
        val password = properties["wifi_password"] ?: ""
        httpClient.connect(ssid, password)

        //sendKeepAlive()
    }

    private fun sendKeepAlive() {
        handler.postDelayed({
            CoroutineScope(Dispatchers.IO).launch {
                val result = httpClient.sendKeepAlive()
                Log.v("BLE", "KeepAlive returned $result")
                if (result.startsWith("error:")) {
                    properties["keep_alive"] = "Error"
                } else {
                    val now = SimpleDateFormat("HH:mm:ss", Locale.getDefault()).format(Date())
                    properties["keep_alive"] = "Wifi $now"
                }
            }
            sendKeepAlive()
        }, 5000)
    }

    @SuppressLint("MissingPermission")
    private fun subscribeNextNotification() {
        if (notifyCharacteristics.isEmpty()) {
            Log.i("BLE", "Subscribed all chars. Starting Handshake.")
            startHandshake()
            return
        }
        val char = notifyCharacteristics[0]
        notifyCharacteristics.removeAt(0)
        subscribeToNotification(gatt!!, char)
    }
    @RequiresPermission(Manifest.permission.BLUETOOTH_CONNECT)
    private fun subscribeToNotification(
        gatt: BluetoothGatt,
        characteristic: BluetoothGattCharacteristic
    ) {
        gatt.setCharacteristicNotification(characteristic, true)

        val charName = GoProUuids.findByUuid(characteristic.uuid.toString())?.name ?: "Unknown"

        // CCCD 디스크립터를 찾아 설정
        val cccdUuid = UUID.fromString("00002902-0000-1000-8000-00805f9b34fb")
        val descriptor = characteristic.getDescriptor(cccdUuid)
        if (descriptor != null) {
            descriptor.value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
            gatt.writeDescriptor(descriptor)
            Log.i("BLE", "✅ Subscribed to ${characteristic.uuid} $charName")
        } else {
            Log.w("BLE", "⚠️ CCCD not found for ${characteristic.uuid} $charName")
        }
    }

    private var keepAliveReservedOn: Long = 0
    private fun reserveKeepAlive() {
        keepAliveReservedOn = System.currentTimeMillis()
        Log.v("BLE", "keepAliveReserved on $keepAliveReservedOn")
        val reservedOn = keepAliveReservedOn
        handler.postDelayed({
            if (reservedOn == keepAliveReservedOn) {
                enqueueRequest(CommandRequest(CommandId.KEEP_ALIVE) {
                    val now = SimpleDateFormat("HH:mm:ss", Locale.getDefault()).format(Date())
                    properties["keep_alive"] = "BLE $now"
                })
            } else {
                Log.v("BLE", "reservedOn=$reservedOn now reserved=$keepAliveReservedOn")
            }
        }, 3000)
    }
    private val requestQueue: ArrayDeque<BleRequest> = ArrayDeque()
    private var isProcessing = false
    private var requestForNotify: BleRequest.Write? = null
    private var requestForRead: BleRequest.Read? = null
    private var requestedOn: Long = 0

    fun enqueueRequest(request: BleRequest) {
        Log.d("BLE", "enqueue")
        requestQueue.addLast(request)
        processNext()
    }

    private fun handleRequestFailure(request: BleRequest) {
        request.tryCount -= 1
        Log.d("BLE", "tryCount={request.tryCount}")
        if (request.tryCount > 0) {
            requestQueue.addFirst(request)
        }
        finishRequest()
    }
    @SuppressLint("MissingPermission")
    private fun processNext() {
        Log.v("BLE", "In processNext(): $isProcessing or $requestForNotify")
        if (isProcessing || requestForNotify != null) return

        val request = requestQueue.removeFirstOrNull()
        if (request == null) {
            reserveKeepAlive()
            return
        }
        Log.v("BLE", "popped: $request")
        isProcessing = true

        when (request) {
            is BleRequest.Read -> {
                requestForRead = request
                Log.v("BLE", "before read")
                val success = gatt?.readCharacteristic(request.characteristic) == true
                Log.v("BLE", "after  read: $success")
                if (!success) {
                    handleRequestFailure(request)
                } else {
                    waitForResponse()
                }
            }

            is BleRequest.Write -> {
                request.characteristic.value = request.value
                val success = gatt?.writeCharacteristic(request.characteristic) == true

                Log.d("BLE", "Write: ${request.value.toHexString()} ${success} $gatt")

                if (!success) {
                    handleRequestFailure(request)
                    return
                }
                // 👇 write 후 response가 없는 명령이면 바로 다음 처리
                if (!request.waitForResponse) {
                    finishRequest()
                } else {
                    // 👇 response notify가 올 때까지 block
                    requestForNotify = request
                    waitForResponse()
                }
            }
        }
    }
    private fun waitForResponse() {
        requestedOn = System.currentTimeMillis()
        val reqOn = requestedOn
        handler.postDelayed({
            if (reqOn == requestedOn) {
                Log.w("BLE", "Timeout: $requestForNotify read=$requestForRead")
                finishRequest()
            } else {
                Log.v("BLE", "ignoring timeout because $reqOn != $requestedOn")
            }
        }, 1000)
    }
    private fun finishRequest() {
        Log.d("BLE", "finishing Request: notify=$requestForNotify read=$requestForRead")
        requestedOn = 0
        requestForRead = null
        requestForNotify = null
        // delayed processNext()
        handler.postDelayed({
            isProcessing = false
            Log.d("BLE", "After Delay?")
            processNext()
        }, 100)
    }
}