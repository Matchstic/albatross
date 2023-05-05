import os
import logging
import sys

# See: https://stackoverflow.com/a/66209331
class LoggerWriter:
    def __init__(self, logfct):
        self.logfct = logfct
        self.buf = []

    def write(self, msg):
        if msg.endswith('\n'):
            self.buf.append(msg.removesuffix('\n'))
            self.logfct(''.join(self.buf))
            self.buf = []
        else:
            self.buf.append(msg)

    def flush(self):
        pass

def setupLogging(logpath: str, parentDir: str):
    # Setup the log file
    if not os.path.exists(logpath):
        logpath = os.path.join(parentDir, 'logs')

        print('WARNING Log path not found, redirecting to: ' + os.path.join(parentDir, 'logs'))

        # In the event the user has not got a relative `logs` folder
        if not os.path.exists(logpath):
            os.mkdir(logpath)

    fileCount = len(os.listdir(logpath))
    logFile = os.path.join(logpath, str(fileCount) + '.log')

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-15s %(levelname)-8s %(message)s",
        handlers=[
            logging.FileHandler(logFile),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger()

    # messing around with stdout for logging to file
    # this is nasty but whatever
    sys.stdout = LoggerWriter(logger.info)
    sys.stderr = LoggerWriter(logger.error)