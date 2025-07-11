package com.example.xiangatewaypilot.ui

import android.widget.Button
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import com.example.xiangatewaypilot.BleScannerVM

@Composable
fun BleScannerScreen(viewModel: BleScannerVM) {
    val devices by viewModel.devices.collectAsState()
    var isScanning by remember { mutableStateOf(false) }
    val context = LocalContext.current

    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Button(
            onClick = {
                if (isScanning) {
                    viewModel.stopScan()
                } else {
                    viewModel.startScan()
                }
                isScanning = !isScanning
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
                            viewModel.connectToDevice(context, device.address)
                        }
                    ) {
                        Text("Connect")
                    }
                }
                HorizontalDivider()
            }
        }

    }
}