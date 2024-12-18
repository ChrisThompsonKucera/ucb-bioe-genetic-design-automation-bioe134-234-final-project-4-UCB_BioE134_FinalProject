import pytest
import sys
import os

# Add project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from CTK_BioE134_Final_Project_Bottom_Level import design_grna_general, CRISPRToolkit

from CTK_BioE134_Final_Project_High_Level import ToolkitSelector, ConstructionFileCreator
from CTK_BioE134_Final_Project_Bottom_Level import CRISPRToolkit

def test_toolkit_selection():
    toolkits = {
        "SpCas9 Toolkit": {"plants": ["Arabidopsis"], "pam": "NGG"}
    }
    selector = ToolkitSelector(toolkits)
    toolkit = selector.select_toolkit("Arabidopsis", "TTTTTTNGGATGCGT")
    assert toolkit.name == "SpCas9 Toolkit", "Failed to select correct toolkit"

def test_generate_construction_file():
    plant_name = "Arabidopsis"
    target_sequence = "TTTTTTTTTTTNGGATGCGT"
    toolkit = CRISPRToolkit(name="SpCas9 Toolkit")
    gRNA = "GCGTNGGATGCGT"

    creator = ConstructionFileCreator(plant_name, target_sequence)
    result = creator.generate_construction_file(toolkit, gRNA)
    assert "pcr" in result, "PCR step missing in construction file"
    assert "digest" in result, "Digest step missing in construction file"
