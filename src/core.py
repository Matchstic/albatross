import time

from enum import Enum
from constants import HEARTBEAT_TIMEOUT

from dronekit import Vehicle
from camera.base import BaseCamera
from state import StateMachine

class ExecutionState(str, Enum):
    Init           = "INIT"
    AwaitingArm    = "AWAITING_ARM"
    Running        = "RUNNING"
    ConnectionLoss = "CONNECTION_LOSS"
    Stop           = "STOP"

class Core:
    vehicle: Vehicle = None
    camera: BaseCamera = None
    statemachine: StateMachine = StateMachine()

    def __init__(self, vehicle: Vehicle, camera: BaseCamera):
        self.camera = camera
        self.vehicle = vehicle

        # Setup vehicle etc
        self.vehicle.add_attribute_listener('armed', self.armedCallback)
        self.vehicle.add_attribute_listener('last_heartbeat', self.lastHeartbeatCallback)

        # Enter ready state
        self.statemachine.start()

    #### Callbacks

    def armedCallback(self, _, _1, _2) -> None:
        print("Vehicle armed %d" % (self.vehicle.armed,))

        self.statemachine.onStateUpdate(self.vehicle.armed, self.isConnected)

    def lastHeartbeatCallback(self, _, _1, _2) -> None:
        self.statemachine.onStateUpdate(self.vehicle.armed, self.isConnected)

    #### Getters

    @property
    def isConnected(self) -> bool:
        return self.vehicle.last_heartbeat < HEARTBEAT_TIMEOUT

    #### State machine

    def run(self) -> None:
        stopped = False

        while stopped == False:
            stopped = self.statemachine.update(self.vehicle, self.camera) == ExecutionState.Stop

            time.sleep(0.02)

    def stop(self) -> None:
        self.statemachine.stop()

        # Cleanup
        self.vehicle.close()