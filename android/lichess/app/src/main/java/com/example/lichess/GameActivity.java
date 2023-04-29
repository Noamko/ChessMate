package com.example.lichess;

import android.os.Bundle;
import android.widget.TextClock;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

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
        Date time = null;
        try {
             time = sdf.parse(timeFromServer);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        TextView clock1 = findViewById(R.id.clock1);
        TextView clock2 = findViewById(R.id.clock2);


        if(time != null){
            clock1.setText(sdf.format(time));
        }

    }
}
