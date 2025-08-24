import copy

from ..ABCBaseManager          import ABCBaseManager
from ..FileHandling.SCPData    import SCPData


class OVLManager(ABCBaseManager):
    def __init__(self, scp_data: SCPData, dec_data, msg_data, names: dict, forcecodes: dict):
        self._names      = names
        self._forcecodes = forcecodes
        super().__init__(
            scp_data=scp_data,
            dec_data=dec_data,
            msg_data=msg_data,
            scp_target_filename="Overloadmastery.scp",
            dec_target_filename="overloadmastery.dec",
        )

    def _enrich_scp(self):
        new_scp = super()._enrich_scp()

        for section in new_scp:
            for entry in section['entries']:
                if section['section'] == 'Overloadmastery_Base':
                    entry['MasteryName'] = self._names.get(entry['mastery_index'])
                    entry['PreMasteryName'] = self._names.get(entry['premastery_idx'])
                
                if section['section'] == 'Overloadmastery_Value':
                    entry['MasteryName'] = self._names.get(entry['Mastery_index'])
                    entry['StatName'] = self._forcecodes.get(entry['forcecode_num'])

        return new_scp
    
    def _modify_entry(self, entry, is_dec, usepoint=None, forcecode_num=None ,forcecode_value=None, value_type=None):
        if is_dec:
            entry = entry['attributes']
        if usepoint is not None:
            entry['usepoint'] = usepoint
        if forcecode_num is not None:
            entry['forcecode_num'] = forcecode_num
        if forcecode_value is not None:
            entry['forcecode_value'] = forcecode_value
        if value_type is not None:
            entry['value_type'] = value_type

    def _modify_scp(self, Mastery_index, Overloadmastery_lv, usepoint=None, forcecode_num=None ,forcecode_value=None, value_type=None):
        for entry in self._scp_data.get_section('Overloadmastery_Value'):
            if entry['Mastery_index'] == Mastery_index and entry['Overloadmastery_lv'] == Overloadmastery_lv:
                self._modify_entry(entry, False, usepoint, forcecode_num, forcecode_value, value_type)

    def _modify_dec(self, Mastery_index, Overloadmastery_lv, usepoint=None, forcecode_num=None ,forcecode_value=None, value_type=None):
        Mastery_index      = str(Mastery_index)
        Overloadmastery_lv = str(Overloadmastery_lv)
        usepoint           = str(usepoint) if usepoint else None
        forcecode_num      = str(forcecode_num) if forcecode_num else None
        forcecode_value    = str(forcecode_value) if forcecode_value else None
        value_type         = str(value_type) if value_type else None

        for entry in self._dec_data['children'][3]['children']:
            mastery_id = entry['attributes']['index']
            if mastery_id == Mastery_index:
                for entry2 in entry['children']:                
                    atr = entry2['attributes']
                    if atr['overloadmastery_lv'] == Overloadmastery_lv:
                        self._modify_entry(entry2, True, usepoint, forcecode_num, forcecode_value, value_type)
                        

    def modify_stat(self, Mastery_index, Overloadmastery_lv, usepoint=None, forcecode_num=None ,forcecode_value=None, value_type=None, save_files=True, do_reinit=True):
        if all(x == None for x in (usepoint, forcecode_num, forcecode_value, value_type)):
            return
        
        self._modify_scp(Mastery_index, Overloadmastery_lv, usepoint, forcecode_num ,forcecode_value, value_type)
        self._modify_dec(Mastery_index, Overloadmastery_lv, usepoint, forcecode_num ,forcecode_value, value_type)

        if save_files:
            self.save()
        if do_reinit:
            self.reinit()
