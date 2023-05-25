from .baseNode import BaseNode
from .startNode import StartNode
from .stopNode import StopNode
from .types import Hardware, ExecutionState
from camera.base import BaseCamera

from dronekit import Vehicle

class StateMachine:
    currentNode: BaseNode = None

    def start(self) -> None:
        self.currentNode = StartNode()

    def stop(self) -> None:
        self.currentNode = StopNode()

    @property
    def state(self) -> ExecutionState:
        return self.currentNode.state if self.currentNode != None else ExecutionState.Unknown

    def update(self, vehicle: Vehicle, camera: BaseCamera) -> ExecutionState:
        # Call from parent, who exits loop if this returns .Stop
        self.currentNode.update(Hardware(vehicle=vehicle, camera=camera))

        return self.currentNode.state

    def transition(self, newNode: BaseNode) -> None:
        self.currentNode = newNode

    def onStateUpdate(self, isArmed: bool, isConnected: bool) -> bool:
        # Ask the current node whether it wants to transition to the next node
        # given new state
        possibleNewNode = self.currentNode.shouldTransition(isArmed, isConnected)

        if possibleNewNode != None:
            self.transition(possibleNewNode)
            return True
        
        return False