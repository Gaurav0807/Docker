import pandas as pd
import great_expectations as ge
from great_expectations.dataset import PandasDataset
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, JSON, ForeignKey
import logging
import json

def validate_and_save_data():
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    file_path = "/opt/airflow/jobs/taxi_data.csv"
    postgres_url = "postgresql://airflow:airflow@postgres:5432/airflow"
    table_name = "gx_validation"

    # Read data from a CSV file into a pandas DataFrame
    data = pd.read_csv(file_path)

    # Create a Great Expectations PandasDataset
    dataset = ge.dataset.PandasDataset(data)

    # Create an expectation suite
    expectation_suite = dataset.expect_column_values_to_not_be_null("service_zone")

    # Validate the data using the expectation suite
    #dataset.validate(expectation_suite)
    
    logging.info("Results")
    

    results = dataset.validate()
    logging.info(results)
    
    # Convert relevant information from results to JSON-serializable format
    json_results = {
        "success": str(results['results'][0]['success']),
        "expectation_config": results["results"][0]["expectation_config"],
        "result": results["results"][0]["result"],
        "meta": results["meta"],
    }

    # Extract specific details
    expectation_config = results['results'][0]['expectation_config']
    expectation_name = expectation_config['expectation_type']
    result = str(results['results'][0]['success'])
    message = results.get('results', [{}])[0].get('exception_info', {}).get('exception_message', '')

    # Convert expectation_config to a dictionary
    expectation_config_dict = {
        "expectation_type": expectation_config['expectation_type'],
        "kwargs": expectation_config.get('kwargs', {}),
        "meta": expectation_config.get('meta', {}),
    }


    # Connect to PostgreSQL database
    engine = create_engine(postgres_url)

    # Define the table schema
    metadata = MetaData()
    my_table = Table(
        table_name,
        metadata,
        Column("id", Integer, primary_key=True),
        Column("data_quality_id", Integer, ForeignKey("gx_validation.id")),
        Column("expectation_name", String),
        Column("result", String),
        Column("message", String),
        Column("validation_results", JSON),
    )

    logging.info(my_table)
    logging.info(my_table.columns)

    # Try to create the table if it doesn't exist
    try:
        metadata.create_all(engine, checkfirst=True)
        my_table.create(engine, checkfirst=True)
        logging.info(f"Table {table_name} created successfully.")
        logging.info(metadata.create_all(engine, checkfirst=True))
    except Exception as e:
        logging.error(f"Error creating table: {str(e)}")

    # Save the data to the PostgreSQL table
    try:
        # Insert data into both tables
        data.to_sql(table_name, engine, index=False, if_exists="replace")
        engine.execute(
            f"INSERT INTO {table_name} (expectation_name, result, message, validation_results) "
            f"VALUES ('{expectation_name}', '{result}', '{message}', '{json.dumps(expectation_config_dict)}')"
        )

        logging.info(f"Data and validation results successfully saved to PostgreSQL table: {table_name}")
    except Exception as e:
        logging.error(f"Error saving data to PostgreSQL: {str(e)}")
