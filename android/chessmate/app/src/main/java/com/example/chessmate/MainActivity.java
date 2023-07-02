package com.example.chessmate;

import androidx.annotation.RequiresPermission;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.provider.Settings;
import android.widget.Button;

//import com.example.helloworldgrpc.GreeterGrpc;
//import com.example.helloworldgrpc.HelloReply;
//import com.example.helloworldgrpc.HelloRequest;

import com.chessmate.command.ChallengeAIRequest;
import com.chessmate.command.CommandGrpc;
import com.chessmate.command.CommandRequest;
import com.chessmate.command.ResetRequest;

import java.io.IOException;
import java.util.UUID;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;

public class MainActivity extends AppCompatActivity {
    private Thread.UncaughtExceptionHandler defaultUEH;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        defaultUEH = Thread.getDefaultUncaughtExceptionHandler();
        Thread.setDefaultUncaughtExceptionHandler(_unCaughtExceptionHandler);

        String ip = "10.0.0.178";
        int port = 50051;
        try {
            RPCService.getInstance().start(ip, port);
            RPCService.getInstance().execute(CommandRequest.newBuilder().setReset(ResetRequest.newBuilder().build()).build());
        } catch (Exception e) {
            Intent intent = new Intent(this, ErrorActivity.class);
            intent.putExtra("message", String.format("Cant connect to: %s: %d", ip, port));
            startActivity(intent);

        }
        Button playAgainstPCButton = findViewById(R.id.Play_against_pc);

        playAgainstPCButton.setOnClickListener(v -> {
            Intent intent = new Intent(MainActivity.this, PlayAgainstPCActivity.class);
            startActivity(intent);
        });
    }
    private Thread.UncaughtExceptionHandler _unCaughtExceptionHandler = new Thread.UncaughtExceptionHandler() {
        @Override
        public void uncaughtException(Thread thread, Throwable ex) {
            ex.printStackTrace();
            RPCService.getInstance().execute(
                    CommandRequest.newBuilder()
                            .setReset(ResetRequest.newBuilder().build()).build());

            // TODO handle exception here
        }
    };
}
