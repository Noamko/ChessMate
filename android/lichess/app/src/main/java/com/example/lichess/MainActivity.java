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

import com.chessmate.game.ChallengeAIRequest;
import com.chessmate.game.ChallengeAIResponse;
import com.chessmate.game.GameGrpc;
import com.chessmate.game.GetClockRequest;
import com.chessmate.game.GetClockResponse;

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
//        try {
//            String uuid = Settings.Secure.getString(getContentResolver(), Settings.Secure.ANDROID_ID);
//            System.out.println("UUID iS: ");
//            System.out.println(uuid);
//            UUID _uuid = UUID.nameUUIDFromBytes(uuid.getBytes("utf8"));
//
//            BluetoothSocket bluetoothSocket = device.createInsecureRfcommSocketToServiceRecord(UUID.fromString("7c8c2c7e-e69e-11ed-bb7c-315decf58528"));
//            bluetoothSocket.connect();
//        } catch (SecurityException e) {
//            throw new RuntimeException(e);
//        } catch (IOException e) {
//            throw new RuntimeException(e);
//        }
        ManagedChannel channel = ManagedChannelBuilder.forAddress("10.0.0.178", 50051)
                .usePlaintext()
                .build();

        GameGrpc.GameBlockingStub stub = GameGrpc.newBlockingStub(channel);
        int i = 0;
        while (true) {
            ChallengeAIRequest request = ChallengeAIRequest.newBuilder()
                    .setAiLevel(i)
                    .setColor(i)
                    .build();
            ChallengeAIResponse res = stub.challengeAI(request);
            i++;

        }
//        channel.shutdown();
    }
}
