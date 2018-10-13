import json
import requests


class CheckResidueIndices(object):
    """
    This class has all the methods required for validating the
    residue indices that are in the user submitted data.
    Each residue has an index number in the submitted JSON,
    and each has to match the indices in the official PDB entry
    This class relies on the PDBe API to get the current residue
    indices
    """

    def __init__(self, data):
        self.api_url = "https://www.ebi.ac.uk/pdbe/api/pdb/entry/residue_listing/"
        self.data = data
        self.pdb_id = self.set_pdb_id()
        self.mismatches = []
        self.labels = ["residues", "chains", "molecules"]

    def set_pdb_id(self):
        """
        Sets the PDB id based on the JSON data
        :return: String, PDB id or None
        """
        if "pdb_id" in self.data.keys():
            return self.data["pdb_id"].lower()
        return None

    def loop_chains(self):
        """
        Looping through all the chains that are present
        in the JSON data
        :return: True if the residue numbering is valid, False if not
        """
        if not self.pdb_id:
            return False
        for chain_data in self.data["chains"]:
            if not self.get_residue_numbering(chain_data):
                return False
        return True

    def get_residue_numbering(self, chain_data):
        """
        Gets the residue numbering from the PDBe API and
        checks all residues
        :param chain_data: JSON sub-data
        :return: True if residue numbering is valid, False if not
        """
        chain_id = chain_data["chain_label"]
        url = "%s%s/chain/%s" % (self.api_url, self.pdb_id, chain_id)
        response = requests.get(url)
        residue_numbering = json.loads(response.text)
        if not residue_numbering.keys():
            self.mismatches.append("No residues in PDB for this entry - probably obsoleted entry")
            return False
        return self.check_numbering(residue_numbering, chain_data)

    def check_numbering(self, residue_numbering, chain_data):
        """
        This method loops through all the residues in a chain
        and call the residue index comparator method
        :param residue_numbering: JSON data from PDBe API
        :param chain_data: JSON data from user
        :return: True is residue numbering is valid, False if not
        """
        if not "residues" in chain_data.keys():
            return False
        for residue in chain_data["residues"]:
            depositor_residue_number = residue["pdb_res_label"]
            depositor_aa_type = residue["aa_type"]
            if not self.compare_residue_number(depositor_residue_number, depositor_aa_type, residue_numbering):
                return False
        return True

    def compare_residue_number(self, depositor_residue_number, depositor_aa_type, residue_numbering):
        """
        This method starts looping through the substructure of the PDBe API data
        :param depositor_residue_number: Residue number provided by the user
        :param depositor_aa_type: Residue amino acid code provided by user
        :param residue_numbering: Residue numbering provided by PDBe API
        :return: True is residue numbering is valid, False if not
        """
        molecules = residue_numbering[self.pdb_id]["molecules"]
        return self.recursive_loop(molecules, "chains", depositor_residue_number, depositor_aa_type)

    def recursive_loop(self, data, label, depositor_residue_number, depositor_aa_type):
        """
        A recursive loop that goes down to residue level and processes all residues
        :param data: JSON data
        :param label: String, "chains" or "residues" depending on the level
        :param depositor_residue_number: Residue number provided by the user
        :param depositor_aa_type: Residue amino acid code provided by user
        :return: True is residue numbering is valid, False if not
        """
        for item in data:
            sub_data = item[label]
            if label == "chains":
                return self.recursive_loop(sub_data, "residues", depositor_residue_number, depositor_aa_type)
            elif label == "residues":
                return self.process_residues(sub_data, depositor_residue_number, depositor_aa_type)
            return False

    def process_residues(self, residues, depositor_residue_number, depositor_aa_type):
        """
        This method grabs the residue information and call the comparator if the
        residue number of PDBe is the same as the user input
        :param residues: Residue data from PDBe API
        :param depositor_residue_number: Residue number provided by the user
        :param depositor_aa_type: Residue amino acid code provided by user
        :return: True is residue numbering is valid, False if not
        """
        for residue in residues:
            if "%i%s" % (residue["author_residue_number"], residue["author_insertion_code"]) == depositor_residue_number:
                return self.make_comparison(residue["residue_name"], depositor_aa_type, depositor_residue_number)
        self.mismatches.append("residue numbering is completely mismatched between data and PDB entry")
        return False

    def make_comparison(self, residue_name, depositor_aa_type, depositor_residue_number):
        """
        This method does the comparison between two residues that have the same index number
        The comparison is between amino acid code
        :param residue_name: Residue amino acid code provided by PDBe API
        :param depositor_aa_type: Residue amino acid code provided by user
        :param depositor_residue_number: Residue number provided by the user
        :return: True is residue numbering is valid, False if not
        """
        if residue_name == depositor_aa_type:
            return True
        mismatch = "residue %s (%s) in data does not match residue %s (%s) in PDB" % (
            depositor_residue_number, depositor_aa_type, depositor_residue_number, residue_name)
        self.mismatches.append(mismatch)
        return False