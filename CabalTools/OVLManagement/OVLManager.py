import copy

from ..FileHandling.SCPData    import SCPData
from ..FileHandling.SCPPreview import SCPPreview

class OVLManager:
    def __init__(self, scp_data: SCPData, dec_data, msg_data):
        self._scp_data = scp_data
        self._dec_data = dec_data
        self._msg_data = msg_data

        self._rich_scp = copy.deepcopy(scp_data)

    def preview_ovl(
            self,
            section_name=None,
            columns=None,
            filter_key=None,
            filter_val=None,
            filter_operator=None
        ):
        SCPPreview().preview(
            self._rich_scp.data,
            section_name=None,
            columns=None,
            filter_key=None,
            filter_val=None,
            filter_operator=None
        )
