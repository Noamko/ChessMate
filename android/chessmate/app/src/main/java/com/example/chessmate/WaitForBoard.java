package com.example.chessmate;

import androidx.appcompat.app.AppCompatActivity;

import android.app.VoiceInteractor;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;

import com.chessmate.command.CommandGrpc;
import com.chessmate.command.CommandRequest;
import com.chessmate.command.CommandResponse;
import com.chessmate.command.GetBoardStateRequest;

public class WaitForBoard extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_wait_for_board);

        RPCService rpc = RPCService.getInstance();
        GetBoardStateRequest boardStateRequest = GetBoardStateRequest.newBuilder().build();
        CommandRequest request  = CommandRequest.newBuilder()
                .setGetBoardState(boardStateRequest)
                                .build();

        long boarState = 0;
        long board_ready_state = -281474976645121L;
        while (boarState != board_ready_state) {
            CommandResponse response = rpc.execute(request);
            boarState = response.getGetBoardState().getState();

            // do more logic about the given state, maybe show it on the Screen
        }
        Intent intent = new Intent(this, GameActivity.class);
        startActivity(intent);
    }
}