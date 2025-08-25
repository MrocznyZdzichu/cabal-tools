from ..FileHandling.SCPData import SCPData

class SetBonusChanger:
    def __init__(self):
        pass

    @staticmethod
    def _get_grade(Line_No):
        return 2*Line_No + 2
    
    @staticmethod
    def _modify_scp(scp_data:SCPData, Line_No, Grade, Force_Code1=None, Value1=None, Value_Type1=None, Force_Code2=None, Value2=None, Value_Type2=None):
        changes = {
            'Force_Code1' : Force_Code1,
            'Value1'      : Value1,
            'Value_Type1' : Value_Type1,
            'Force_Code2' : Force_Code2,
            'Value2'      : Value2,
            'Value_Type2' : Value_Type2,
        }
        entries = scp_data.get_section('Set_Ability')
        for entry in entries:
            if entry['Line_No'] == Line_No and entry['Grade'] == Grade:
                for k, v in changes.items():
                    if v:
                        entry[k] = v
                return

    @staticmethod
    def _modify_dec(dec_data: dict, Line_No, Grade, Force_Code1=None, Value1=None, Value_Type1=None, Force_Code2=None, Value2=None, Value_Type2=None):
        changes = {
            'force_code1' : str(Force_Code1) if Force_Code1 else None,
            'Value1'      : str(Value1)      if Value1      else None,
            'value_type1' : str(Value_Type1) if Value_Type1 else None,
            'force_code2' : str(Force_Code2) if Force_Code2 else None,
            'Value2'      : str(Value2)      if Value2      else None,      
            'value_type2' : str(Value_Type2) if Value_Type2 else None
        }
        for section in dec_data['children'][1]['children']:
            for line in section['children']:
                line_no = line['attributes']['line_no']
                if line_no == str(Line_No):
                    for line_details in line['children']:
                        grade = line_details['attributes']['grade']
                        if grade == str(Grade):
                            atr = line_details['attributes']
                            for k, v in changes.items():
                                if v:
                                    atr[k] = v
                            return

    @staticmethod
    def modify_set_bonus(
        scp_data,
        dec_data,
        Line_No,
        Grade,
        Force_Code1=None,
        Value1=None,
        Value_Type1=None,
        Force_Code2=None,
        Value2=None,
        Value_Type2=None,
    ):
        SetBonusChanger._modify_scp(
            scp_data,
            Line_No,
            Grade,
            Force_Code1,
            Value1,
            Value_Type1,
            Force_Code2,
            Value2,
            Value_Type2,
        )

        SetBonusChanger._modify_dec(
            dec_data,
            Line_No, 
            Grade, 
            Force_Code1=Force_Code1, 
            Value1=Value1, 
            Value_Type1=Value_Type1, 
            Force_Code2=Force_Code2, 
            Value2=Value2, 
            Value_Type2=Value_Type2
        )