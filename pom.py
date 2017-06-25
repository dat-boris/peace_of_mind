import time
import six
from NeuroPy import NeuroPy


#object1=NeuroPy("COM6")

object1=NeuroPy('/dev/tty.MindWave')
#If port not given 57600 is automatically assumed
#object1=NeuroPy("/dev/rfcomm0") for linux

def attention_callback(attention_value):
    "this function will be called everytime NeuroPy has a new value for attention"
    print "Value of attention is", attention_value
    #do other stuff (fire a rocket), based on the obtained value of attention_value
    #do some more stuff
    return None


#set call back:
object1.setCallBack("attention",attention_callback)

#call start method
print("Starting....")
print(object1.start())

while True:
    print("Meditation: {}".format(object1.meditation))
    time.sleep(1)
    if(object1.meditation>70): #another way of accessing data provided by headset (1st being call backs)
        object1.stop()         #if meditation level reaches above 70, stop fetching data from the headset