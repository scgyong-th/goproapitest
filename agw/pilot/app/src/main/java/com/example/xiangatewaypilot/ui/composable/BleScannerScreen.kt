package com.example.xiangatewaypilot.ui.composable

import android.content.pm.PackageManager
import android.os.Build
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.example.xiangatewaypilot.model.scan.ScannedDeviceEntry
import com.example.xiangatewaypilot.model.scan.BleScannerVM

@Composable
fun BleScannerScreen(viewModel: BleScannerVM, onResult: (ScannedDeviceEntry?)->Unit) {
    val devices by viewModel.devices.collectAsState()
    //var isScanning by remember { mutableStateOf(false) }
    val isScanning by viewModel.isScanning.collectAsState()
    val context = LocalContext.current

    LaunchedEffect(Unit) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            val permissions = arrayOf(
                android.Manifest.permission.BLUETOOTH_SCAN,
                android.Manifest.permission.BLUETOOTH_CONNECT
            )

            if (!permissions.all {
                    ContextCompat.checkSelfPermission(
                        context,
                        it
                    ) == PackageManager.PERMISSION_GRANTED
                }) {
                return@LaunchedEffect
            }
        }

        viewModel.startScan()
        //isScanning = true
    }
    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Text(
            text = "Scan GoPro Devices",
            fontSize = 24.sp,
            modifier = Modifier.padding(16.dp)
        )
        Text("🔍 검색된 BLE 장치 목록:")
        Button(
            onClick = {
                if (isScanning) {
                    viewModel.stopScan()
                } else {
                    viewModel.startScan()
                }
                //isScanning = !isScanning
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(if (isScanning) "Stop Scan" else "Start Scan")
        }

        Spacer(modifier = Modifier.height(16.dp))

        LazyColumn {
            items(devices) { device ->
                Column(
                    Modifier
                        .fillMaxWidth()
                        .clickable { /* onClick */ }
                        .padding(8.dp)
                ) {
                    Text(text = device.name, style = MaterialTheme.typography.titleMedium)
                    Text(text = device.address, style = MaterialTheme.typography.bodySmall)
                    if (device.manufacturerData.isNotBlank()) {
                        Text(
                            text = device.manufacturerData,
                            style = MaterialTheme.typography.bodySmall,
                            modifier = Modifier.padding(top = 4.dp)
                        )
                    }
                    Spacer(modifier = Modifier.height(4.dp))

                    Button(
                        onClick = {
                            onResult(device)
                        }
                    ) {
                        Text("Select")
                    }
                }
                HorizontalDivider()
            }
        }
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.padding(8.dp)
        ) {
            Button(
                onClick = {
                    onResult(null)
                }
            ) {
                Text("Close")
            }
            if (isScanning) {
                Spacer(modifier = Modifier.weight(1f)) // 간격

                CircularProgressIndicator(
                    strokeWidth = 2.dp,
                    modifier = Modifier.size(30.dp) // 버튼 높이에 맞게
                )
            }
        }
    }
}

@Composable
fun TimedScanView(
    onScanStart: () -> Unit,
    onScanStop: () -> Unit
) {
    val totalTimeMillis = 5000L
    var progress by remember { mutableStateOf(1f) }

    // 스캔과 타이머 동시 시작
    LaunchedEffect(Unit) {
        onScanStart()

        val startTime = withFrameNanos { it }
        var now: Long

        do {
            now = withFrameNanos { it }
            val elapsed = (now - startTime) / 1_000_000
            progress = 1f - (elapsed.toFloat() / totalTimeMillis)
        } while (elapsed < totalTimeMillis)

        progress = 0f
        onScanStop()
    }

    // UI
    Box(
        contentAlignment = Alignment.Center,
        modifier = Modifier.fillMaxSize()
    ) {
        CircularProgressIndicator(
            progress = { progress.coerceIn(0f, 1f) },
            strokeWidth = 6.dp,
            trackColor = ProgressIndicatorDefaults.circularTrackColor,
        )
        Text("${(progress * 5).toInt() + 1}s")
    }
}

@Preview
@Composable
fun TimedScanViewPreview() {
    TimedScanView(
        onScanStop = {},
        onScanStart = {}
    )
}