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
import android.os.Handler
import android.os.Looper
import android.os.ParcelUuid
import android.util.Log
import androidx.lifecycle.AndroidViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import java.util.UUID
import androidx.core.content.edit
import com.example.xiangatewaypilot.data.responses.ResponseFactory
import java.lang.Math.ceil

data class BleDevice(
    val name: String,
    val address: String,
    val manufacturerData: String
) {
    override fun toString(): String {
        return "$name ($address)\n$manufacturerData"
    }

    fun save(context: Context) {
        Log.v("BleDevice", "Saving: $this")
        val prefs = context.getSharedPreferences("ble_prefs", Context.MODE_PRIVATE)
        prefs.edit() {
            putString("ble_device", this@BleDevice.toString())
            Log.v("BleDevice", this@BleDevice.toString())
        }
    }

    companion object {
        fun fromString(str: String): BleDevice? {
            val lines = str.lines()
            if (lines.size < 2) return null

            val firstLine = lines[0]
            val manufacturerData = lines.drop(1).joinToString("\n") // 여러 줄일 수도 있음

            val nameAddressRegex = Regex("""^(.*)\s+\(([^)]+)\)$""")
            val match = nameAddressRegex.matchEntire(firstLine) ?: return null

            val name = match.groupValues[1].trim()
            val address = match.groupValues[2].trim()

            return BleDevice(name, address, manufacturerData.trim())
        }
        fun load(context: Context): BleDevice? {
            val prefs = context.getSharedPreferences("ble_prefs", Context.MODE_PRIVATE)
            val saved = prefs.getString("ble_device", null) ?: return null
            return fromString(saved)
        }
    }
}

class BleScannerVM(app: Application) : AndroidViewModel(app) {
    private val _devices = MutableStateFlow<List<BleDevice>>(emptyList())
    val devices: StateFlow<List<BleDevice>> = _devices.asStateFlow()
    var gatt: BluetoothGatt? = null
    var device: BleDevice? = null
    val notifyReassembler: NotifyReassembler = NotifyReassembler()

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

    fun connectToDevice(context: Context, device: BleDevice) {
        this.device = device
        val macAddress = device.address
        val dev = bluetoothAdapter.getRemoteDevice(macAddress)
        dev.connectGatt(context.applicationContext, false, gattCallback)
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

                this@BleScannerVM.gatt = gatt
                CharCache.gatt = gatt!!
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

                Handler(Looper.getMainLooper()).postDelayed({
                    sendGetHardwareInfo()
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
            }
        }

    }

    @OptIn(ExperimentalUnsignedTypes::class)
    private fun sendGetHardwareInfo() {
        val msg = BleMessage.getHardwareInfo()
        val char = CharCache["0072"]
        Log.v("BLE", "sendGetHardwareInfo() $char")
        char?.let {
            if (it.properties and BluetoothGattCharacteristic.PROPERTY_WRITE == 0) {
                Log.e("BLE", "This characteristic is not writable")
            }
            it.value = msg.bytes!!
            it.writeType = BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT
            val success = gatt?.writeCharacteristic(it) == true
            if (!success) {
                Log.w("BLE", "Write failed")
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

object CharCache {
    private val map = mutableMapOf<String, BluetoothGattCharacteristic>()

    lateinit var gatt: BluetoothGatt  // 외부에서 초기화 필요
    private var serviceUuid: UUID = UUID.fromString(GOPRO_UUID)

    /**
     * [key]는 4글자 short code ("0072") 형태
     */
    operator fun get(key: String): BluetoothGattCharacteristic? {
        return map[key] ?: run {
            val fullUuid = goproUuid(key)
            val char = gatt.getService(serviceUuid)?.getCharacteristic(fullUuid)
            if (char != null) {
                map[key] = char
            }
            char
        }
    }

    fun clear() {
        map.clear()
    }

    private fun goproUuid(shortCode: String): UUID {
        return UUID.fromString("b5f9${shortCode}-aa8d-11e3-9046-0002a5d5c51b")
    }
}

fun ByteArray.toHexString(): String =
    joinToString(" ") { "%02X".format(it) }

class NotifyReassembler(private val timeoutMillis: Long = 2000) {
    private val fragments = mutableMapOf<Int, ByteArray>()
    private var expectedPacketCount: Int? = null
    private var totalPayloadLength: Int? = null
    private var lastReceivedTime: Long = 0

    fun append(fragment: ByteArray): ByteArray? {
        if (fragment.isEmpty()) return null

        val now = System.currentTimeMillis()

        // 타임아웃 초과되었으면 초기화
        if (lastReceivedTime > 0 && now - lastReceivedTime > timeoutMillis) {
            fragments.clear()
            expectedPacketCount = null
            totalPayloadLength = null
        }

        lastReceivedTime = now

        val seq = fragment[0].toInt() and 0xFF
        val body = fragment.copyOfRange(1, fragment.size)

        fragments[seq] = body

        if (seq == 0x20 && body.size > 0) {
            // 메시지 총 길이 추출 (두 번째 바이트가 전체 길이)
            val totalLen = body[0].toInt() and 0xFF
            totalPayloadLength = totalLen + 1

            // BLE 패킷은 최대 20바이트 → 1바이트는 seq, 19바이트 payload
            val firstBodyPayloadSize = body.size
            val remainingPayload = totalLen - firstBodyPayloadSize
            val packetsNeeded = kotlin.math.ceil(remainingPayload / 19.0).toInt()

            expectedPacketCount = 1 + packetsNeeded
        }

        if (expectedPacketCount != null && fragments.size >= expectedPacketCount!!) {
            val fullPayload = fragments.toSortedMap().values.flattenBytes()

            // 일부 BLE 기기는 1~2 byte 더 보낼 수도 있어서 길이 기준으로 잘라줌
            val actualLength = totalPayloadLength ?: fullPayload.size
            val result = fullPayload.take(actualLength).toByteArray()

            // 초기화
            fragments.clear()
            expectedPacketCount = null
            totalPayloadLength = null

            return result
        }

        return null
    }

    private fun Collection<ByteArray>.flattenBytes(): ByteArray {
        val totalLength = sumOf { it.size }
        val result = ByteArray(totalLength)
        var offset = 0
        for (array in this) {
            array.copyInto(result, offset)
            offset += array.size
        }
        return result
    }
}