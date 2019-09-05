package com.example.photopi;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.util.Log;

import java.io.IOException;
import java.util.UUID;

public class ConnectThread extends Thread {

    private final BluetoothSocket mmSocket;
    private final BluetoothDevice mmDevice;
    BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
    BluetoothService service;

    private UUID guid = UUID.fromString("4866edd5-3667-4e5f-a07e-b076aa6fe453" );

    public ConnectThread(BluetoothDevice device, BluetoothService srv) {

        // Use a temporary object that is later assigned to mmSocket
        // because mmSocket is final.
        BluetoothSocket tmp = null;
        mmDevice = device;
        service = srv;

        try {
            // Get a BluetoothSocket to connect with the given BluetoothDevice.
            // MY_UUID is the app's UUID string, also used in the server code.
            tmp = device.createRfcommSocketToServiceRecord( guid );
        } catch (IOException e) {
            Log.e( "Bluetooth", "Socket's create() method failed", e );
        }
        mmSocket = tmp;
    }

    private void manageMyConnectedSocket() {

        Log.e( "Bluetooth", "managing socket" );
        service.start( mmSocket );
    }

    public void run() {

        // Cancel discovery because it otherwise slows down the connection.
        bluetoothAdapter.cancelDiscovery();

        try {
            // Connect to the remote device through the socket. This call blocks
            // until it succeeds or throws an exception.
            Log.e( "Bluetooth", "calling connect" );
            mmSocket.connect();
        } catch (IOException connectException) {
            // Unable to connect; close the socket and return.
            try {
                Log.e( "Bluetooth", "calling close" );
                mmSocket.close();
            } catch (IOException closeException) {
                Log.e( "Bluetooth", "Could not close the client socket", closeException );
            }
            return;
        }

        // The connection attempt succeeded. Perform work associated with
        // the connection in a separate thread.
        manageMyConnectedSocket();
    }

    // Closes the client socket and causes the thread to finish.
    public void cancel() {
        try {
            mmSocket.close();
        } catch (IOException e) {
            Log.e( "Bluetooth", "Could not close the client socket", e );
        }
    }
}

