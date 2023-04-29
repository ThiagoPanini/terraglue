"""Test cases for auxiliar modules put no helpers folder.

This file handles all unit tests to check if modules on helpers folder are
working properly in order to provide useful code to help users to create
their own Spark DataFrames to be used on fixtures and test cases.

___
"""

# Importing libraries
import pytest

from tests.helpers.dataframes import parse_string_to_spark_dtype,\
    create_spark_schema_from_dict, create_source_dataframes

from pyspark.sql.types import StructType, StructField, StringType,\
     IntegerType, DecimalType, FloatType, DateType, TimestampType, BooleanType


@pytest.mark.helpers
@pytest.mark.dataframes
def test_string_reference_is_parsed_to_spark_stringtype():
    """
    G: given that users want to parse a "string" reference to a Spark dtype
    W: when the function parse_string_to_spark_dtype() is called with
       dtype="string" argument
    T: then the return object must be a StringType Spark object
    """

    assert parse_string_to_spark_dtype(dtype="string") is StringType


@pytest.mark.helpers
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


@pytest.mark.helpers
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


@pytest.mark.helpers
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


@pytest.mark.helpers
@pytest.mark.dataframes
@pytest.mark.parse_string_to_spark_dtype
def test_float_reference_is_parsed_to_spark_decimaltype():
    """
    G: given that users want to parse a "float" reference to a Spark dtype
    W: when the function parse_string_to_spark_dtype() is called with
       dtype="float" argument
    T: then the return object must be a FloatType Spark object
    """

    assert parse_string_to_spark_dtype(dtype="float") is FloatType


@pytest.mark.helpers
@pytest.mark.dataframes
@pytest.mark.parse_string_to_spark_dtype
def test_date_reference_is_parsed_to_spark_decimaltype():
    """
    G: given that users want to parse a "date" reference to a Spark dtype
    W: when the function parse_string_to_spark_dtype() is called with
       dtype="date" argument
    T: then the return object must be a DateType Spark object
    """

    assert parse_string_to_spark_dtype(dtype="date") is DateType


@pytest.mark.helpers
@pytest.mark.dataframes
@pytest.mark.parse_string_to_spark_dtype
def test_timestamp_reference_is_parsed_to_spark_decimaltype():
    """
    G: given that users want to parse a "timestamp" reference to a Spark dtype
    W: when the function parse_string_to_spark_dtype() is called with
       dtype="timestamp" argument
    T: then the return object must be a TimestampType Spark object
    """

    assert parse_string_to_spark_dtype(dtype="timestamp") is TimestampType


@pytest.mark.helpers
@pytest.mark.dataframes
@pytest.mark.parse_string_to_spark_dtype
def test_boolean_reference_is_parsed_to_spark_decimaltype():
    """
    G: given that users want to parse a "boolean" reference to a Spark dtype
    W: when the function parse_string_to_spark_dtype() is called with
       dtype="boolean" argument
    T: then the return object must be a BooleanType Spark object
    """

    assert parse_string_to_spark_dtype(dtype="boolean") is BooleanType


@pytest.mark.helpers
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
