"""Test cases for auxiliar modules put no helpers folder.

This file handles all unit tests to check if modules on helpers folder are
working properly in order to provide useful code to help users to create
their own Spark DataFrames to be used on fixtures and test cases.

___
"""

# Importing libraries
import pytest

from tests.helpers.dataframes import parse_string_to_spark_dtype,\
    create_spark_schema_from_schema_info, get_json_data_info,\
    compare_dataframe_schemas

from tests.conftest import SOURCE_JSON_SCHEMAS_PATH

from pyspark.sql import DataFrame
from pyspark.sql.types import StructType, StringType, IntegerType, LongType,\
    DecimalType, FloatType, DoubleType, BooleanType, DateType, TimestampType


@pytest.mark.dataframes
@pytest.mark.get_json_data_info
def test_get_json_data_info_function_returns_a_python_list():
    """
    G: given that users want to read the preconfigured JSON file
    W: when the function get_json_data_info() is called
    T: then the result must be a Python list
    """

    # Reading the preconfigured JSON file
    json_data_info = get_json_data_info(
        json_path=SOURCE_JSON_SCHEMAS_PATH,
        json_main_key="dataframes"
    )

    assert type(json_data_info) is list


@pytest.mark.dataframes
@pytest.mark.parse_string_to_spark_dtype
def test_string_reference_is_parsed_to_spark_stringtype():
    """
    G: given that users want to parse a "string" reference to a Spark dtype
    W: when the function parse_string_to_spark_dtype() is called with
       dtype="string" argument
    T: then the return object must be a StringType Spark object
    """

    assert parse_string_to_spark_dtype(dtype="string") is StringType


@pytest.mark.dataframes
@pytest.mark.parse_string_to_spark_dtype
def test_int_reference_is_parsed_to_spark_integertype():
    """
    G: given that users want to parse a "int" reference to a Spark dtype
    W: when the function parse_string_to_spark_dtype() is called with
       dtype="int" argument
    T: then the return object must be a IntegerType Spark object
    """

    assert parse_string_to_spark_dtype(dtype="int") is IntegerType


@pytest.mark.dataframes
@pytest.mark.parse_string_to_spark_dtype
def test_integer_reference_is_parsed_to_spark_integertype():
    """
    G: given that users want to parse a "integer" reference to a Spark dtype
    W: when the function parse_string_to_spark_dtype() is called with
       dtype="integer" argument
    T: then the return object must be a IntegerType Spark object
    """

    assert parse_string_to_spark_dtype(dtype="integer") is IntegerType


@pytest.mark.dataframes
@pytest.mark.parse_string_to_spark_dtype
def test_bigint_reference_is_parsed_to_spark_longtype():
    """
    G: given that users want to parse a "bigint" reference to a Spark dtype
    W: when the function parse_string_to_spark_dtype() is called with
       dtype="bigint" argument
    T: then the return object must be a LongType Spark object
    """

    assert parse_string_to_spark_dtype(dtype="bigint") is LongType


@pytest.mark.dataframes
@pytest.mark.parse_string_to_spark_dtype
def test_long_reference_is_parsed_to_spark_longtype():
    """
    G: given that users want to parse a "long" reference to a Spark dtype
    W: when the function parse_string_to_spark_dtype() is called with
       dtype="long" argument
    T: then the return object must be a LongType Spark object
    """

    assert parse_string_to_spark_dtype(dtype="long") is LongType


@pytest.mark.dataframes
@pytest.mark.parse_string_to_spark_dtype
def test_decimal_reference_is_parsed_to_spark_decimaltype():
    """
    G: given that users want to parse a "decimal" reference to a Spark dtype
    W: when the function parse_string_to_spark_dtype() is called with
       dtype="decimal" argument
    T: then the return object must be a DecimalType Spark object
    """

    assert parse_string_to_spark_dtype(dtype="decimal") is DecimalType


@pytest.mark.dataframes
@pytest.mark.parse_string_to_spark_dtype
def test_float_reference_is_parsed_to_spark_floattype():
    """
    G: given that users want to parse a "float" reference to a Spark dtype
    W: when the function parse_string_to_spark_dtype() is called with
       dtype="float" argument
    T: then the return object must be a FloatType Spark object
    """

    assert parse_string_to_spark_dtype(dtype="float") is FloatType


@pytest.mark.dataframes
@pytest.mark.parse_string_to_spark_dtype
def test_double_reference_is_parsed_to_spark_doubletype():
    """
    G: given that users want to parse a "double" reference to a Spark dtype
    W: when the function parse_string_to_spark_dtype() is called with
       dtype="double" argument
    T: then the return object must be a DoubleType Spark object
    """

    assert parse_string_to_spark_dtype(dtype="double") is DoubleType


@pytest.mark.dataframes
@pytest.mark.parse_string_to_spark_dtype
def test_boolean_reference_is_parsed_to_spark_booleantype():
    """
    G: given that users want to parse a "boolean" reference to a Spark dtype
    W: when the function parse_string_to_spark_dtype() is called with
       dtype="boolean" argument
    T: then the return object must be a BooleanType Spark object
    """

    assert parse_string_to_spark_dtype(dtype="boolean") is BooleanType


@pytest.mark.dataframes
@pytest.mark.parse_string_to_spark_dtype
def test_date_reference_is_parsed_to_spark_datetype():
    """
    G: given that users want to parse a "date" reference to a Spark dtype
    W: when the function parse_string_to_spark_dtype() is called with
       dtype="date" argument
    T: then the return object must be a DateType Spark object
    """

    assert parse_string_to_spark_dtype(dtype="date") is DateType


@pytest.mark.dataframes
@pytest.mark.parse_string_to_spark_dtype
def test_timestamp_reference_is_parsed_to_spark_timestamptype():
    """
    G: given that users want to parse a "timestamp" reference to a Spark dtype
    W: when the function parse_string_to_spark_dtype() is called with
       dtype="timestamp" argument
    T: then the return object must be a TimestampType Spark object
    """

    assert parse_string_to_spark_dtype(dtype="timestamp") is TimestampType


@pytest.mark.dataframes
@pytest.mark.parse_string_to_spark_dtype
@pytest.mark.exception
def test_typeerror_exception_when_passing_a_incorrect_dtype_string_reference():
    """
    G: given that users want to parse any string reference to a Spark dtype
    W: when the function parse_string_to_spark_dtype() is called with an
       invalid dtype argument (such as "foo")
    T: then a TypeError must be thrown
    """

    with pytest.raises(TypeError):
        _ = parse_string_to_spark_dtype(dtype="foo")


@pytest.mark.dataframes
@pytest.mark.create_spark_schema_from_schema_info
def test_spark_schema_generated_by_function_is_a_structype_object():
    """
    G: given that users want to generate a valid Spark schema based on infos
       put in a preconfigured JSON file
    W: when the function create_spark_schema_from_schema_info() is called with
       a preconfigured JSON file passed as an argument for the function
    T: then the return must a StructType object representing a Spark schema
    """

    # Reading the preconfigured JSON file
    json_data_info = get_json_data_info(
        json_path=SOURCE_JSON_SCHEMAS_PATH,
        json_main_key="dataframes"
    )

    # Getting the first element for the JSON file
    sample_source_info = json_data_info[0]

    # Getting a Spark schema from schema info extracted from JSON file
    schema = create_spark_schema_from_schema_info(
        schema_info=sample_source_info["schema"]
    )

    # Checking if returned schema is a StructType object
    assert type(schema) is StructType


@pytest.mark.dataframes
@pytest.mark.create_spark_dataframe_from_json_info
def test_function_to_create_spark_dataframes_returns_a_dictionary(
    source_dataframes_dict
):
    """
    G: given that users want to generate Spark DataFrames based on a
       preconfigured JSON file in a specific format
    W: when the function create_spark_dataframe_from_json_info() is called
       with a path for reading the preconfigured JSON file
    T: then the return object must be a Python dictionary
    """

    assert type(source_dataframes_dict) is dict


@pytest.mark.dataframes
@pytest.mark.create_spark_dataframe_from_json_info
def test_dataframes_dict_has_spark_dataframes_as_dictionary_values(
    source_dataframes_dict
):
    """
    G: given that users want to generate Spark DataFrames based on a
       preconfigured JSON file in a specific format
    W: when the function create_spark_dataframe_from_json_info() is called
       with a path for reading the preconfigured JSON file
    T: then the value of any arbitrary key of the returned dictionary must
       be a Spark DataFrame object
    """

    # Getting any arbitrary key from the dictionary
    dict_key = list(source_dataframes_dict.keys())[0]

    assert type(source_dataframes_dict[dict_key]) is DataFrame


@pytest.mark.dataframes
@pytest.mark.create_spark_dataframe_from_json_info
def test_user_defined_sample_data_on_json_file_are_contained_on_df_rows(
    source_dataframes_dict,
    df_key: str = "df_orders"
):
    """
    G: given that users want to generate Spark DataFrames based on a
       preconfigured JSON file in a specific format
    W: when the function create_spark_dataframe_from_json_info() is called
       with a path for reading the preconfigured JSON file and considering that
       there are at least one data source defined by user in the JSON file to
       use a predefined sample data in order to create a Spark DataFrame
    T: then the returned DataFrame for that source data must has its rows
       composed by user defined sample data on JSON file
    """

    # Getting a DataFrame that was configured with user defined sample data
    df_sample = source_dataframes_dict[df_key]

    # Collecting all rows from this DataFrame
    rows = [[value for value in row] for row in df_sample.collect()]

    # Reading the preconfigured JSON file
    json_data_info = get_json_data_info(
        json_path=SOURCE_JSON_SCHEMAS_PATH,
        json_main_key="dataframes"
    )

    # Getting user defined sample data from JSON file
    user_defined_rows = json_data_info[0]["data"]

    # Checking if DataFrame rows are equal to user defined sample rows
    assert rows == user_defined_rows


@pytest.mark.dataframes
def test_source_data_with_empty_flag_on_json_generates_empty_dataframes(
    source_dataframes_dict,
    df_null_key: str = "df_test_null_data"
):
    """
    G: given that users want to generate Spark DataFrames based on a
       preconfigured JSON file in a specific format
    W: when the function create_spark_dataframe_from_json_info() is called
       with a path for reading the preconfigured JSON file and considering that
       there are at least one data source defined by user in the JSON file to
       create an empty DataFrame (key empty: true)
    T: then the returned DataFrame for that data source must have one row
       full of nulls
    """

    # Unpacking the null DataFrame created for test purposes
    df_test_null_data = source_dataframes_dict[df_null_key]

    # Collecting all rows from this DataFrame
    rows = [[value for value in row] for row in df_test_null_data.collect()]

    # Checking if there is only one row and if this row only has null data
    assert len(rows) == 1
    assert list(set(rows[0]))[0] is None


@pytest.mark.dataframes
@pytest.mark.compare_dataframe_schemas
def test_compare_equal_schemas_returns_true_when_nullable_is_false(df_orders):
    """
    G: given that users want to compare two Spark dataframe schemas
    W: when two different DataFrames are compared with nullable flag is False
    T: then the result must be True
    """

    assert compare_dataframe_schemas(df_orders, df_orders,
                                     compare_nullable_info=False)


@pytest.mark.dataframes
@pytest.mark.compare_dataframe_schemas
def test_compare_different_schemas_returns_false_when_nullable_is_false(
    df_orders,
    df_customers
):
    """
    G: given that users want to compare two Spark dataframe schemas
    W: when two different DataFrames are compared with nullable flag is False
    T: then the result must be False
    """

    assert not compare_dataframe_schemas(df_orders, df_customers,
                                         compare_nullable_info=False)


@pytest.mark.dataframes
@pytest.mark.compare_dataframe_schemas
def test_compare_equal_schemas_returns_true_when_nullable_is_true(df_orders):
    """
    G: given that users want to compare two Spark dataframe schemas
    W: when two different DataFrames are compared with nullable flag is True
    T: then the result must be True
    """

    assert compare_dataframe_schemas(df_orders, df_orders,
                                     compare_nullable_info=True)


@pytest.mark.dataframes
@pytest.mark.compare_dataframe_schemas
def test_compare_different_schemas_returns_false_when_nullable_is_true(
    df_orders,
    df_customers
):
    """
    G: given that users want to compare two Spark dataframe schemas
    W: when two different DataFrames are compared with nullable flag is True
    T: then the result must be False
    """

    assert not compare_dataframe_schemas(df_orders, df_customers,
                                         compare_nullable_info=True)
