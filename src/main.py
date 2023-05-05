import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

import platform
import os
if platform.machine() == 'aarch64':  # Jetson
    os.environ['OPENBLAS_CORETYPE'] = "ARMV8"

from dronekit import connect, Vehicle
from core import Core
from camera import setupCamera
from camera.base import BaseCamera
from utils.logging import setupLogging

import argparse
import time
import threading
import signal
import platform
import logging

PARENT_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

EXIT: bool         = False
core: Core         = None
vehicle: Vehicle   = None
camera: BaseCamera = None

def core_thread(core):
    global EXIT

    if EXIT:
        return

    logging.debug('Running core')
    core.run()
    logging.debug('Stopped core')

def stop():
    global EXIT, core, camera, vehicle

    EXIT = True

    if core:
        core.stop()

    if camera:
        camera.stop()

def signal_handler(sig, frame):
    stop()

def main(args):
    global EXIT, core, vehicle, camera

    thread = None

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    setupLogging(args.log_path, PARENT_DIRECTORY)
    camera = setupCamera(args.timelapse_path)

    if not EXIT:
        logging.info("Starting core")
        logging.info("Connecting to vehicle on: %s" % (args.uri,))
        vehicle = connect(args.uri, wait_ready=['gps_0', 'armed', 'mode', 'attitude'], rate=20)

        # Setup core thread
        core = Core(vehicle, camera)
        thread = threading.Thread(target=core_thread, args=(core,))
        thread.start()

        while not EXIT:
            time.sleep(1)

    # Signal handler will set the value of EXIT

    if thread:
        thread.join(5)

    logging.info('Thank you for travelling Matchstic Sea. We wish you a pleasant onward journey.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--uri', type=str, required=True, help="URI to connect with for MAVLink data. e.g., udp:127.0.0.1:14550")
    parser.add_argument('--log_path', type=str, required=False, default=os.path.join(PARENT_DIRECTORY, 'logs'), help="Path to save log output into")
    parser.add_argument('--timelapse_path', type=str, required=False, default=os.path.join(PARENT_DIRECTORY, 'timelapse'), help="Path to save timelapse frames into")

    args = parser.parse_args()

    main(args)