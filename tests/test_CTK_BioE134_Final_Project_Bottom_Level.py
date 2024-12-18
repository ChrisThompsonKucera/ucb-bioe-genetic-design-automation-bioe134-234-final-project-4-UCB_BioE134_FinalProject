import pytest
import sys
import os

# Add project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from CTK_BioE134_Final_Project_Bottom_Level import design_grna_general, CRISPRToolkit


def test_design_grna_general():
    target_sequence = "TTTTTTTTTTTTTTTTTTTTNGG"  # At least 23 bp
    toolkit = "SpCas9 Toolkit"
    expected_output = "TTTTTTTTTTTTTTTTTTTT"  # Example expected gRNA sequence

    result = design_grna_general(target_sequence, toolkit)
    assert expected_output in result, "gRNA design failed for SpCas9 Toolkit"

def test_invalid_toolkit():
    target_sequence = "TTTTTTTTTTTTTTTTTTTTNGG"  # At least 23 bp
    with pytest.raises(ValueError):
        design_grna_general(target_sequence, "Invalid Toolkit")