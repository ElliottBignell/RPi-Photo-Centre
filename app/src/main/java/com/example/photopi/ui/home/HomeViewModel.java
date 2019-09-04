package com.example.photopi.ui.home;

import android.os.Bundle;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

import com.example.photopi.R;

public class HomeViewModel extends ViewModel {

    private MutableLiveData<String> mText;

    public HomeViewModel() {

        mText = new MutableLiveData<>();
        mText.setValue("This is home fragment");
    }

    protected void onCreate(Bundle savedInstanceState) {

       /*if (bluetoothAdapter == null) {
            btnConnect.setEnabled( false );
        }*/
    }

    public LiveData<String> getText() {
        return mText;
    }
}
