package com.example.chessmate;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.widget.Button;
import android.widget.RadioGroup;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.chessmate.command.ChallengeAIRequest;
import com.chessmate.command.CommandRequest;
import com.chessmate.command.CommandResponse;
import com.chessmate.command.color;
import com.example.chessmate.R;
import com.google.android.material.slider.Slider;
import com.google.type.Color;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;

public class PlayAgainstPCActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_play_pc);

        // Get references to the views
        RadioGroup colorRadioGroup = findViewById(R.id.group_choose_color);

        // Get the SharedPreferences object
        SharedPreferences sharedPreferences = getSharedPreferences("com.example.chessmate", MODE_PRIVATE);
        Slider eloSlider = findViewById(R.id.elo_slider);

        eloSlider.addOnChangeListener((slider, value, user) -> {
//            eloText.setText(String.valueOf((int)(value)));
            SharedPreferences.Editor editor = sharedPreferences.edit();
            editor.putInt("ai_elo", (int)value);
            editor.apply();
        });

        // Set the default values if they are not set yet
        if (!sharedPreferences.contains("color")) {
            SharedPreferences.Editor editor = sharedPreferences.edit();
            editor.putInt("color", R.id.rb_color_white);
            editor.apply();
        }
        if (!sharedPreferences.contains("level")) {
            SharedPreferences.Editor editor = sharedPreferences.edit();
            editor.apply();
        }

        // Set listeners to save the selected values when changed
        colorRadioGroup.setOnCheckedChangeListener((group, checkedId) -> {
            SharedPreferences.Editor editor = sharedPreferences.edit();
            editor.putInt("color", checkedId);
            editor.apply();
        });

        Button play_button = findViewById(R.id.play);
        play_button.setOnClickListener(v -> {
            Intent intent = new Intent(PlayAgainstPCActivity.this, WaitForBoard.class);
            intent.putExtra("isWhite", colorRadioGroup.getCheckedRadioButtonId() == R.id.rb_color_white);
            intent.putExtra("ai_elo", (int)eloSlider.getValue());
            intent.putExtra("black_time",1000 * 60 * 5);
            intent.putExtra("white_time",1000 * 60 * 5);
            startActivity(intent);
        });
    }
}
