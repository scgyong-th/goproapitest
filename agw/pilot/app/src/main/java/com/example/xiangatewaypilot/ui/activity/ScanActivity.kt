package com.example.xiangatewaypilot.ui.activity

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Scaffold
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.xiangatewaypilot.model.scan.BleScannerVM
import com.example.xiangatewaypilot.ui.composable.BleScannerScreen
import com.example.xiangatewaypilot.ui.theme.XianGatewayPilotTheme

class ScanActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
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