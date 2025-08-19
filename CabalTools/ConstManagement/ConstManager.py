from .MultiDropModifier import MultiDropModifier
from ..FileHandling     import SCPSaver

class ConstManager:
    def __init__(self, scp_data):
        self._scp_data   = scp_data
        self._multi_drop = MultiDropModifier()

    def reinit(self, new_scp):
        self._scp_data = new_scp

    def set_drops_count_per_kill(self, new_drop_count, save_files=True, do_reinit=False):
        new_scp = self._multi_drop.set_multidrop(self._scp_data, new_drop_count)

        if save_files:
            SCPSaver().save_scp_file(new_scp, 'Const.scp')
        if do_reinit:
            self.reinit(new_scp)
            
        return new_scp