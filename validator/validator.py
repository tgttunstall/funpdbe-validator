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

import jsonschema
import json
import re


class Validator(object):
    """
    Validates FunPDBe JSON files
    """

    def __init__(self, resource):
        self.resource = resource
        self.schema = None
        self.json_data = None
        self.error_log = None

    def load_json(self, path_to_file):
        self.json_data = self.parse_json(path_to_file)

    def load_schema(self, path_to_schema):
        self.schema = self.parse_json(path_to_schema)

    def parse_json(self, path):
        """
        Parses a FunPDBe JSON file and in case of file error
        or JSON error, the error message is saved to self.error_log

        :return: Bool, True is parsed, False if failed
        """
        try:
            with open(path, "r") as json_file:
                try:
                    return json.load(json_file)
                except json.decoder.JSONDecodeError as err:
                    self.error_log = "JSON error: %s" % err
                    return None
        except IOError as ioerr:
            self.error_log = "File error: %s" % ioerr
            return None

    def basic_checks(self):
        if self.test_resource() and self.test_pdb_id():
            return True
        return False

    def test_resource(self):
        if "data_resource" not in self.json_data.keys():
            self.error_log = "No data resource name found"
            return False
        elif self.json_data["data_resource"] != self.resource:
            self.error_log = "Data resource name mismatch"
            return False
        return True

    def test_pdb_id(self):
        if "pdb_id" not in self.json_data.keys():
            self.error_log = "No PDB id found"
            return False
        elif not re.match("^[1-9][a-zA-Z0-9]{3}$", self.json_data["pdb_id"]):
            self.error_log = "Invalid PDB id found"
            return False
        return True

    def validate_against_schema(self):
        try:
            jsonschema.validate(self.json_data, self.schema)
            return True
        except jsonschema.exceptions.ValidationError as err:
            self.error_log = "JSON does not comply with schema: %s" % err
            return False



# TODO - Add the file path to the error log, if not empty
# jsonschema.validate(json_data, self.json_schema)