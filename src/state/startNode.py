from typing import Optional

from .baseNode import BaseNode
from .cameraSnaphotNode import CameraSnapshotNode

from . import Data, ExecutionState

class StartNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.state = ExecutionState.Init

    def shouldTransition(self, data: Data) -> Optional[BaseNode]:
        return CameraSnapshotNode() if data.armed and data.connected else None