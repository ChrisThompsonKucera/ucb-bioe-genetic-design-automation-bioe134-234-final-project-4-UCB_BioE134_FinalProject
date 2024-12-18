# Import required modules
import sys
import os

# Ensure the current directory is in sys.path for imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

# Import dependencies from Middle and Bottom Levels
from CTK_BioE134_Final_Project_Bottom_Level import CRISPRToolkit
from CTK_BioE134_Final_Project_Middle_Level import gRNADesigner


# Updated ToolkitSelector class with improved select_toolkit method
class ToolkitSelector:
    def __init__(self, toolkits):
        self.toolkits = toolkits  # Dictionary of available toolkits and their properties

    def select_toolkit(self, plant_name, target_sequence):
        """
        Selects the most suitable CRISPR toolkit based on plant compatibility and PAM presence.
        """
        for toolkit_name, data in self.toolkits.items():
            if plant_name in data["plants"]:  # Check if the plant is supported
                if data["pam"] in target_sequence:  # Check if PAM is present in the target sequence
                    return CRISPRToolkit(name=toolkit_name)  # Only pass the name of the toolkit
        raise ValueError(f"No suitable toolkit found for plant '{plant_name}' with the given target sequence.")

# Class for generating the construction file
class ConstructionFileCreator:
    def __init__(self, plant_name, target_sequence):
        self.plant_name = plant_name
        self.target_sequence = target_sequence

    def generate_construction_file(self, toolkit, gRNA):
        """
        Produces a construction file in CF Shorthand format with descriptive gRNA primer names.
        """
        # Generate meaningful primer names using plant name and toolkit
        primer_prefix = f"{self.plant_name}_{toolkit.name.replace(' ', '_')}"

        steps = [
            f"pcr {primer_prefix}_gRNA_forward {primer_prefix}_gRNA_reverse {toolkit.name}_template {primer_prefix}_gRNA_pcr",
            f"digest {primer_prefix}_gRNA_pcr {toolkit.pam} 1 {primer_prefix}_gRNA_digested",
            f"ligate {primer_prefix}_gRNA_digested {primer_prefix}_gRNA_ligated",
            f"transform {primer_prefix}_gRNA_ligated {self.plant_name} Spec {toolkit.name}_edited"
        ]

        return "\n".join(steps)

# Example toolkits data
toolkits_data = {
    "SpCas9 Toolkit": {"plants": ["Arabidopsis", "Rice", "Maize"], "pam": "NGG"},
    "FnCas12a Toolkit": {"plants": ["Arabidopsis", "Wheat", "Tomato"], "pam": "TTTV"},
    "SaCas9 Toolkit": {"plants": ["Rice", "Maize", "Barley"], "pam": "NNGRRT"},
}

# Example usage
if __name__ == "__main__":
    # Define inputs
    plant_name = "Arabidopsis"
    # Corrected and extended target sequence
    target_sequence = "TTTTTTTTTTTTTTTTTTTTNGGATGCGTAGCTGATGCGTAGGTTTAGCGTNGGTAGCTTTTTTTTTTGGGGTTAGCGTAGCTG"

    try:
        # Check sequence length
        if len(target_sequence) < 23:
            raise ValueError("Target sequence is too short. Please provide a sequence of at least 23 bp.")

        # Initialize the ToolkitSelector and select a toolkit
        toolkit_selector = ToolkitSelector(toolkits=toolkits_data)
        selected_toolkit = toolkit_selector.select_toolkit(plant_name, target_sequence)

        # Design the gRNA
        grna_designer = gRNADesigner()
        gRNA = grna_designer.design_gRNA(target_sequence, selected_toolkit)

        # Generate the construction file in CF Shorthand format
        file_creator = ConstructionFileCreator(plant_name, target_sequence)
        construction_file = file_creator.generate_construction_file(selected_toolkit, gRNA)

        # Print the construction file
        print(construction_file)

    except ValueError as e:
        # Handle errors and display meaningful messages
        print(f"Error: {str(e)}")
