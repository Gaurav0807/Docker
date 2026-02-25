import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def extract(**context):
    """
    Extract function to read data from CSV and process it.
    This function is called by the Airflow DAG.
    """
    try:
        # Read the taxi data CSV file from docker path
        file_path = '/opt/airflow/jobs/taxi_data.csv'
        
        logger.info(f"Starting extraction from {file_path}")
        

        df = pd.read_csv(file_path)
        
        logger.info(f"Successfully extracted {len(df)} rows from the file")
        logger.info(f"Columns: {df.columns.tolist()}")
        logger.info(f"Data shape: {df.shape}")
        
        # Display first few row
        logger.info(f"\nFirst 5 rows:\n{df.head()}")
        

        logger.info(f"\nData Info:\n{df.info()}")
        

        logger.info(f"\nData Summary:\n{df.describe()}")
        
        # Push data to XCom for downstream tasks
        context['ti'].xcom_push(key='extracted_data', value=df.to_json())
        context['ti'].xcom_push(key='row_count', value=len(df))
        
        logger.info("Extraction completed successfully")
        
        return {
            'status': 'success',
            'rows_extracted': len(df),
            'timestamp': datetime.now().isoformat()
        }
        
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error during extraction: {str(e)}")
        raise
