from ..ABCBaseManager       import ABCBaseManager
from ..FileHandling.SCPData import SCPData


class MultipleSCPManager(ABCBaseManager):
    def __init__(self, scp_data: SCPData):
        super().__init__(scp_data=scp_data, scp_target_filename='Multiple.scp')

    def set_drop_rate(self, new_drop_rate, save_files=True):
        self._scp_data.modify_field(
            section_name   = "Multiple",
            item_key_field = "RowIndex",
            item_key_value = 3,
            field_name     = "All_M",
            new_value      = new_drop_rate,
        )
        self._scp_data.modify_field(
            section_name   = "Multiple",
            item_key_field = "RowIndex",
            item_key_value = 3,
            field_name     = "PC_M",
            new_value      = new_drop_rate,
        )
        
        if save_files:
            self.save()