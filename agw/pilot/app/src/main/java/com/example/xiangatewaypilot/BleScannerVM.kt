package com.example.xiangatewaypilot

import android.app.Application
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothGatt
import android.bluetooth.BluetoothGattCallback
import android.bluetooth.BluetoothGattCharacteristic
import android.bluetooth.BluetoothGattDescriptor
import android.bluetooth.BluetoothManager
import android.bluetooth.BluetoothProfile
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
import java.util.UUID

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

    //onScanResult() - ScanResult{
    // mDevice=E0:4B:85:02:4C:35, mScanRecord=ScanRecord [
    //  mAdvertiseFlags=2,
    //  mServiceUuids=[0000fea6-0000-1000-8000-00805f9b34fb],
    //  mManufacturerSpecificData={
    //      754=[2, 5, 65, 35, 0, 53, 76, 2, -123, 75, -32, 12]
    //  },
    //  mServiceData={
    //      0000fea6-0000-1000-8000-00805f9b34fb=[71, 95, 122, 122, 49, 56, 57, 53]
    //  },
    //  mTxPowerLevel=-2147483648,
    //  mDeviceName=GoPro 1895], mRssi=-56, mTimestampNanos=729496450490217}

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

    fun connectToDevice(context: Context, macAddress: String) {
        val device = bluetoothAdapter.getRemoteDevice(macAddress)
        device.connectGatt(context.applicationContext, false, gattCallback)
    }

    private val gattCallback = object : BluetoothGattCallback() {
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

                Log.i("BLE", "🔍 Discovered GATT Services:")
                gatt?.services?.let { services ->
                    for (service in services) {
                        val serviceName = GoProUuids.findByUuid(service.uuid.toString())?.name ?: "Unknown"
                        Log.i("BLE", "📦 Service UUID: ${service.uuid} [${serviceName}]")

                        for (characteristic in service.characteristics) {
                            val props = logCharacteristicProperties(characteristic)
                            val charName = GoProUuids.findByUuid(characteristic.uuid.toString())?.name ?: "Unknown"
                            Log.i("BLE", "  └─ 🧬 Characteristic UUID: ${characteristic.uuid} ${props} [${charName}]")
                            if (characteristic.properties and BluetoothGattCharacteristic.PROPERTY_NOTIFY != 0) {
                                subscribeToNotification(gatt, characteristic)
                            }
//                            if ((characteristic.properties and notifyFlag) != 0) {
//                                val descriptor = characteristic.getDescriptor(UUID.fromString(CLIENT_CHARACTERISTIC_CONFIG))
//                                descriptor?.value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
//                                gatt.writeDescriptor(descriptor)
//                            }
                        }
                    }
                }

                sendHard
            }
        }
    }

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
            Log.i("BLE", "✅ Subscribed to ${characteristic.uuid} ${charName}")
        } else {
            Log.w("BLE", "⚠️ CCCD not found for ${characteristic.uuid} ${charName}")
        }
    }

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