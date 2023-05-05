import os
import logging
from typing import Union

from .raspicam import RaspiCamera
from .mock import MockCamera

def cameraClass():
  if RaspiCamera.available(): return RaspiCamera
  return MockCamera

def setupCamera(path: str) -> Union[RaspiCamera, MockCamera, None]:
  logging.info('Saving videos to: ' + path)

  if not os.path.exists(path):
      logging.warning('Video path ' + path + ' does not exist, not recording video.')
      return None
  else:
      fileCount = len(os.listdir(path))
      directory = os.path.join(path, str(fileCount))
      return cameraClass()(directory)