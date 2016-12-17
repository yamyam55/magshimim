package com.example.omer.projectapp;

import android.app.Activity;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Button;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.EditText;
import java.io.*;
import java.net.Socket;

public class OptionsScreen extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_options_screen);

        setTitle("Options");
        CharSequence username = getIntent().getCharSequenceExtra("USERNAME");
        final TextView welcomwithusername = (TextView) findViewById(R.id.WelcomeWithUsername);
        welcomwithusername.setText("Wellcome " + username + "!");

    }
    public void CreateNewFontPress(View view)
    {
        Intent intent = new Intent(this, CreateNewFontScreen.class);
        startActivity(intent);
    }
    public void ChangeUserSettingsPress(View view)
    {
        Intent intent = new Intent(this, ChangeUserSettingsScreen.class);
        startActivity(intent);
    }
    public void ChangeUserFontsSettingsPress(View view)
    {
        Intent intent = new Intent(this, ChangeUserFontsSettingsScreen.class);
        startActivity(intent);
    }
    public void ConvertWrittenTextToComputerFontPress(View view)
    {
        Intent intent = new Intent(this, WrittenTextToComputerFontScreen.class);
        startActivity(intent);
    }
}
