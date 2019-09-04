package com.example.photopi;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.google.android.material.bottomnavigation.BottomNavigationView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static android.provider.AlarmClock.EXTRA_MESSAGE;

public class MainActivity extends AppCompatActivity {

    BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //Button btnFire    = (Button) findViewById( R.id.btnFire ),
        //       btnConnect = (Button) findViewById( R.id.btnConnect );

        //btnFire.setClickable( false );

        BottomNavigationView navView = findViewById(R.id.nav_view);
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        AppBarConfiguration appBarConfiguration = new AppBarConfiguration.Builder(
                R.id.navigation_home, R.id.navigation_dashboard, R.id.navigation_notifications)
                .build();
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment);
        NavigationUI.setupActionBarWithNavController(this, navController, appBarConfiguration);
        NavigationUI.setupWithNavController(navView, navController);
    }

    /** Called when the user taps the Send button */
    public void sendFire(View view) {

        // Intent intent = new Intent(this, DisplayMessageActivity.class);
        Button btn = (Button) findViewById(R.id.btnFire);
        btn.setText( "Fired!" );
        // intent.putExtra(EXTRA_MESSAGE, message);
        // startActivity(intent);
    }

    /** Called when the user taps the Send button */
    public void sendConnect(View view) {

        Button btn = (Button) findViewById(R.id.btnFire);
        btn.setEnabled( false );

        if ( null != bluetoothAdapter ) {

            if ( !bluetoothAdapter.isEnabled() ) {

                Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                int REQUEST_ENABLE_BT = 1;
                startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
            }
            else {
                connect();
            }
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {

        if(resultCode == RESULT_OK){

            Button btn = (Button) findViewById(R.id.btnFire);
            btn.setEnabled( true );
        }
    }

    private void connect() {

        Set< BluetoothDevice > pairedDevices = bluetoothAdapter.getBondedDevices();

        if ( pairedDevices.size() > 0 ) {

            // There are paired devices. Get the name and address of each paired device.
            for (BluetoothDevice device : pairedDevices) {

                String deviceName = device.getName();
                String deviceHardwareAddress = device.getAddress(); // MAC address

                String id = "AEQ.*";
                Pattern pattern = Pattern.compile( id );
                Matcher match = pattern.matcher( deviceName );

                Log.e( "Bluetooth", "Matching patten" );
                if ( match.matches() ) {

                    Button btn = (Button) findViewById(R.id.btnFire);
                    btn.setEnabled(true);
                    btn.setText( deviceName );

                    Log.e( "Bluetooth", "Connecting" );
                    ConnectThread thread = new ConnectThread( device );

                    thread.run();
                }
            }
        }
    }
}
