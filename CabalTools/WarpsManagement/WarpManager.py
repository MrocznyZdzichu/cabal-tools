from .WarpPointAdder import WarpPointAdder

from ..ABCBaseManager        import ABCBaseManager
from ..FileHandling.SCPData  import SCPData
from ..FileHandling.XMLSaver import XMLSaver


class WarpManager(ABCBaseManager):
    def __init__(self, scp_data: SCPData, dec_data):
        super().__init__(scp_data, dec_data, scp_target_filename='Warp.scp', dec_target_filename='warp.dec')

        self._warp_point_adder = WarpPointAdder()
    
    def add_warp_point(self, warp_point_item, save_files=True, do_reinit=False):
        new_dec = self._warp_point_adder.add_warp_point(
            self._dec_data, 
            self._scp_data, 
            warp_point_item=warp_point_item
        )
        if save_files:
            self.save()

        if do_reinit:
            self.reinit(new_dec=new_dec)

        return new_dec