package com.example.xiangatewaypilot

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.xiangatewaypilot.ui.BleScannerScreen
import com.example.xiangatewaypilot.ui.theme.XianGatewayPilotTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        GoProUuids.init(this)
        enableEdgeToEdge()
        setContent {
            val vm: BleScannerVM = viewModel()
            BleScannerScreen(viewModel = vm)
            //XianGatewayPilotTheme {
            //    Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
            //        MainScreen()
            //        //Greeting(
            //        //    name = "Android",
            //        //    modifier = Modifier.padding(innerPadding)
            //        //)
            //    }
            //}
        }
    }
}

@Composable
fun MainScreen() {
    val context = LocalContext.current

    LaunchedEffect(Unit) {
        // 앱 실행 시 Service 시작
        val intent = Intent(context, GatewayService::class.java)
        context.startService(intent)
    }

    Column(Modifier.padding(32.dp)) {
        Text("테스트 게이트웨이 앱")
        Spacer(modifier = Modifier.height(8.dp))
        Text("HTTP 서버가 백그라운드에서 실행 중입니다.")
    }

}
@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    XianGatewayPilotTheme {
        Greeting("Android")
    }
}

@Preview(showBackground = true)
@Composable
fun MainScreenPreview() {
    XianGatewayPilotTheme {
        MainScreen()
    }
}
