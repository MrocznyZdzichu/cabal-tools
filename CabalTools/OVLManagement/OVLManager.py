import copy

from ..ABCBaseManager          import ABCBaseManager
from ..FileHandling.SCPData    import SCPData
from ..FileHandling.SCPPreview import SCPPreview

class OVLManager(ABCBaseManager):
    def __init__(self, scp_data: SCPData, dec_data, msg_data):
        super().__init__(scp_data=scp_data, dec_data=dec_data, msg_data=msg_data)