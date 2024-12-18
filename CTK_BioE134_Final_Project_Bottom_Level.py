from Bio.Seq import Seq

# Define CRISPR toolkit data
CRISPR_TOOLKITS = {
    "SpCas9 Toolkit": {
        "organisms": ["Arabidopsis", "Rice", "Maize", "Tomato", "Soybean"],
        "cas_system": "SpCas9",
        "pam": "NGG",
        "protospacer_length": 20,
        "scaffold": "GTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGC",
    },
    "FnCas12a Toolkit": {
        "organisms": ["Arabidopsis", "Wheat", "Tomato"],
        "cas_system": "FnCas12a",
        "pam": "TTTV",
        "protospacer_length": 24,
        "scaffold": "TTTAACTTTGCTATTTCTAGCTCTAAAAC",
    },
    "SaCas9 Toolkit": {
        "organisms": ["Rice", "Maize", "Barley"],
        "cas_system": "SaCas9",
        "pam": "NNGRRT",
        "protospacer_length": 20,
        "scaffold": "GTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGC",
    },
}
class CRISPRToolkit:
    """
    Class representing a CRISPR toolkit with its properties.
    """
    def __init__(self, name):
        self.name = name
        self.toolkit_info = CRISPR_TOOLKITS.get(name)
        if not self.toolkit_info:
            raise ValueError(f"Toolkit '{name}' is not defined in CRISPR_TOOLKITS.")
        
        # Automatically extract properties from CRISPR_TOOLKITS
        self.pam = self.toolkit_info["pam"]
        self.protospacer_length = self.toolkit_info["protospacer_length"]
        self.scaffold = self.toolkit_info["scaffold"]

# Function to find PAM in a DNA sequence
def find_pam_general(target_sequence, pam):
    """
    Finds the index of the PAM sequence in the target DNA.
    """
    import re
    pam_regex = pam.replace("N", ".").replace("V", "[ACG]")
    matches = list(re.finditer(pam_regex, target_sequence))
    if matches:
        return matches[0].start()
    return -1

# Function to design gRNA for a given CRISPR toolkit
def design_grna_general(target_sequence, crispr_toolkit_name):
    """
    Designs a guide RNA (gRNA) sequence based on the toolkit's PAM and protospacer requirements.
    
    Parameters:
        target_sequence (str): The DNA sequence to be targeted. Must include a valid PAM sequence.
        crispr_toolkit_name (str): The name of the CRISPR toolkit. 
            Possible values: 'SpCas9 Toolkit', 'FnCas12a Toolkit', 'SaCas9 Toolkit'.

    Returns:
        str: The complete gRNA sequence combining the protospacer and toolkit-specific scaffold.
    """
    toolkit_info = CRISPR_TOOLKITS.get(crispr_toolkit_name)
    if not toolkit_info:
        raise ValueError(f"Unknown CRISPR toolkit: {crispr_toolkit_name}")

    pam = toolkit_info["pam"]
    protospacer_length = toolkit_info["protospacer_length"]
    scaffold = toolkit_info["scaffold"]

    required_length = protospacer_length + len(pam)
    if len(target_sequence) < required_length:
        raise ValueError(f"Target sequence is too short. It must be at least {required_length} bp long.")

    pam_index = find_pam_general(target_sequence, pam)
    if pam_index == -1:
        raise ValueError(f"PAM sequence '{pam}' not found in target sequence: {target_sequence}")

    protospacer_start = pam_index - protospacer_length
    if protospacer_start < 0:
        raise ValueError("Target sequence too short to extract protospacer.")

    protospacer = target_sequence[protospacer_start:pam_index]
    if len(protospacer) != protospacer_length:
        raise ValueError("Protospacer length is incorrect.")

    return protospacer + scaffold

if __name__ == "__main__":
    # Test the bottom level
    target_sequence = "ATGCGTATGCGTAGCTGATGCGTNGGTAGCTTTTV"  # Example target sequence
    crispr_toolkit_name = "SpCas9 Toolkit"
    try:
        # Test design_grna_general
        gRNA = design_grna_general(target_sequence, crispr_toolkit_name)
        print(f"Designed gRNA: {gRNA}")
    except ValueError as e:
        print(f"Error: {str(e)}")
