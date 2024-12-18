import pytest
import sys
import os

# Add project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from CTK_BioE134_Final_Project_Bottom_Level import design_grna_general, CRISPRToolkit

from CTK_BioE134_Final_Project_Middle_Level import gRNADesigner
from CTK_BioE134_Final_Project_Bottom_Level import CRISPRToolkit

def test_grna_designer():
    target_sequence = "TTTTTTTTTTTTTTTTTTTTNGG"  # At least 23 bp
    toolkit = CRISPRToolkit(name="SpCas9 Toolkit")
    expected_output = "TTTTTTTTTTTTTTTTTTTT"

    result = gRNADesigner.design_gRNA(target_sequence, toolkit)
    assert expected_output in result, "gRNA design failed for Middle Level"

def test_grna_invalid_toolkit():
    target_sequence = "TTTTTTTTTTTTTTTTTTTTNGG"  # At least 23 bp
    with pytest.raises(ValueError):
        gRNADesigner.design_gRNA(target_sequence, "Not a Toolkit")