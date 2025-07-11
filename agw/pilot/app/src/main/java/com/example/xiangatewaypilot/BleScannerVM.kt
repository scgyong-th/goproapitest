package com.example.xiangatewaypilot

import android.app.Application
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothManager
import android.bluetooth.le.BluetoothLeScanner
import android.bluetooth.le.ScanCallback
import android.bluetooth.le.ScanFilter
import android.bluetooth.le.ScanResult
import android.bluetooth.le.ScanSettings
import android.content.Context
import android.os.ParcelUuid
import android.util.Log
import androidx.lifecycle.AndroidViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

data class BleDevice(
    val name: String,
    val address: String,
    val manufacturerData: String
) {
    override fun toString(): String {
        return "$name ($address)\n$manufacturerData"
    }
}

const val GOPRO_UUID = "0000FEA6-0000-1000-8000-00805f9b34fb"

class BleScannerVM(app: Application) : AndroidViewModel(app) {
    private val _devices = MutableStateFlow<List<BleDevice>>(emptyList())
    val devices: StateFlow<List<BleDevice>> = _devices.asStateFlow()

    private val bluetoothAdapter: BluetoothAdapter by lazy {
        val manager = getApplication<Application>().getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
        manager.adapter
    }

    private val scanner: BluetoothLeScanner? get() = bluetoothAdapter.bluetoothLeScanner

    private val scanFilters = listOf<ScanFilter>(
        ScanFilter.Builder()
            .setServiceUuid(ParcelUuid.fromString(GOPRO_UUID))
            .build()
    )

    private val scanSettings = ScanSettings.Builder()
        .setScanMode(ScanSettings.SCAN_MODE_LOW_LATENCY)
        .build()

    private val scanCallback = object : ScanCallback() {
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

                val device = BleDevice(deviceName, address, manuDataStr)

                _devices.update { list ->
                    if (list.any { it.address == device.address }) list else list + device
                }
            }
        }
    }

    fun startScan() {
        _devices.value = emptyList()
        scanner?.startScan(scanFilters, scanSettings, scanCallback)
    }

    fun stopScan() {
        scanner?.stopScan(scanCallback)
    }

    override fun onCleared() {
        stopScan()
        super.onCleared()
    }
}