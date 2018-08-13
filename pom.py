"""
Copy and paste from http://pythonhosted.org/NeuroPy/
"""

import time
import six
from pprint import pprint
from datetime import datetime

import click
import progressbar
from NeuroPy import NeuroPy

DEBUG = False

# object1=NeuroPy("/dev/rfcomm0") for linux
# object1=NeuroPy("COM6") for windows
mindwave_obj = NeuroPy('/dev/tty.MindWave')
bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
logfile = open('stress.log', 'a')


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
    MAX_QUEUE_SIZE = 65
    STRESS_THRESHOLD = 50
    # According to documentation, if it is same for 15 seconds
    # then it might be disconnected
    # But it also takes approx 1 min to warm up initially...
    MAX_SAME = 60

    assert MAX_SAME <= MAX_QUEUE_SIZE, "MAX_SAME must be less than MAX_QUEUE_SIZE"

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

    def is_disconnected(self):
        """ If value is the same, then it is stuck

        Except if it is zero, then possibly just we have
        taken off the headset!
        """
        if len(self.queue_list) < self.MAX_SAME:
            return False
        last_queues = self.queue_list[:self.MAX_SAME]
        unique_values = set(last_queues)
        return len(unique_values) == 1 and (0 not in unique_values)

    def reset(self):
        self.queue_list = []


@click.command()
@click.option('--verbose', default=False)
@click.option('--check_stress', default=False, help='Check for stress broundry')
def main(verbose, check_stress):
    print("Starting....")
    print(mindwave_obj.start())

    sq = StreeQueue()
    is_stressed = False

    try:
        while True:
            if verbose:
                print_debug(mindwave_obj)
                print(mindwave_obj.meditation)

            med_value = mindwave_obj.meditation

            sq.add(med_value)

            if (check_stress):
                current_stress = sq.check_is_stress()
                if (current_stress != is_stressed):
                    is_stressed = current_stress
                    print("Stress: {}".format(current_stress))

            if sq.is_disconnected():
                print("Disconnected.  Restarting....\n")
                mindwave_obj.stop()
                sq.reset()
                time.sleep(5)
                mindwave_obj.start()

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


if __name__ == "__main__":
    main()
