from collections import defaultdict

from ..FileHandling.SCPData import SCPData


class GradeChanceChanger:
    def __init__(self):
        pass

    @staticmethod
    def _build_chance_sum_per_group(scp_data: SCPData):
        total_chances = defaultdict(float)
        for entry in scp_data.get_section('Stellar_Grade'):
            total_chances[entry['G_Id']] += entry['G_Per']

        return total_chances
    
    @staticmethod
    def normalize(scp_data: SCPData):
        total_chances = GradeChanceChanger._build_chance_sum_per_group(scp_data)
        for entry in scp_data.get_section('Stellar_Grade'):
            entry['G_Per'] *= (100 / total_chances[entry['G_Id']])

    @staticmethod
    def modify(scp_data: SCPData, upgrade_code, target_grade, chance, normalize=False): #G_Id	Grade	G_Per --> 101	1	38.000000
        for entry in scp_data.get_section('Stellar_Grade'):
            if entry['G_Id'] == upgrade_code and entry['Grade'] == target_grade:
                entry['G_Per'] = chance
                break 

        total_chances = GradeChanceChanger._build_chance_sum_per_group(scp_data)
        for k, v in total_chances.items():
            if v > 100:
                print(f"WARN: Total percentages exceed 100 % in {k} group. Consider normalization.")

        if normalize:
            GradeChanceChanger.normalize(scp_data)