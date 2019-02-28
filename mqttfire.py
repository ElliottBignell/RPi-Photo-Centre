import paho.mqtt.client as mqtt
import time

def on_message( client, userdata, message ):
    print( "Recv. ", str( message.payload.decode( "utf-8" ) ) )
    print( "Topic: ", message.topic )

broker_address = "127.0.0.1"

client = mqtt.Client( "P1" )
client.on_message = on_message

client.connect( broker_address )
client.loop_start()

client.subscribe( "camera/go" )

time.sleep( 30 )
client.loop_stop()
