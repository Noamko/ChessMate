package com.example.chessmate;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.widget.Button;
import android.widget.RadioGroup;

import androidx.appcompat.app.AppCompatActivity;

import com.chessmate.command.ChallengeAIRequest;
import com.chessmate.command.CommandRequest;
import com.chessmate.command.CommandResponse;
import com.chessmate.command.color;
import com.example.chessmate.R;
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
        RadioGroup levelRadioGroup = findViewById(R.id.group_pc_level);

        // Get the SharedPreferences object
        SharedPreferences sharedPreferences = getSharedPreferences("com.example.chessmate", MODE_PRIVATE);

        // Set the default values if they are not set yet
        if (!sharedPreferences.contains("color")) {
            SharedPreferences.Editor editor = sharedPreferences.edit();
            editor.putInt("color", R.id.rb_color_white);
            editor.apply();
        }
        if (!sharedPreferences.contains("level")) {
            SharedPreferences.Editor editor = sharedPreferences.edit();
            editor.putInt("level", R.id.rb_pc_easy);
            editor.apply();
        }

        // Set the selected values in the radio groups
        colorRadioGroup.check(sharedPreferences.getInt("color", R.id.rb_color_white));
        levelRadioGroup.check(sharedPreferences.getInt("level", R.id.rb_pc_easy));

        // Set listeners to save the selected values when changed
        colorRadioGroup.setOnCheckedChangeListener((group, checkedId) -> {
            SharedPreferences.Editor editor = sharedPreferences.edit();
            editor.putInt("color", checkedId);
            editor.apply();
        });
        levelRadioGroup.setOnCheckedChangeListener((group, checkedId) -> {
            SharedPreferences.Editor editor = sharedPreferences.edit();
            editor.putInt("level", checkedId);
            editor.apply();
        });
        Button returnToMenu = findViewById(R.id.btn_back_to_menu);
        returnToMenu.setOnClickListener(v -> {
            Intent intent = new Intent(PlayAgainstPCActivity.this, MainActivity.class);
            startActivity(intent);
        });

        Button play_button = findViewById(R.id.play);
        play_button.setOnClickListener(v -> {
            Intent intent = new Intent(PlayAgainstPCActivity.this, WaitForBoard.class);
            intent.putExtra("color", sharedPreferences.getInt("color", R.id.rb_color_white));
            intent.putExtra("level", sharedPreferences.getInt("level", R.id.rb_pc_medium));
            RPCService rpc = RPCService.getInstance();

            ChallengeAIRequest challengeAIRequest = ChallengeAIRequest.newBuilder()
                    .setColor(color.WHITE)
                    .setLevel(10)
                    .setBlackTimer(0)
                    .setWhiteTimer(0)
                    .build();
            rpc.execute(CommandRequest.newBuilder().setChallengeAI(challengeAIRequest).build());
            startActivity(intent);
        });
    }
}
