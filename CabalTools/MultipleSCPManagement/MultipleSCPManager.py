from ..FileHandling.SCPData import SCPData


class MultipleSCPManager:
    def __init__(self, scp_data: SCPData):
        self._scp_data   = scp_data

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
            self._scp_data.save_to_file('Multiple.scp')