from collections import defaultdict

from ..FileHandling.SCPData import SCPData


class StatsValuesChanger:
    def __init__(self):
        pass

    @staticmethod
    def delete_stat(scp_data:SCPData, V_val):
        rows_to_drop = []
        for entry in scp_data.get_section('Stellar_Forcecode'):     # F_Id	Force_Code	Value_Type	F_Per	Value	
            if entry['Value'] == V_val:
                rows_to_drop.append(entry['RowIndex'])
                break
        
        for entry in scp_data.get_section('Stellar_Value'):         # V_Id	V_Order	Value	Value_type	V_Per
            if entry['V_Id'] == V_val:
                rows_to_drop.append(entry['RowIndex'])

        for it, row_idx in enumerate(rows_to_drop):
            section = 'Stellar_Forcecode' if it == 0 else 'Stellar_Value'
            scp_data.remove_entry(section, row_idx)

        scp_data.rebuild_rowindex('Stellar_Forcecode')
        scp_data.rebuild_rowindex('Stellar_Value')

    @staticmethod
    def delete_stat_grade(scp_data: SCPData, V_Id, V_Order):        #V_Id	V_Order	Value	Value_type	V_Per
        for entry in scp_data.get_section('Stellar_Value'): 
            if entry['V_Id'] == V_Id and entry['V_Order'] == V_Order:
                entry['V_Per'] = 0

    @staticmethod
    def normalize(scp_data: SCPData):
        config = {
            'Stellar_Forcecode' : {
                'KeyColumn' : 'F_Id',
                'ValColumn' : 'F_Per',
            },
            'Stellar_Value' : {
                'KeyColumn' : 'V_Id',
                'ValColumn' : 'V_Per',
            }
        }
        percentage_sums = defaultdict(lambda: defaultdict(float))
        for k, v in config.items():
            for entry in scp_data.get_section(k):
                percentage_sums[k][entry[v['KeyColumn']]] += entry[v['ValColumn']]

        for k, v in config.items():
            for entry in scp_data.get_section(k):
                entry[v['ValColumn']] *= (100 / percentage_sums[k][entry[v['KeyColumn']]])

    @staticmethod
    def set_stat_percentage(scp_data: SCPData, Value_Key, new_percentage):        # F_Id	Force_Code	Value_Type	F_Per	Value
        for entry in scp_data.get_section('Stellar_Forcecode'):
            if entry['Value'] == Value_Key:
                entry['F_Per'] = new_percentage

    @staticmethod
    def set_stat_value(scp_data: SCPData, V_Id, V_Order, new_value):
        for entry in scp_data.get_section('Stellar_Value'):
            if entry['V_Id'] == V_Id and entry['V_Order'] == V_Order:
                entry['Value'] = new_value
                break