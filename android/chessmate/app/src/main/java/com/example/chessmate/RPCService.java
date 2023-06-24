package com.example.chessmate;

import android.util.Log;

import com.chessmate.command.CommandGrpc;
import com.chessmate.command.CommandRequest;
import com.chessmate.command.CommandResponse;

import java.net.SocketException;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;

public class RPCService {

    private static RPCService instance = null;
    private ManagedChannel channel;
    private CommandGrpc.CommandBlockingStub stub;
    private  boolean connected = false;
    private  RPCService() {}

    public static RPCService getInstance() {
        if (instance == null) {
            instance = new RPCService();
        }
        return instance;
    }

    public void start(String ip, int port) throws Exception {
        this.channel = ManagedChannelBuilder.forAddress(ip, port)
                .usePlaintext()
                .build();
        if (false) {
            Log.e("GRPC connection error", "Failed to create channel");
            throw new Exception("Connection failed");
        }
        this.stub = CommandGrpc.newBlockingStub(channel);
    }

    public CommandResponse execute(CommandRequest request) {
        if (!channel.isTerminated()) {
            CommandResponse res = this.stub.execute(request);
            return res;
        }
        Log.e("GRPC error", "failed to execute command");
        return null;
    }
}
