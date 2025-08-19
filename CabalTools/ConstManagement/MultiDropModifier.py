from ..FileHandling.SCPEasyModifier import SCPEasyModifier


class MultiDropModifier:
    def __init__(self):
        pass

    def set_multidrop(self, scp_data, new_value):
        return SCPEasyModifier().modify_scp_row(scp_data, 'Multiple_Base', 'RowIndex', 2, 'Value', new_value)