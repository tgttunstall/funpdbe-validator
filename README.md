FunPDBe JSON Validator
======================

[![Build Status](https://travis-ci.org/funpdbe-consortium/funpdbe-validator.svg?branch=master)](https://travis-ci.org/funpdbe-consortium/funpdbe-client)
[![codecov](https://codecov.io/gh/funpdbe-consortium/funpdbe-validator/branch/master/graph/badge.svg)](https://codecov.io/gh/funpdbe-consortium/funpdbe-client)
[![Maintainability](https://api.codeclimate.com/v1/badges/7b7786745ea63451187e/maintainability)](https://codeclimate.com/github/funpdbe-consortium/funpdbe-validator/maintainability)

This Python3 client can be used for validating FunPDBe JSON files. It performs various sanity checks, and validates user JSONs against the FunPDBe schema.

For more information on the FunPDBe initiative, visit https://funpdbe.org

Quick start
-----------

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Please note that the client is written in Python3, and the dependencies have to be installed accordingly (i.e. using pip3)!

### Installing

#### Checking out this repository

```
$ git clone https://github.com/funpdbe-consortium/funpdbe-validator
$ cd funpdbe-validator
$ pip3 install -r requirements.txt
```

## Running the tests

Running tests for the client is performed simply by using
```
$ pytest tests
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/funpdbe-consortium/funpdbe-client/tags).

## Authors

* **Mihaly Varadi** - *Initial work* - [mvaradi](https://github.com/mvaradi)

See also the list of [contributors](https://github.com/funpdbe-consortium/funpdbe-validator/graphs/contributors) who participated in this project.

## License

This project is licensed under the EMBL-EBI License - see the [LICENSE](LICENSE) file for details