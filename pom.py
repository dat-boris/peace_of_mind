"""
Copy and paste from http://pythonhosted.org/NeuroPy/
"""

import time
import six
from pprint import pprint

import progressbar
from NeuroPy import NeuroPy

DEBUG = False

#object1=NeuroPy("/dev/rfcomm0") for linux
#object1=NeuroPy("COM6") for windows
object1=NeuroPy('/dev/tty.MindWave')
bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)

if __name__=="__main__":
    print("Starting....")
    print(object1.start())

    while True:
        if DEBUG:
            pprint({
                attr: getattr(object1, attr, 'n/a')
                for attr in [
                    'attention',
                    'meditation',
                    'poorSignal',
                    'blinkStrengthrawValue',
                    'delta',
                    'theta'
                ]
            })

        # print(object1.meditation)
        bar.update(object1.meditation)
