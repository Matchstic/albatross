import subprocess
import os
from .base import BaseCamera

class RaspiCamera(BaseCamera):
    '''
    A camera implementation that wraps raspistill stuff.
    '''

    def available():
        return True

    def snapshot(self):
        fileCount = len(os.listdir(self.directory))
        filename = os.path.join(self.directory, str(fileCount) + '.jpg')

        cmd = "raspistill -t 1 -w 1080 -h 1920 -q 80 -ex auto -awb auto -o " + filename
        subprocess.call(cmd, shell = True)
