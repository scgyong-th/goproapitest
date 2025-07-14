package com.example.xiangatewaypilot.ui.activity

import android.annotation.SuppressLint
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.xiangatewaypilot.constants.GoProUuids
import com.example.xiangatewaypilot.httpd.GatewayService
import com.example.xiangatewaypilot.model.main.BleModel
import com.example.xiangatewaypilot.ui.composable.MainScreen

class MainActivity : ComponentActivity() {
    private lateinit var vm: BleModel
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        GoProUuids.init(this)
        enableEdgeToEdge()

        vm = ViewModelProvider(this)[BleModel::class.java]

        setContent {
            MainScreen(viewModel = vm)
        }
    }

    @SuppressLint("UnspecifiedRegisterReceiverFlag")
    override fun onStart() {
        super.onStart()
        registerReceiver(receiver, IntentFilter("com.thinkware.xian.msg.web"))

        val intent = Intent(this, GatewayService::class.java)
        this.startService(intent)
    }

    override fun onStop() {
        unregisterReceiver(receiver)
        super.onStop()
    }

    val receiver = object: BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            val path = intent?.getStringExtra("path")?: ""
            Log.d("MainActivity", "Broadcast Receiver received: $path.")

            when {
                path == "connect" -> {
                    vm.connect()
                }
            }
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
