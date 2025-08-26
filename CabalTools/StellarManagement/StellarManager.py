from ..FileHandling.SCPData import SCPData
from ..ABCBaseManager       import ABCBaseManager, can_reconfig

from .SetBonusChanger    import SetBonusChanger
from .GradeChanceChanger import GradeChanceChanger
from .StatsValuesChanger import StatsValuesChanger


class StellarManager(ABCBaseManager):
    def __init__(self, scp_data:SCPData, dec_data, msg_data, forcecodes: dict):
        self._stats_dict = forcecodes
        super().__init__(
            scp_data,
            dec_data,
            msg_data,
            scp_target_filename="Stellar.scp",
            dec_target_filename="stellar.dec",
        )

    def _enrich_scp(self):
        rich_scp = super()._enrich_scp()

        for section in rich_scp:
            for entry in section['entries']:
                if section['section'] == 'Stellar_Forcecode':
                    entry['Force_Code_Name'] = self._stats_dict.get(entry['Force_Code'])
                if section['section'] == 'Set_Ability':
                    entry['Force_Code_Name1'] = self._stats_dict.get(entry['Force_Code1'])
                    entry['Force_Code_Name2'] = self._stats_dict.get(entry['Force_Code2'])

        return rich_scp

    @can_reconfig
    def modify_set_bonus(
        self,
        Line_No,
        Grade,
        Force_Code1=None,
        Value1=None,
        Value_Type1=None,
        Force_Code2=None,
        Value2=None,
        Value_Type2=None
    ):
        if all(x == None for x in (Force_Code1, Value1, Value_Type1, Force_Code2, Value2, Value_Type2)):
            return
        
        SetBonusChanger.modify_set_bonus(
            self._scp_data, 
            self._dec_data, 
            Line_No, 
            Grade, 
            Force_Code1=Force_Code1, 
            Value1=Value1, 
            Value_Type1=Value_Type1, 
            Force_Code2=Force_Code2, 
            Value2=Value2, 
            Value_Type2=Value_Type2
        )

    @can_reconfig
    def modify_grade_chances(self, upgrade_code, target_grade, chance, normalize=False):
        GradeChanceChanger.modify(self._scp_data, upgrade_code, target_grade, chance, normalize=normalize)

    def normalize_grade_chances(self):
        GradeChanceChanger.normalize(self._scp_data)

    @can_reconfig
    def truncate_force_value(self, V_value):           
        StatsValuesChanger.delete_stat(self._scp_data, V_value)

    @can_reconfig
    def remove_value_grade(self, V_Id, V_Order):   # V_Id	V_Order	Value	Value_type	V_Per
        StatsValuesChanger.delete_stat_grade(self._scp_data, V_Id, V_Order)

    def normalize_stat_chances(self):
        StatsValuesChanger.normalize(self._scp_data)

    @can_reconfig
    def set_stat_percentage(self, Value_Key, new_percentage):
        StatsValuesChanger.set_stat_percentage(self._scp_data, Value_Key, new_percentage)

    @can_reconfig
    def set_stat_value(self, V_Id, V_Order, new_value):
        StatsValuesChanger.set_stat_value(self._scp_data, V_Id, V_Order, new_value)