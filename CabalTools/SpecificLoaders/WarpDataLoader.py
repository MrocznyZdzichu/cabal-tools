from .ABCSpecificLoader import ABCSpecificLoader

class WarpDataLoader(ABCSpecificLoader):
    def __init__(self, scp_path, dec_path):
        super().__init__(
            scp_path=scp_path, 
            dec_path=dec_path, 
            messages_path=None, 
            dec_section_start='<warp_point>', 
            dec_section_end='</warp_point>', 
            msg_section_start=None, 
            msg_section_end=None
        )

    def load(self):
        warp_dec_data = self._load_dec()
        warp_scp_data = self._load_scp_file()

        return warp_dec_data, warp_scp_data