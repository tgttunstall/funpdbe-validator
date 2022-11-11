#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 11:18:52 2022

@author: tanu
"""
from validator.validator import Validator
from validator.residue_index import ResidueIndexes

#validator = Validator("ProKinO") # Same as in the JSON
validator = Validator("FoldX") # Same as in the JSON
validator.load_schema()
print("Schema loaded successfully")

validator.load_json("tt_3pl1_example.json")
#print("Loaded json file successfully")

if validator.basic_checks() and validator.validate_against_schema():
    # Passed data validations
    print('Passed schema validation')
    residue_indexes = ResidueIndexes(validator.json_data)
    if residue_indexes.check_every_residue():
        # Passed the index validation
        print('Passed index validation')
else:
    print('Failed schema validation')
    print(validator.error_log)
