"""
Copy and paste from http://pythonhosted.org/NeuroPy/
"""

import time
import six
from pprint import pprint
from datetime import datetime

import progressbar
from NeuroPy import NeuroPy

DEBUG = False

#object1=NeuroPy("/dev/rfcomm0") for linux
#object1=NeuroPy("COM6") for windows
mindwave_obj = NeuroPy('/dev/tty.MindWave')
bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
logfile = open('stress.log','a')

def print_debug(obj):
    pprint({
        attr: getattr(obj, attr, 'n/a')
        for attr in [
            'attention',
            'meditation',
            'poorSignal',
            'blinkStrengthrawValue',
            'delta',
            'theta'
        ]
    })


if __name__=="__main__":
    print("Starting....")
    print(mindwave_obj.start())

    try:
        while True:
            if DEBUG: print_debug(mindwave_obj)
            # print(mindwave_obj.meditation)
            bar.update(mindwave_obj.meditation)

            logfile.write('{}\t{}\n'.format(
                datetime.now().replace(microsecond=0).isoformat(),
                mindwave_obj.meditation
            ))
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    finally:
        mindwave_obj.stop()
        logfile.close()
