package com.example.chessmate;

import android.content.DialogInterface;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import com.chessmate.command.CommandError;
import com.chessmate.command.CommandRequest;
import com.chessmate.command.CommandResponse;
import com.chessmate.command.EndTurnRequest;
import com.chessmate.command.ResetRequest;

import java.util.Timer;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.atomic.AtomicBoolean;

public class GameActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_game);

        TextView playerClock = findViewById(R.id.player_clock);
        TextView opponentClock = findViewById(R.id.opponent_clock);
        ExecutorService executorService = Executors.newFixedThreadPool(1);
        Bundle extras = getIntent().getExtras();
        if (extras == null) {
            Log.e("GameActivity", "extras is null");
            return;
        }
        // get color from intent
        boolean isWhite = getIntent().getBooleanExtra("isWhite", true);
        // get ai_elo from intent
        int ai_elo = getIntent().getIntExtra("ai_elo", 800);
        AtomicBoolean isPlayerTurn = new AtomicBoolean(isWhite);
        Thread clockThread = new Thread(() -> {
            Timer timer = new Timer();
            timer.scheduleAtFixedRate(new java.util.TimerTask() {
                int whiteTime = getIntent().getIntExtra("white_time", 1000 * 60 * 5);
                int blackTime = getIntent().getIntExtra("black_time", 1000 * 60 * 5);
                @Override
                public void run() {
                    if(isPlayerTurn.get()) {
                        whiteTime -= 1000;
                        int minutes = (int) (whiteTime / 60000);
                        int seconds = (int) ((whiteTime % 60000) / 1000);
                        String time = String.format("%02d:%02d", minutes, seconds);
                        playerClock.setText(time);
                        // dim the opponent clock
                        playerClock.setAlpha(1f);
                        opponentClock.setAlpha(0.5f);
                    } else{
                        blackTime -= 1000;
                        int minutes = (int) (blackTime / 60000);
                        int seconds = (int) ((blackTime % 60000) / 1000);
                        String time = String.format("%02d:%02d", minutes, seconds);
                        opponentClock.setText(time);
                        // dim the opponent clock
                        playerClock.setAlpha(0.5f);
                        opponentClock.setAlpha(1f);
                    }
                }
            }, 0, 1000);
        });
        AlertDialog.Builder alertDialogBuilder = new AlertDialog.Builder(this);
        alertDialogBuilder.setMessage("Press OK to start the game");
        alertDialogBuilder.setNegativeButton("Abort", (dialog, which) -> {
            dialog.cancel();
            finish();
        });

        alertDialogBuilder.setPositiveButton("OK", (dialog, which) -> {
            dialog.cancel();
            clockThread.start();
        });

        alertDialogBuilder.setCancelable(false);
        AlertDialog alertDialog = alertDialogBuilder.create();
        alertDialog.setOnShowListener(new DialogInterface.OnShowListener() {
            @Override
            public void onShow(DialogInterface dialog) {
                Button button = alertDialog.getButton(AlertDialog.BUTTON_POSITIVE);
                button.setGravity(android.view.Gravity.CENTER);
            }
        });
        alertDialog.show();

        playerClock.setOnClickListener(v -> {
            executorService.submit(() -> {
            if (isPlayerTurn.get()) {
                isPlayerTurn.set(false);
                EndTurnRequest endTurnRequest = EndTurnRequest.newBuilder().build();
                CommandRequest commandRequest = CommandRequest.newBuilder().setEndTurn(endTurnRequest).build();
                CommandResponse response = RPCService.getInstance().execute(commandRequest);
                CommandError error = response.getError();
                if(error.getCode() > 0) {
                    String msg = error.getMsg();
                    Log.e("GameActivity error: ", msg);
                }
                else {
                    isPlayerTurn.set(true);
                }
            }
            });
        });
    }
}
