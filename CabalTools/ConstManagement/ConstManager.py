from ..FileHandling.SCPData import SCPData


class ConstManager:
    def __init__(self, scp_data: SCPData):
        self._scp_data = scp_data

    def set_drops_count_per_kill(self, new_drop_count, save_files=True):
        self._scp_data.modify_field(
            section_name   = "Multiple_Base",
            item_key_field = "RowIndex",
            item_key_value = 2,
            field_name     = "Value",
            new_value      = new_drop_count,
        )

        if save_files:
            self._scp_data.save_to_file('Const.scp')
