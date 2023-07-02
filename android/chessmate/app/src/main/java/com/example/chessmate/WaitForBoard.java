package com.example.chessmate;

import androidx.appcompat.app.AppCompatActivity;

import android.app.VoiceInteractor;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.chessmate.command.ChallengeAIRequest;
import com.chessmate.command.CommandError;
import com.chessmate.command.CommandGrpc;
import com.chessmate.command.CommandRequest;
import com.chessmate.command.CommandResponse;
import com.chessmate.command.GetBoardStateRequest;
import com.chessmate.command.color;

public class WaitForBoard extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_wait_for_board);
        Bundle bundle = getIntent().getExtras();
        if (bundle == null) {
            Log.e("WaitForBoard", "bundle is null");
            return;
        }
        TextView wait_screen_text = findViewById(R.id.wait_screen_text);
        RPCService rpc = RPCService.getInstance();
        ChallengeAIRequest challengeAIRequest = ChallengeAIRequest.newBuilder()
                .setColor(bundle.getBoolean("isWhite") ? color.WHITE : color.BLACK)
                .setLevel(bundle.getInt("ai_elo"))
                .build();

        CommandResponse response = rpc.execute(CommandRequest.newBuilder().setChallengeAI(challengeAIRequest).build());
        CommandError error = response.getError();
        if (error.getCode() != 0) {
            String msg = "Error: " + error.getCode() + " " + error.getMsg();
            wait_screen_text.setText(msg);
            return;
        }
        Intent intent = new Intent(this, GameActivity.class);
        intent.putExtras(bundle);
        startActivity(intent);
    }
}