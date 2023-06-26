package com.example.chessmate;

import android.os.Bundle;
import android.widget.Button;
import android.widget.TextClock;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.chessmate.command.CommandRequest;
import com.chessmate.command.CommandResponse;
import com.chessmate.command.EndTurnRequest;
import com.chessmate.command.EndTurnResponse;
import com.chessmate.command.GetClockRequest;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class GameActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_game);
        SimpleDateFormat sdf = new SimpleDateFormat("HH:mm");
        String timeFromServer = "12:34";

        Button button = findViewById(R.id.button2);

        button.setOnClickListener(v -> {
            EndTurnRequest endTurnRequest = EndTurnRequest.newBuilder().build();
            CommandRequest commandRequest = CommandRequest.newBuilder().setEndTurn(endTurnRequest).build();

            RPCService.getInstance().execute(commandRequest);
        });
    }
}
