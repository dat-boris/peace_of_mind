import six
import mindwave, time
from pprint import pprint

headset = mindwave.Headset(
    '/dev/tty.MindWave',
    #'7067'  # autoconnect
)
time.sleep(2)

headset.connect()
print("Connecting...")

while headset.status != 'connected':
    print headset.status
    time.sleep(0.5)
    if headset.status == 'standby':
        headset.connect()
        print("Retrying connect...")
print("Connected.")

try:
    while True:
        pprint({
            attr: getattr(headset, attr, 'n/a')
            for attr in [
                'attention', 'meditation', 'blink', 'poor_signal'
            ]
            })
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    print("Disconnecting")
    headset.disconnect()