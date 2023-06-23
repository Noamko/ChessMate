package com.example.lichess;

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

import java.io.IOException;
import java.util.UUID;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button playAgainstPCButton = findViewById(R.id.Play_against_pc);

        playAgainstPCButton.setOnClickListener(v -> {
            Intent intent = new Intent(MainActivity.this, PlayAgainstPCActivity.class);
            startActivity(intent);
        });
        ManagedChannel channel = ManagedChannelBuilder.forAddress("10.0.0.178", 50051)
                .usePlaintext()
                .build();

        CommandGrpc.CommandBlockingStub stuv = CommandGrpc.newBlockingStub(channel);
        CommandRequest req = CommandRequest.newBuilder()
                .setChallengeAI(ChallengeAIRequest.newBuilder()
                        .setColorValue(1)
                        .setLevel(12).build()).build();
        stuv.execute(req);

        channel.shutdown();
    }
}
