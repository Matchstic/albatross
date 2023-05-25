from enum import Enum
from dataclasses import dataclass
from camera.base import BaseCamera

from dronekit import Vehicle

@dataclass
class Hardware:
    camera: BaseCamera
    vehicle: Vehicle

@dataclass
class Data:
    armed: bool
    connected: bool

class ExecutionState(str, Enum):
    Unknown        = "UNKNOWN"
    Init           = "INIT"
    Camera         = "CAMERA"
    Stop           = "STOP"