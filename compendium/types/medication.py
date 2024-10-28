from dataclasses import dataclass

@dataclass
class Medication:
    name: str = ""
    composition: str = ""
    dosage_form: str = ""
    indications: str = ""
    dosage: str = ""
    contraindications: str = ""
    warnings_and_precautions: str = ""
    interactions: str = ""
    pregnancy_lactation_period: str = ""
    effects_on_the_ability_to_drive_and_operate_machinery: str = ""
    undesirable_effects: str = ""
    overdose: str = ""
    properties_effects: str = ""
    pharmacokinetics: str = ""
    preclinical_data: str = ""
    other_information: str = ""
