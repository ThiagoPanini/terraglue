"""Helps users to create Spark DataFrames to be used on unit tests.

This Python file handles useful functions that can be used to create Spark
DataFrames based on JSON files containing definitions about source DataFrames
and expected DataFrames from transformation methods.

The JSON files must be configured by users and stored on configs/ folder. This
module then defines functions to read those JSON files and return Spark
DataFrames based on how users configured schema information on the files.

___
"""

# Importing libraries
import json
import os

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType,\
    IntegerType, DecimalType, FloatType, DateType, TimestampType, BooleanType


# Initializing findspark in case of using a Windows platform
if os.name == "nt":
    import findspark
    findspark.init()

# Getting the active SparkSession
spark = SparkSession.builder.getOrCreate()


# Creating a Python dictionary based on the read of a JSON file
def get_json_data_info(json_path: str, json_main_key: str = "source") -> list:
    """Reads a JSON file with predefined data from job data sources.

    This functions receives a path from a JSON file and a main key in order to
    return a Python list object gotten after executing the json.load() method.

    Example:
        ```python
        json_data_info = get_json_data_info(
            json_path="../configs/source_schemas.json",
            json_main_key="source"
        )
        ```

    Args:
        json_path (str):
            The path for the JSON file provided by user with all information
            needed to create Spark DataFrames for all source data for the job

        json_main_key (str):
            The main key of the JSON file according to how the JSON file was
            configured

    Returns:
        A Python list containing all information of data sources put in\
        the JSON file.
    """

    with open(json_path, "r") as f:
        return json.load(f)[json_main_key]


# Parsing a string for a dtype into a valid Spark dtype
def parse_string_to_spark_dtype(dtype: str):
    """Transform a string dtype reference into a valid Spark dtype.

    This function checks for the data type reference for a field given by users
    while filling the JSON schema file in order to return a valid Spark dtype
    based on the string reference.

    Example:
        ```python
        # Returning the Spark reference for a "string" data type
        spark_dtype = parse_string_to_spark_dtype(dtype="string")
        # spark_dtype now holds the StringType Spark dtype object
        ```

    Args:
        dtype (str): A string reference for any parseable Spark dtype

    Returns:
        A callable Spark dtype object based on the string reference provided
    """

    # Removing noise on string before validating
    dtype_prep = dtype.lower().strip()

    # Parsing string reference for dtype to spark data type
    if dtype_prep == "string":
        return StringType
    elif dtype_prep in ("int", "integer"):
        return IntegerType
    elif dtype_prep == "decimal":
        return DecimalType
    elif dtype_prep == "float":
        return FloatType
    elif dtype_prep == "date":
        return DateType
    elif dtype == "timestamp":
        return TimestampType
    elif dtype_prep == "boolean":
        return BooleanType
    else:
        raise TypeError(f"Data type {dtype} is not valid or currently "
                        "parseable into a native Spark dtype")


# Creating a valid Spark DataFrame schema from a list with fields information
def create_spark_schema_from_schema_info(schema_info: list) -> StructType:
    """Generates a StructType Spark schema based on a list of fields info.

    This function receives a preconfigured Python list extracted from a JSON
    schema definition file provided by user in order to return a valid Spark
    schema composed by a StructType structure with multiple StructField objects
    containing informations about name, data type and nullable info about
    attributes.

    Example:
        ```python
        # Showing an example of a input schema list
        schema_list = [
            {
                "attribute": "idx",
                "dtype": "int",
                "nullable": true
            },
            {
                "attribute": "order_id",
                "dtype": "string",
                "nullable": true
            }
        ]

        # Returning a valid Spark schema object based on a dictionary
        schema = create_spark_schema_from_dict(schema_info)
        ```

    Args:
        schema_info (list): A list with information about fields of a DataFrame

    Returns:
        A StructType object structured in such a way that makes it possible to\
        create a Spark DataFrame with a predefined schema.
    """

    # Extracing the schema based on the preconfigured dict info
    schema = StructType([
        StructField(
            field_info["attribute"],
            parse_string_to_spark_dtype(field_info["dtype"])(),
            nullable=field_info["nullable"]
        ) for field_info in schema_info
    ])

    return schema


# Creating a dictionary with DataFrames to mock all sources
def create_spark_dataframe_from_json_info(
    json_path: dict,
    spark: SparkSession = spark,
) -> dict:
    """Creates a dictionary of Spark DataFrames based on inputs on a JSON file.

    This function receives the path for a user defined JSON file containing
    all information needed to specify all the sources to be on the Glue job
    deployed and also testes on the pipeline in order to return a dictionary
    of Spark DataFrames based on configs provided by users on the JSON file.

    Example:
        ```python
        # Defining the path for the JSON file that defines all source data
        json_path = "../configs/source_schemas.json"

        # Getting a dictionary of Spark DataFrames based on user configs
        source_dataframes = create_spark_dataframe_from_json_info(json_path)
        ```

    Args:
        json_path (str):
            The path for the JSON file provided by user with all information
            needed to create Spark DataFrames for all source data for the job

        spark (pyspark.sql.SparkSession):
            A SparkSession object to call Spark methods

    Returns:
        A Python dictionary composed by multiple DataFrame objects based on\
        inputs provided by users on the JSON file.
    """

    # Reading JSON file with all schemas definition
    json_data_info = get_json_data_info(
        json_path=json_path,
        json_main_key="source"
    )

    # Creating an empty dict to store all source DataFrames
    sources_dataframes = {}

    # Iterating over all source schemas in order to create Spark DataFrames
    for source_data in json_data_info:
        # Returning a valid Spark DataFrame schema
        schema = create_spark_schema_from_schema_info(source_data["schema"])

        # Checking if users want to create an empty DataFrame
        if source_data["empty"]:
            # Creating a list of empty tuples to fill Dataframe with null data
            data = [tuple([None] * len(source_data["schema"]))]
        else:
            # Checks if users want to fill DataFrames with fake data
            if source_data["fake_data"]:
                pass  # ToDo: function to fake data based on dtype using faker
            else:
                # Using data provided by users in the JSON file
                data = [tuple(row) for row in source_data["data"]]

        # Creating a Spark DataFrame and adding a new entry on dictionary
        df_reference = source_data["dataframe_reference"]
        sources_dataframes[df_reference] = spark.createDataFrame(
            data=data, schema=schema
        )

    return sources_dataframes
