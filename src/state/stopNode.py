from typing import Optional
from .baseNode import BaseNode

from . import Data, ExecutionState

class StopNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.state = ExecutionState.Stop

    def shouldTransition(self, data: Data) -> Optional[BaseNode]:
        return None