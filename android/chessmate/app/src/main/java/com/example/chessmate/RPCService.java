package com.example.chessmate;

import com.chessmate.command.CommandGrpc;
import com.chessmate.command.CommandRequest;
import com.chessmate.command.CommandResponse;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;

public class RPCService {

    private static RPCService instance = null;
    private ManagedChannel channel;
    private CommandGrpc.CommandBlockingStub stub;
    private  RPCService() {
        this.channel = ManagedChannelBuilder.forAddress("10.0.0.127", 50000)
                .usePlaintext()
                .build();
        this.stub = CommandGrpc.newBlockingStub(channel);
    }

    public static RPCService getInstance() {
        if (instance == null) {
            instance = new RPCService();
        }
        return instance;
    }

    public CommandResponse execute(CommandRequest request) {
        CommandResponse res = this.stub.execute(request);
        return res;
    }
}
