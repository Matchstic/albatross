from enum import Enum
import time
from typing import Callable

from camera.base import BaseCamera

class ExecutionState(str, Enum):
    Unknown        = "UNKNOWN"
    Init           = "INIT"
    Running        = "RUNNING"
    ConnectionLoss = "CONNECTION_LOSS"
    Stop           = "STOP"

class ExecutionGraphNode:
    state: ExecutionState = None
    decider: Callable[[bool], ExecutionState] = None

    def __init__(self, state: ExecutionState, decider: Callable[[bool], ExecutionState]):
        self.state = state
        self.decider = decider

executionGraph: dict[ExecutionState, ExecutionGraphNode] = {
    ExecutionState.Init: ExecutionGraphNode(ExecutionState.Init, lambda isArmed: ExecutionState.Running if isArmed else ExecutionState.Init),
    ExecutionState.Running: ExecutionGraphNode(ExecutionState.Running, lambda _: ExecutionState.Running),
    ExecutionState.ConnectionLoss: ExecutionGraphNode(ExecutionState.Running, lambda _: ExecutionState.Stop),
    ExecutionState.Stop: ExecutionGraphNode(ExecutionState.Running, lambda _: ExecutionState.Stop),
}

class StateMachine:
    camera: BaseCamera = None
    currentNode: ExecutionGraphNode = None

    def __init__(self, camera: BaseCamera) -> None:
        self.camera = camera

    def start(self) -> None:
        self.currentNode = executionGraph[ExecutionState.Init]

    def stop(self) -> None:
        self.currentNode = executionGraph[ExecutionState.Stop]

    @property
    def state(self) -> ExecutionState:
        return self.currentNode.state if self.currentNode != None else ExecutionState.Unknown

    def update(self) -> ExecutionState:
        # Call from parent, who exits loop if this returns .Stop

        if self.state is ExecutionState.Init:
            # Do nothing during setup.
            pass
        elif self.state is ExecutionState.Running:
            # Snapshot every 5s
            self.camera.snapshot()
            time.sleep(5)
        elif self.state is ExecutionState.ConnectionLoss:
            # until reconnected, nothing we can do.
            pass

        return self.state

    def transition(self, newState: ExecutionState) -> None:
        self.currentNode = executionGraph[newState]

    def onStateUpdate(self, isArmed: bool) -> bool:
        # Ask the current node whether it wants to transition to the next node
        # given new state
        possibleNewState = self.currentNode.decider(isArmed)

        if possibleNewState != self.state:
            self.transition(possibleNewState)
            return True
        
        return False