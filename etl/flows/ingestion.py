# etl/flows/ingestion.py
"""
Prefect Flow: Ingest CSV/Excel/Sheets -> S3 -> Validate (Great Expectations) -> Clean (NLP) -> Load to Postgres mart.
Manual upload via API triggers this.
Error table for failures.
Inspired by , , , , 
"""
import pandas as pd
from prefect import flow, task
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.checkpoint import SimpleCheckpoint
from great_expectations.data_context import FileDataContext
from boto3 import client as boto_client
import fuzzywuzzy  # For cleaning

s3 = boto_client('s3')
context = FileDataContext(project_root_dir="etl/expectations/")  # GX context
checkpoint = SimpleCheckpoint(name="sales_checkpoint", data_context=context)

@task
def download_file(s3_key: str) -> pd.DataFrame:
    """Download from S3."""
    obj = s3.get_object(Bucket=settings.S3_BUCKET, Key=s3_key)
    df = pd.read_csv(obj['Body'])  # Or Excel
    return df

@task
def validate_data(df: pd.DataFrame) -> bool:
    """Great Expectations: Check schema, nulls, ranges."""
    batch_request = RuntimeBatchRequest(
        datasource_name="my_datasource",
        data_connector_name="runtime_data_connector",
        data_asset_name="sales_data",
        runtime_parameters={"batch_data": df},
    )
    results = checkpoint.run(batch_request=batch_request)
    if not results["success"]:
        # Log failures to error table
        pd.DataFrame(results["evaluations"]).to_sql("validation_errors", con=engine, if_exists="append")
        raise ValueError("Validation failed")
    return True

@task
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Data Cleaning: Unify product names with fuzzy matching."""
    master_catalog = pd.read_sql("SELECT name FROM products", con=engine)  # Global or tenant
    for idx, row in df.iterrows():
        best_match = fuzzywuzzy.process.extractOne(row['product_name'], master_catalog['name'])
        if best_match[1] > 80:  # Threshold
            df.at[idx, 'product_name'] = best_match[0]
    # NLP: Detect season (e.g., keyword 'silk' + date -> Navratri alert)
    return df

@flow
def ingestion_flow(s3_key: str, tenant_id: UUID):
    """Orchestrate: Download -> Validate -> Clean -> Load."""
    df = download_file(s3_key)
    validate_data(df)
    cleaned_df = clean_data(df)
    cleaned_df['tenant_id'] = tenant_id
    cleaned_df.to_sql("sales_raw", con=engine, if_exists="append", index=False)
    # Create mart view if needed