package com.example.xiangatewaypilot

import android.app.Application
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothManager
import android.bluetooth.le.BluetoothLeScanner
import android.bluetooth.le.ScanCallback
import android.bluetooth.le.ScanResult
import android.content.Context
import androidx.lifecycle.AndroidViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

data class BleDevice(val name: String?, val address: String)

class BleScannerVM(app: Application) : AndroidViewModel(app) {
    private val _devices = MutableStateFlow<List<BleDevice>>(emptyList())
    val devices: StateFlow<List<BleDevice>> = _devices.asStateFlow()

    private val bluetoothAdapter: BluetoothAdapter by lazy {
        val manager = getApplication<Application>().getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
        manager.adapter
    }

    private val scanner: BluetoothLeScanner? get() = bluetoothAdapter.bluetoothLeScanner

    private val scanCallback = object : ScanCallback() {
        override fun onScanResult(callbackType: Int, result: ScanResult?) {
            result?.let {
                val device = BleDevice(it.device.name, it.device.address)
                val address = it.device.address
                _devices.update { list ->
                    if (list.any { address == device.address}) list else list + device
                }
            }
        }
    }

    fun startScan() {
        _devices.value = emptyList()
        scanner?.startScan(scanCallback)
    }

    fun stopScan() {
        scanner?.stopScan(scanCallback)
    }

    override fun onCleared() {
        stopScan()
        super.onCleared()
    }
}