package com.example.xiangatewaypilot.ui.activity

import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.location.LocationManager
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Scaffold
import androidx.compose.ui.Modifier
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.xiangatewaypilot.model.scan.BleScannerVM
import com.example.xiangatewaypilot.ui.composable.BleScannerScreen
import com.example.xiangatewaypilot.ui.theme.XianGatewayPilotTheme

class ScanActivity : ComponentActivity() {
    private val REQUEST_CODE: Int = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // TODO: 권한 관리 정리 필요
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            val permissions = arrayOf(
                android.Manifest.permission.BLUETOOTH_SCAN,
                android.Manifest.permission.BLUETOOTH_CONNECT
            )

            if (!permissions.all {
                    ContextCompat.checkSelfPermission(this, it) == PackageManager.PERMISSION_GRANTED
                }) {
                ActivityCompat.requestPermissions(this, permissions, REQUEST_CODE)
            }
        }

        enableEdgeToEdge()
        setContent {
            XianGatewayPilotTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    val vm: BleScannerVM = viewModel()
                    BleScannerScreen(vm) { device ->
                        device?.let {
                            val resultIntent = Intent().apply {
                                putExtra("device", it.toString())
                            }
                            setResult(RESULT_OK, resultIntent)
                        }
                        finish()
                    }
                }
            }
        }

        val locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager
        val isLocationEnabled = locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER)
        if (!isLocationEnabled) {
            startActivity(Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS))
        }
    }
}

//@Composable
//fun Greeting2(name: String, modifier: Modifier = Modifier) {
//    Text(
//        text = "Hello $name!",
//        modifier = modifier
//    )
//}
//
//@Preview(showBackground = true)
//@Composable
//fun GreetingPreview2() {
//    XianGatewayPilotTheme {
//        Greeting2("Android")
//    }
//}