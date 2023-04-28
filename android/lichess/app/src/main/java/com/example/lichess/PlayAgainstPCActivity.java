package com.example.lichess;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.widget.Button;
import android.widget.RadioGroup;

import androidx.appcompat.app.AppCompatActivity;

public class PlayAgainstPCActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_play_pc);
        // Get references to the views
        RadioGroup colorRadioGroup = findViewById(R.id.group_choose_color);
        RadioGroup levelRadioGroup = findViewById(R.id.group_pc_level);

        // Get the SharedPreferences object
        SharedPreferences sharedPreferences = getSharedPreferences("com.example.lichess", MODE_PRIVATE);

        Button playAgainstPCButton = findViewById(R.id.btn_back_to_menu);
        playAgainstPCButton.setOnClickListener(v -> {
            Intent intent = new Intent(PlayAgainstPCActivity.this, MainActivity.class);
            startActivity(intent);
        });

    }
}
