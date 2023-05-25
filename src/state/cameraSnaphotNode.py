import time

from typing import Optional
from .baseNode import BaseNode
from .stopNode import StopNode

from .types import Hardware, Data, ExecutionState

class CameraSnapshotNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.state = ExecutionState.Camera

    def shouldTransition(self, data: Data) -> Optional[BaseNode]:
        if data.connected == False:
            return StopNode()
        
        return None
    
    def update(self, hardware: Hardware):
        hardware.camera.snapshot()
        time.sleep(5)