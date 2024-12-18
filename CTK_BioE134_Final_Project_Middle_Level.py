from CTK_BioE134_Final_Project_Bottom_Level import design_grna_general, CRISPR_TOOLKITS
from CTK_BioE134_Final_Project_Bottom_Level import CRISPRToolkit, design_grna_general

class gRNADesigner:
    @staticmethod
    def design_gRNA(target_sequence, toolkit):
        """
        Designs a guide RNA (gRNA) sequence using a selected CRISPR toolkit object.
        
        Parameters:
            target_sequence (str): The DNA sequence to be targeted. Must include a valid PAM sequence.
            toolkit (CRISPRToolkit): The selected CRISPR toolkit object containing PAM details, protospacer length, and scaffold.

        Returns:
            str: The complete designed gRNA sequence.
        """
        # Ensure toolkit is a CRISPRToolkit object
        if not isinstance(toolkit, CRISPRToolkit):
            raise ValueError("Invalid toolkit object provided. Must be an instance of CRISPRToolkit.")
        
        # Use the name of the toolkit and delegate to the bottom level function
        return design_grna_general(target_sequence, toolkit.name)

if __name__ == "__main__":
    from CTK_BioE134_Final_Project_Bottom_Level import CRISPRToolkit

    target_sequence = "TTTTTTTTTTTTTTTTTTTTNGGATGCGTAGCTGATGCGTAGGTTT"

    # Properly instantiate a CRISPRToolkit object
    toolkit = CRISPRToolkit(name="SpCas9 Toolkit")

    try:
        gRNA = gRNADesigner.design_gRNA(target_sequence, toolkit)
        print(f"Designed gRNA: {gRNA}")
    except ValueError as e:
        print(f"Error: {str(e)}")

