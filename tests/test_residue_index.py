#!/usr/bin/env python3

"""
Copyright 2018 EMBL - European Bioinformatics Institute

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific
language governing permissions and limitations under the
License.
"""

import json
from unittest import TestCase

from validator.residue_index import CheckResidueIndices

with open("data/test_data.json", "r") as mock_data_file:
    mock_data = json.load(mock_data_file)

mock_data_no_pdb_id = {"foo": "bar"}

mock_data_bad_numbering = {"pdb_id": "2aqa",
                           "chains": [{"chain_label": "A",
                                       "residues": [{"pdb_res_label": "2",
                                                     "aa_type": "ALA"}]}]}


def mock_get_residue_numbering_false(self):
    return False


def mock_get_residue_numbering_true(self):
    return True


def mock_compare_residue_number(self, foo, bar):
    return False


class TestCheckResidueIndices(TestCase):

    def setUp(self):
        self.cri = CheckResidueIndices(mock_data)

    def test_loop_chains(self):
        self.cri.get_residue_numbering = mock_get_residue_numbering_false
        result = self.cri.loop_chains()
        self.assertFalse(result)
        self.cri.get_residue_numbering = mock_get_residue_numbering_true
        result = self.cri.loop_chains()
        self.assertTrue(result)
        self.cri.pdb_id = None
        self.assertFalse(self.cri.loop_chains())

    def test_set_pdb_id(self):
        self.assertIsNotNone(self.cri.set_pdb_id())
        bad_cri = CheckResidueIndices(mock_data_no_pdb_id)
        self.assertIsNone(bad_cri.set_pdb_id())

    def test_check_numbering(self):
        result = self.cri.check_numbering({}, {})
        self.assertFalse(result)
        self.cri.compare_residue_number = mock_compare_residue_number
        result = self.cri.check_numbering({}, {"residues": [{"pdb_res_label": 0, "aa_type": "ALA"}]})
        self.assertFalse(result)

    def test_get_residue_numbering(self):
        mock_data = {"chain_label": "A"}
        self.cri.pdb_id = "1CBS"
        self.cri.check_numbering = lambda x, y : True
        result = self.cri.get_residue_numbering(mock_data)
        self.assertTrue(result)
        self.cri.pdb_id = "2H58"
        result = self.cri.get_residue_numbering(mock_data)
        self.assertFalse(result)

    def test_recursive_loop(self):
        result = self.cri.recursive_loop([{"foo": "bar"}], "foo", None, None)
        self.assertFalse(result)

    def test_with_bad_numbering(self):
        cri_with_bad_numbering = CheckResidueIndices(mock_data_bad_numbering)
        result = cri_with_bad_numbering.loop_chains()
        self.assertFalse(result)

    def test_process_residues(self):
        result = self.cri.process_residues(
            [{"author_residue_number": 1, "residue_name": "ALA", "author_insertion_code": ""}], "1", "ALA")
        self.assertTrue(result)
        result = self.cri.process_residues(
            [{"author_residue_number": 1, "residue_name": "ALA", "author_insertion_code": "C"}], "1C", "ALA")
        self.assertTrue(result)
        result = self.cri.process_residues(
            [{"author_residue_number": 2, "residue_name": "ALA", "author_insertion_code": ""}], "1", "ALA")
        self.assertFalse(result)
        result = self.cri.process_residues(
            [{"author_residue_number": 1, "residue_name": "ALA", "author_insertion_code": ""}], "1", "HIS")
        self.assertFalse(result)