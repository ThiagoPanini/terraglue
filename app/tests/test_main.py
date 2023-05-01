"""Test cases for the Spark application on main.py script.

This file handles all unit tests of features from the main application script
built to be deployed as a Spark application and ran as a Glue job in AWS. The
test cases are based on important elements that should be checked and verified
in order to ensure the application are working properly.

___
"""

# Importing libraries
import pytest

# from src.main import ARGV_LIST


@pytest.mark.main
@pytest.mark.skip(reason="Work in progress")
def test_user_defind_argv_list_variable_is_a_python_list():
    """
    G:
    W:
    T:
    """
    ...
    # assert type(ARGV_LIST) is list
