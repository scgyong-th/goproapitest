package com.example.xiangatewaypilot.model.scan

import android.Manifest
import android.Manifest.permission.BLUETOOTH_CONNECT
import android.app.Application
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothGattCharacteristic
import android.bluetooth.BluetoothManager
import android.bluetooth.le.BluetoothLeScanner
import android.bluetooth.le.ScanCallback
import android.bluetooth.le.ScanFilter
import android.bluetooth.le.ScanResult
import android.bluetooth.le.ScanSettings
import android.content.Context
import android.os.ParcelUuid
import androidx.annotation.RequiresPermission
import androidx.lifecycle.AndroidViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import androidx.lifecycle.viewModelScope
import com.example.xiangatewaypilot.constants.GOPRO_UUID
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class BleScannerVM(app: Application) : AndroidViewModel(app) {
    private val _devices = MutableStateFlow<List<ScannedDeviceEntry>>(emptyList())
    val devices: StateFlow<List<ScannedDeviceEntry>> = _devices.asStateFlow()
    private val _isScanning = MutableStateFlow(false)
    val isScanning: StateFlow<Boolean> = _isScanning

    private val bluetoothAdapter: BluetoothAdapter? by lazy {
        val manager = getApplication<Application>().getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager?
        manager?.adapter
    }

    private val scanner: BluetoothLeScanner? get() = bluetoothAdapter?.bluetoothLeScanner

    private val scanFilters = listOf<ScanFilter>(
        ScanFilter.Builder()
            .setServiceUuid(ParcelUuid.fromString(GOPRO_UUID))
            .build()
    )

    private val scanSettings = ScanSettings.Builder()
        .setScanMode(ScanSettings.SCAN_MODE_LOW_LATENCY)
        .build()

    private val scanCallback = object : ScanCallback() {
        @RequiresPermission(BLUETOOTH_CONNECT)
        override fun onScanResult(callbackType: Int, result: ScanResult?) {
            result?.let {
                val deviceName = it.device.name ?: "Unknown"
                val address = it.device.address

                // 제조사 데이터 추출
                val manuData = it.scanRecord?.manufacturerSpecificData
                val manuDataStr = buildString {
                    if (manuData != null) {
                        for (i in 0 until manuData.size()) {
                            val id = manuData.keyAt(i)
                            val data = manuData.valueAt(i)
                            append("ID=0x${id.toString(16).uppercase()} [${data.joinToString { b -> "%02X".format(b) }}]")
                            if (i != manuData.size() - 1) append("\n")
                        }
                    }
                }

                val device = ScannedDeviceEntry(deviceName, address, manuDataStr)

                _devices.update { list ->
                    if (list.any { it.address == device.address }) list else list + device
                }
            }
        }
    }

    @RequiresPermission(Manifest.permission.BLUETOOTH_SCAN)
    fun startScan() {
        _devices.value = emptyList()
        scanner?.startScan(scanFilters, scanSettings, scanCallback)
        _isScanning.value = true

        viewModelScope.launch {
            delay(5000)
            stopScan()
        }
    }

    @RequiresPermission(Manifest.permission.BLUETOOTH_SCAN)
    fun stopScan() {
        scanner?.stopScan(scanCallback)
        _isScanning.value = false
    }

    @RequiresPermission(Manifest.permission.BLUETOOTH_SCAN)
    override fun onCleared() {
        stopScan()
        super.onCleared()
    }

//    @OptIn(ExperimentalUnsignedTypes::class)
//    private fun sendGetHardwareInfo() {
//        val msg = BleMessage.getHardwareInfo()
//        val char = CharCache["0072"]
//        Log.v("BLE", "sendGetHardwareInfo() ${char?.uuid ?: ""}")
//        char?.let {
//            if (it.properties and BluetoothGattCharacteristic.PROPERTY_WRITE == 0) {
//                Log.e("BLE", "This characteristic is not writable")
//            }
//            it.value = msg.bytes!!
//            it.writeType = BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT
//            val success = gatt?.writeCharacteristic(it) == true
//            if (!success) {
//                Log.w("BLE", "Write (GetHardwareInfo) failed")
//            }
//        }
//    }
//
//    private fun sendGetWifiInfo() {
//        val char = CharCache.get("0001", "0002")
//        Log.v("BLE", "sendGetWifiInfo() $char")
//        char?.let {
//            val success = gatt?.readCharacteristic(it) == true
//            if (!success) {
//                Log.w("BLE", "Read (GetWifiInfo) failed")
//            }
//        }
//    }
//    private fun sendGetWifiPassword() {
//        val char = CharCache.get("0001", "0003")
//        Log.v("BLE", "sendGetWifiPassword() $char")
//        char?.let {
//            val success = gatt?.readCharacteristic(it) == true
//            if (!success) {
//                Log.w("BLE", "Read (GetWifiInfo) failed")
//            }
//        }
//    }

    fun logCharacteristicProperties(characteristic: BluetoothGattCharacteristic): String {
        val props = characteristic.properties
        val propList = mutableListOf<String>()

        if (props and BluetoothGattCharacteristic.PROPERTY_BROADCAST != 0)
            propList.add("BROADCAST")
        if (props and BluetoothGattCharacteristic.PROPERTY_READ != 0)
            propList.add("READ")
        if (props and BluetoothGattCharacteristic.PROPERTY_WRITE_NO_RESPONSE != 0)
            propList.add("WRITE_NO_RESPONSE")
        if (props and BluetoothGattCharacteristic.PROPERTY_WRITE != 0)
            propList.add("WRITE")
        if (props and BluetoothGattCharacteristic.PROPERTY_NOTIFY != 0)
            propList.add("NOTIFY")
        if (props and BluetoothGattCharacteristic.PROPERTY_INDICATE != 0)
            propList.add("INDICATE")
        if (props and BluetoothGattCharacteristic.PROPERTY_SIGNED_WRITE != 0)
            propList.add("SIGNED_WRITE")
        if (props and BluetoothGattCharacteristic.PROPERTY_EXTENDED_PROPS != 0)
            propList.add("EXTENDED_PROPS")

        return propList.joinToString(", ")
    }
}

