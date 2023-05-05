import os
import threading
import time
from ..constants import TIMELAPSE_INTERVAL_MS

THREAD_STOP = False
RUNNING     = False

def thread(snapshotFn, interval):
    global THREAD_STOP, RUNNING

    print('Camera started')
    RUNNING = True

    while THREAD_STOP == False:
        start = time.time_ns() // 1_000_000
        snapshotFn()
        end = time.time_ns() // 1_000_000

        elapsed = end - start
        remaining = interval - elapsed
        if remaining <= 0: continue

        # Wait remaining time until next interval
        time.sleep(remaining / 1_000)

    RUNNING = False

    print('Camera stopped')

class BaseCamera:

    _thread = None

    def __init__(self, directory):
        self.directory = directory

        if not os.path.exists(directory):
            os.makedirs(directory)

    def available(self):
        return False

    def running(self):
        global RUNNING

        return RUNNING

    def start(self):
        self._thread = threading.Thread(target=thread, args=(self.snapshot, TIMELAPSE_INTERVAL_MS))
        self._thread.start()

    def stop(self):
        global THREAD_STOP
        THREAD_STOP = True

        self._thread.join(5)

    def snapshot(self):
        pass
