package com.example.lichess;
import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;

import com.example.helloworldgrpc.GreeterGrpc;
import com.example.helloworldgrpc.HelloReply;
import com.example.helloworldgrpc.HelloRequest;

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

        GreeterGrpc.GreeterBlockingStub stub = GreeterGrpc.newBlockingStub(channel);
//
        HelloRequest request =  HelloRequest.newBuilder()
                .setName("Bobiboten").build();
        HelloReply res = stub.sayHello(request);
//
//        System.out.println(res.getMessage());
//        channel.shutdown();
    }
}
