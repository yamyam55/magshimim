package com.example.omer.projectapp;

import android.app.Activity;
import android.content.Intent;
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

public class SignUpScreen extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_up_screen);
        setTitle("Sign Up");
    }
    public void SignUpPress(View view)
    {
        /*
        ----------------------------
         SEND TO SERVER
         ---------------------------
         */

        Intent intent = new Intent(this, LoginScreen.class);
        startActivity(intent);
    }

}
