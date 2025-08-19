from .WarpPointAdder import WarpPointAdder

from ..FileHandling.SCPSaver        import SCPSaver
from ..FileHandling.XMLSaver        import XMLSaver


class WarpManager:
    def __init__(self, dec_data, scp_data):
        self._dec_data = dec_data
        self._scp_data = scp_data

        self._warp_point_adder = WarpPointAdder()

    def reinit(self, new_dec, new_scp):
        self._dec_data = new_dec
        self._scp_data = new_scp

    def add_warp_point(self, warp_point_item, save_files=True, do_reinit=False):
        new_dec, new_scp = self._warp_point_adder.add_warp_point(
            self._dec_data, 
            self._scp_data, 
            warp_point_item=warp_point_item
        )
        if save_files:
            SCPSaver().save_scp_file(new_scp, 'Warp.scp')
            XMLSaver().save_dict_to_file(new_dec, 'warp.dec')

        if do_reinit:
            self.reinit(new_dec, new_scp)

        return new_dec, new_scp