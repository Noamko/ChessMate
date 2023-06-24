package com.example.chessmate;

import android.os.Bundle;
import android.widget.TextClock;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.chessmate.command.CommandRequest;
import com.chessmate.command.CommandResponse;
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
        // create a thread for the timers
        Thread timerThread = new Thread(new Runnable() {
            @Override
            public void run() {
                while(true){
                    try {
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                TextView clock1 = findViewById(R.id.clock1);
                                TextView clock2 = findViewById(R.id.clock2);
                                // get time from server
                                GetClockRequest getClockRequest = GetClockRequest.newBuilder().build();
                                CommandRequest request = CommandRequest.newBuilder().setGetClock(getClockRequest).build();
                                CommandResponse response = RPCService.getInstance().execute(request);
                                int whiteTime = response.getGetClock().getBlack();
                                int blackTIme = response.getGetClock().getWhite();

                                // convert millis to HH:mm
                                int whiteTimeInMinuts = whiteTime / 60000;
                                int whiteTimeInSeconds = (whiteTime % 60000) / 1000;
                                String whiteTimeStr = String.format("%02d:%02d", whiteTimeInMinuts, whiteTimeInSeconds);
                                int blackTimeInMinuts = blackTIme / 60000;
                                int blackTimeInSeconds = (blackTIme % 60000) / 1000;
                                String blackTimeStr = String.format("%02d:%02d", blackTimeInMinuts, blackTimeInSeconds);
                                clock1.setText(whiteTimeStr);
                                clock2.setText(blackTimeStr);
                            }
                        });
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        });

        timerThread.start();
    }
}
