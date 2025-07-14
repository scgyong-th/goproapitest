package com.example.xiangatewaypilot.ui.activity

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.xiangatewaypilot.constants.GoProUuids
import com.example.xiangatewaypilot.model.main.BleModel
import com.example.xiangatewaypilot.ui.composable.MainScreen

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        GoProUuids.init(this)
        enableEdgeToEdge()
        setContent {
            val vm: BleModel = viewModel()
            MainScreen(viewModel = vm)
        }
    }

}

//enableEdgeToEdge()
//setContent {
//    val vm: BleScannerVM = viewModel()
//    val lastDevice = BleDevice.load(this)
//    Log.d("MainActivity", "lastDevice=" + lastDevice.toString())
//    BleScannerScreen(viewModel = vm, lastDevice = lastDevice)
//}


//@Composable
//fun MainScreen() {
//    val context = LocalContext.current
//
//    LaunchedEffect(Unit) {
//        // 앱 실행 시 Service 시작
//        val intent = Intent(context, GatewayService::class.java)
//        context.startService(intent)
//    }
//
//    Column(Modifier.padding(32.dp)) {
//        Text("테스트 게이트웨이 앱")
//        Spacer(modifier = Modifier.height(8.dp))
//        Text("HTTP 서버가 백그라운드에서 실행 중입니다.")
//    }
//
//}
//@Composable
//fun Greeting(name: String, modifier: Modifier = Modifier) {
//    Text(
//        text = "Hello $name!",
//        modifier = modifier
//    )
//}
//
//@Preview(showBackground = true)
//@Composable
//fun GreetingPreview() {
//    XianGatewayPilotTheme {
//        Greeting("Android")
//    }
//}
//
//@Preview(showBackground = true)
//@Composable
//fun MainScreenPreview() {
//    XianGatewayPilotTheme {
//        MainScreen()
//    }
//}
