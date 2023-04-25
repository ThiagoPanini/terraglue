"""Test cases for aux functions created to help users generating sample dfs

This file handles all unit tests to check if the auxiliar code and functions
created to help users to generate their own sample Spark DataFrames are
working properly.

___
"""

# Importing libraries
import pytest

from samples.data import SAMPLES_DICT

from pyspark.sql import DataFrame


@pytest.mark.dataframes
def test_function_to_get_dataframe_samples_generates_a_python_dictionary(
    samples_dfs_dict
):
    """
    G: given that users want to generate their own DataFrames samples to test
    W: when the function generate_samples_dataframes() is executed
    T: then the returned object must be a Python dictionary
    """
    assert type(samples_dfs_dict) is dict


@pytest.mark.dataframes
def test_table_keys_defined_by_user_are_contained_on_samples_dfs_dictionary(
    samples_dfs_dict
):
    """
    G: given that users want to generate their own DataFrames samples to test
    W: when the function generate_samples_dataframes() is executed
    T: then the keys defined by user on SAMPLES_DICT dictionary on samples.data
       module must be contained on samples_dfs_dict
    """
    assert all(c in list(samples_dfs_dict.keys()) for c in list(SAMPLES_DICT))


@pytest.mark.dataframes
def test_all_elements_on_samples_dfs_dictionary_are_spark_dataframes(
    samples_dfs_dict
):
    """
    G: given that users want to generate their own DataFrames samples to test
    W: when the function generate_samples_dataframes() is executed
    T: then all elements in samples_dfs_dict must be Spark DataFrames
    """

    # Extracting types of samples in samples dictionary
    samples_types = [type(sample) for sample in samples_dfs_dict.values()]

    # Checks if there is only one distinct type and if it's a Spark DataFrame
    assert len(set(samples_types)) == 1
    assert list(set(samples_types))[0] == DataFrame
