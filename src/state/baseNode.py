from __future__ import annotations
from typing import Optional

from . import Hardware, Data, ExecutionState

class BaseNode:
    state: ExecutionState = None

    def __init__(self):
        self.state = ExecutionState.Unknown

    def shouldTransition(self, data: Data) -> Optional[BaseNode]:
        return None
    
    def update(self, hardware: Hardware):
        pass