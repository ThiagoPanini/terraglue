"""Helps users to generate their own sample Spark DataFrames.

This Python file enables users to call functions specially created to make
the process of generating Spark DataFrames easier. It uses a user defined
Python dictionary SAMPLES_DICT on samples.data Python file to iterate over
all information set in order to create a dictionary of Spark DataFrames
objects based on user samples.

___
"""

# Importing libraries
from samples.data import SAMPLES_DICT
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField


# Creating or getting a SparkSession object
spark = SparkSession.builder.getOrCreate()


# Defining a function to generate mocked DataFrames based on an info dict
def generate_samples_dataframes(
    spark: SparkSession = spark,
    samples_dict: dict = SAMPLES_DICT
) -> dict:
    """Creates a Spark DataFrame based on a predefined dictionary

    This function uses a user defined Python dictionary with all information
    needed to create a Spark DataFrame to be used as a fixture in the conftest
    file. The main goal is to enable users to use sample DataFrames to build
    custom unit tests.

    Examples:
        ```python
        # Generating a sample DataFrame
        df_sample = generate_samples_dataframes(samples_dict=SAMPLES_DICT)
        ```
    """

    # Creating a Python dictionary to store the samples DataFrame
    samples_dfs_dict = {}

    # Iterating over all tables sampled in samples_dict dictionary
    for tbl_name, tbl_info in samples_dict.items():
        # Extracing the schema in a way that is readable for Spark
        sample_schema = StructType([
            StructField(col, dtype(), nullable=True)
            for col, dtype in tbl_info["schema"].items()
        ])

        # Extracting sample data content for the table
        sample_data = tbl_info["data"]

        # Creating a Spark DataFrame with sample data
        df_sample = spark.createDataFrame(
            data=sample_data,
            schema=sample_schema
        )

        # Including the sample DataFrame on the final dictionary
        samples_dfs_dict[tbl_name] = df_sample

    return samples_dfs_dict
