from compendium.types.medication import Medication
from pathlib import Path
from typing import List


file_path = Path("data/compendium.txt")
section_markers = {
    "name": ("Fachinformation", "Zusammensetzung"),
    "composition": ("Zusammensetzung", "Wirkstoffmenge pro Einheit"),
    "dosage_form": ("Wirkstoffmenge pro Einheit", "Indikationen/Anwendungsmöglichkeiten"),
    "indications": ("Indikationen/Anwendungsmöglichkeiten", "Dosierung/Anwendung"),
    "dosage": ("Dosierung/Anwendung", "Kontraindikationen"),
    "contraindications": ("Kontraindikationen", "Warnhinweise und Vorsichtsmassnahmen"),
    "warnings_and_precautions": ("Warnhinweise und Vorsichtsmassnahmen", "Interaktionen"),
    "interactions": ("Interaktionen", "Schwangerschaft/Stillzeit"),
    "pregnancy_lactation_period": ("Schwangerschaft/Stillzeit", "Wirkung auf die Fahrtüchtigkeit und auf das Bedienen von Maschinen"),
    "effects_on_the_ability_to_drive_and_operate_machinery": ("Wirkung auf die Fahrtüchtigkeit und auf das Bedienen von Maschinen", "Unerwünschte Wirkungen"),
    "undesirable_effects": ("Unerwünschte Wirkungen", "Überdosierung"),
    "overdose": ("Überdosierung", "Eigenschaften/Wirkungen"),
    "properties_effects": ("Eigenschaften/Wirkungen", "Pharmakokinetik"),
    "pharmacokinetics": ("Pharmakokinetik", "Präklinische Daten"),
    "preclinical_data": ("Präklinische Daten", "Sonstige Hinweise"),
    "other_information": ("Sonstige Hinweise", "")
}

def split_medication_texts():
    content = file_path.read_text(encoding='utf-8')
    medication_texts = content.split("\n")
    return medication_texts

def parse_medications(medication_texts: List[str]) -> List[Medication]:
    medications: List[Medication] = []
    for med_text in medication_texts:
        start_header = "Normal Drucken"
        end_header = "Sonstige Hinweise"
        start_index = med_text.find(start_header)
        end_index = med_text.find(end_header) + len(end_header) if end_header in med_text else 0
        if start_index != -1 and end_index != -1:
            med_text = med_text[end_index:].strip()
        medication = Medication()
        for attr, (start_marker, end_marker) in section_markers.items():
            start_index = med_text.find(start_marker)
            end_index = med_text.find(end_marker) if end_marker else len(med_text)
            if start_index != -1:
                section_text = med_text[start_index + len(start_marker):end_index].strip()
                if attr == "composition":
                    section_text = section_text.rstrip("Galenische Form und")
                    section_text = section_text.rstrip("Darreichungsform und")
                setattr(medication, attr, section_text)
        medications.append(medication)
    return medications

def get_medications():
    medication_texts = split_medication_texts()
    medications = parse_medications(medication_texts)
    return medications
