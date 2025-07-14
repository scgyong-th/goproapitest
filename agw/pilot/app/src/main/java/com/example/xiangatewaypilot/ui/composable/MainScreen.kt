package com.example.xiangatewaypilot.ui.composable

import android.app.Activity
import android.app.Application
import android.content.Intent
import android.util.Log
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.runtime.Composable
import androidx.compose.material3.*
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.xiangatewaypilot.model.scan.ScannedDeviceEntry
import com.example.xiangatewaypilot.model.main.BleModel
import com.example.xiangatewaypilot.ui.activity.ScanActivity

@Composable
fun MainScreen(viewModel: BleModel) {
    val selectedDevice by viewModel.selectedDevice.collectAsState()
    val context = LocalContext.current

    val launcher = rememberLauncherForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            val deviceDesc = result.data?.getStringExtra("device")
            Log.d("MainScreen", "Result from ScanActivity")
            deviceDesc?.let { desc ->
                val device = ScannedDeviceEntry.fromString(desc)
                device?.let { dev ->
                    viewModel.selectDevice(dev)
                    Log.d("MainScreen", dev.toString())
                }
            }
        }
    }
    Column(modifier = Modifier.fillMaxSize().padding(8.dp)) {
        Text(
            text = "Xian Android GateWay",
            fontSize = 24.sp,
            modifier = Modifier.padding(16.dp)
        )
        Text("Recent connected device:")
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Column(
                modifier = Modifier
                    .weight(1f)
                    .border(1.dp, Color.Blue)
                    .padding(4.dp)
            ) {
                Text(
                    text = selectedDevice?.name ?: "No Device",
                    fontWeight = FontWeight.Bold
                )
                Text(selectedDevice?.address ?: "Recent device not found")
            }
            Button(
                onClick = {
                    viewModel.connect()
                }
            ) {
                Text("Connect")
            }
        }
        Button(
            onClick = {
                val intent = Intent(context, ScanActivity::class.java)
                launcher.launch(intent)
            }
        ) {
            Text("Scan")
        }
    }
}

@Preview(showBackground = true)
@Composable
fun MainScreenPreview() {
    MainScreen(BleModel(Application()))
}
