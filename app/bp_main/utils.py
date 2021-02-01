import pandas as pd


def check_tool_compability(feature_list, technology_list):
    """
    @Params: feature_list ist eine Liste oder json von allen Featuren.
    @Params: technology_list ist eine Liste mit allen Technologien,
        die nach Technologiereihenfolge sortiert worden ist.

    Funktionsablauf:
    1. Gehe durch jedes Feature
    2. Durchlaufe jede Technologie
    3. Ueberpruefe ob die Technologie das Feature bearbeiten kann
    4. Ueberpruefe ob die Technologie die Nebenbedingungen erfuellt
        4.1. Zwischen b - c // Flag = safe
        4.2. Zwischen a - b oder c - d // Flag = unsafe
    5. Wenn keine Flag dann naechste Technlogie
    6. Wenn alle Technologien durch und keine Flag // Flag = error 
    """

    for feature in feature_list:
        for technology in technology_list:
            if technology['possible_features'] not in feature['Classifier']:
                break
