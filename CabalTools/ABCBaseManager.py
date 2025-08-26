import copy
from abc import ABC, abstractmethod

from .FileHandling.SCPData    import SCPData
from .FileHandling.SCPPreview import SCPPreview
from .FileHandling.XMLSaver   import XMLSaver


class ABCBaseManager(ABC):
    def __init__(self, scp_data: SCPData = None, dec_data=None, msg_data=None, scp_target_filename=None, dec_target_filename=None):
        self._scp_data            = scp_data
        self._dec_data            = dec_data
        self._msg_data            = msg_data
        self._scp_target_filename = scp_target_filename
        self._dec_target_filename = dec_target_filename
        self._enriched_data       = self._enrich_scp() if scp_data else None

    def _enrich_scp(self):
        return copy.deepcopy(self._scp_data.data)

    def reinit(self, new_scp=None, new_dec=None):
        if new_scp:
            self._scp_data = new_scp
        if new_dec:
            self._dec_data = new_dec

        self._enriched_data = self._enrich_scp()

    def preview(self, section_name=None, columns=None, filter_key=None, filter_val=None, filter_operator=None, suppress=False):
        return SCPPreview().preview(
            self._enriched_data,
            section_name    = section_name,
            columns         = columns,
            filter_key      = filter_key,
            filter_val      = filter_val,
            filter_operator = filter_operator,
            suppress        = suppress
        )

    def save(self):
        if self._scp_data and self._scp_target_filename:
            self._scp_data.save_to_file(self._scp_target_filename)
        if self._dec_data and self._dec_target_filename:
            XMLSaver().save_dict_to_file(self._dec_data, self._dec_target_filename)


def can_reconfig(func):
    def wrapper(self, *args, do_reinit=True, save_files=True, **kwargs):
        result = func(self, *args, **kwargs)

        if do_reinit:
            self.reinit()
        if save_files:
            self.save()

        return result
    return wrapper
