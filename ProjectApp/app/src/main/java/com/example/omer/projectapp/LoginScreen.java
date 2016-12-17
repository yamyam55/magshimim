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

public class LoginScreen extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login_screen);
        setTitle("Log in");

        /*final EditText fromserver = (EditText) findViewById(R.id.fromServer);
        final Button LoginButton = (Button) findViewById(R.id.LogInButton);
        LoginButton.setOnClickListener(new View.OnClickListener()
        {
            public void onClick(View v)
            {


                final EditText usernameText = (EditText) findViewById(R.id.UsernameText);
                final EditText passwordText = (EditText) findViewById(R.id.PasswordText);
                CharSequence username = usernameText.getText();
                CharSequence password = passwordText.getText();
                CharSequence toSend = username + " " + password;
                fromserver.setText(toSend);

                /*
                -----------------------
                ALL COMMUNICATION STUFF
                -----------------------
                 */
            /*
                Intent intent = new Intent(this, OptionsScreen.class);
                intent.putExtra("USERNAME!", usernameText.getText());
                startActivity(intent);
            }
        });*/

    }
    public void openSignInScreen(View view)
    {
        Intent intent = new Intent(this, SignUpScreen.class);
        startActivity(intent);
    }

    public void LogInPress(View view)
    {
        final EditText fromserver = (EditText) findViewById(R.id.fromServer);
        final EditText usernameText = (EditText) findViewById(R.id.UsernameText);
        final EditText passwordText = (EditText) findViewById(R.id.PasswordText);
        CharSequence username = usernameText.getText();
        CharSequence password = passwordText.getText();
        CharSequence toSend = username + " " + password;
        fromserver.setText(toSend);

                /*
                -----------------------
                ALL COMMUNICATION STUFF
                -----------------------
                 */

        Intent intent = new Intent(this, OptionsScreen.class);
        intent.putExtra("USERNAME", username);
        startActivity(intent);
    }

}
