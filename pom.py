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


class StreeQueue(object):
    MAX_QUEUE_SIZE = 3
    STRESS_THRESHOLD = 50

    def __init__(self):
        self.queue_list = []

    def add(self, item):
        self.queue_list.insert(0, item)
        if len(self.queue_list) > self.MAX_QUEUE_SIZE:
            self.queue_list.pop()

    @property
    def avg_stress(self):
        return (
            float(sum(self.queue_list)) /
            max(len(self.queue_list), 1)
        )

    def check_is_stress(self):
        return self.avg_stress < self.STRESS_THRESHOLD


if __name__=="__main__":
    print("Starting....")
    print(mindwave_obj.start())

    sq = StreeQueue()
    is_stressed = False

    try:
        while True:
            if DEBUG: print_debug(mindwave_obj)
            # print(mindwave_obj.meditation)
            med_value = mindwave_obj.meditation

            sq.add(med_value)

            current_stress = sq.check_is_stress()
            if (current_stress != is_stressed):
                is_stressed = current_stress
                print("Stress: {}".format(current_stress))

            bar.update(med_value)

            logfile.write('{}\t{}\n'.format(
                datetime.now().replace(microsecond=0).isoformat(),
                med_value
            ))

            time.sleep(1)

    except KeyboardInterrupt:
        pass

    finally:
        mindwave_obj.stop()
        logfile.close()
