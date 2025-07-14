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
import androidx.lifecycle.AndroidViewModel
import com.example.xiangatewaypilot.constants.GoProUuids
import com.example.xiangatewaypilot.data.responses.ResponseFactory
import com.example.xiangatewaypilot.model.scan.ScannedDeviceEntry
import com.example.xiangatewaypilot.util.toHexString
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import java.util.UUID

class BleModel(app: Application): AndroidViewModel(app) {
    //var device = BleDevice("", "", "xxx")
    private val _selectedDevice = MutableStateFlow<ScannedDeviceEntry?>(null)
    val selectedDevice: StateFlow<ScannedDeviceEntry?> = _selectedDevice
    var gatt: BluetoothGatt? = null

    val notifyReassembler: NotifyReassembler = NotifyReassembler()

    private val bluetoothAdapter: BluetoothAdapter? by lazy {
        val manager = app.getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager?
        manager?.adapter
    }

    init {
        _selectedDevice.value = ScannedDeviceEntry.load(app)
    }
    fun selectDevice(device: ScannedDeviceEntry) {
        _selectedDevice.value = device
    }
    @SuppressLint("MissingPermission")
    fun connect() {
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
                    gatt?.discoverServices()
                }
                BluetoothProfile.STATE_DISCONNECTED -> {
                    Log.w("BLE", "Disconnected from ${gatt?.device?.address}")
                }
            }
        }

        override fun onServicesDiscovered(gatt: BluetoothGatt?, status: Int) {
            if (status == BluetoothGatt.GATT_SUCCESS) {
                //Log.i("BLE", "Services: ${gatt?.services}")
                val notifyFlag = BluetoothGattCharacteristic.PROPERTY_NOTIFY

                this@BleModel.gatt = gatt
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
                                subscribeToNotification(gatt, characteristic)
                            }
                        }
                    }
                }


                Handler(Looper.getMainLooper()).postDelayed({
                    startHandshake()
                }, 500)
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
            val assembled = notifyReassembler.append(data)
            if (assembled == null) {
                Log.i("BLE", "🔔 Notify from ${characteristic.uuid}: ${data.toHexString()}")
                return
            }

            Log.d("BLE", "Assembled: ${assembled.toHexString()}")
            val resp = ResponseFactory.parse(assembled)
            resp?.let {
                Log.d("BLE", "JSON: ${it.toJson()}")
                Handler(Looper.getMainLooper()).post {
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

            Handler(Looper.getMainLooper()).post {
                val request = requestForRead
                if (requestForRead != null) {
                    requestForRead = null
                    finishRequest()
                }
                request?.setResponse(value)
            }
        }
    }

    private fun startHandshake() {
        Log.d("BLE", "startHandshake()")
        enqueueRequest(GetHardwareInfo() { resp ->
            Log.d("BLE", "resp: ${resp.toJson()}")
        })
        enqueueRequest(GetWifiApSsid() { ssid ->
            Log.d("BLE", "SSID: $ssid")
        })
        enqueueRequest(GetWifiApPassword() { password ->
            Log.d("BLE", "Password: $password")
        })
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

    private val requestQueue: ArrayDeque<BleRequest> = ArrayDeque()
    private var isProcessing = false
    private var requestForNotify: BleRequest.Write? = null
    private var requestForRead: BleRequest.Read? = null

    fun enqueueRequest(request: BleRequest) {
        Log.d("BLE", "enqueue")
        requestQueue.addLast(request)
        processNext()
    }

    @SuppressLint("MissingPermission")
    private fun processNext() {
        Log.v("BLE", "In processNext(): $isProcessing or $requestForNotify")
        if (isProcessing || requestForNotify != null) return

        val request = requestQueue.removeFirstOrNull() ?: return
        Log.v("BLE", "popped: $request")
        isProcessing = true

        when (request) {
            is BleRequest.Read -> {
                requestForRead = request
                Log.v("BLE", "before read")
                val success = gatt?.readCharacteristic(request.characteristic) == true
                Log.v("BLE", "after  read: $success")
                if (!success) finishRequest()
            }

            is BleRequest.Write -> {
                request.characteristic.value = request.value
                val success = gatt?.writeCharacteristic(request.characteristic) == true

                Log.d("BLE", "Write: ${request.value.toHexString()} ${success}")

                // 👇 write 후 response가 없는 명령이면 바로 다음 처리
                if (!success || !request.waitForResponse) {
                    finishRequest()
                } else {
                    // 👇 response notify가 올 때까지 block
                    requestForNotify = request
                }
            }
        }
    }
    private fun finishRequest() {
        Log.d("BLE", "finishing Request")
        // delayed processNext()
        Handler(Looper.getMainLooper()).postDelayed({
            isProcessing = false
            Log.d("BLE", "After Delay?")
            processNext()
        }, 100)
    }
}