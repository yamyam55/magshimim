package com.example.omer.projectapp;

import android.app.Activity;
import android.content.Intent;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.EditText;
import java.io.*;
import java.net.Socket;

public class ChangeUserSettingsScreen extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_change_user_settings_screen);
        setTitle("Change User Settings");
    }

    public void savePress(View view)
    {
        /*
        -----------------------
        COMMUNICATION
        -----------------------
         */
        Snackbar snackbar = Snackbar.make(view , "Saved", Snackbar.LENGTH_SHORT);
        snackbar.show();
    }
}
