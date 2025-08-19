from ..FileHandling     import SCPSaver
from ..FileHandling     import SCPEasyModifier


class MultipleSCPManager:
    def __init__(self, scp_data):
        self._scp_data   = scp_data

    def reinit(self, new_scp):
        self._scp_data = new_scp

    def set_drop_rate(self, new_drop_rate, save_files=True, do_reinit=False):
        new_scp = SCPEasyModifier().modify_scp_row(self._scp_data, "Multiple", "RowIndex", 3, "All_M", new_drop_rate)
        new_scp = SCPEasyModifier().modify_scp_row(new_scp,        "Multiple", "RowIndex", 3, "PC_M",  new_drop_rate)

        if save_files:
            SCPSaver().save_scp_file(new_scp, 'Multiple.scp')
        if do_reinit:
            self.reinit(new_scp)
            
        return new_scp