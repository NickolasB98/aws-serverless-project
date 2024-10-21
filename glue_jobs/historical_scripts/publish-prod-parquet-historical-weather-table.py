import boto3

client = boto3.client('athena')

# Refresh the table
queryStart = client.start_query_execution(
    QueryString = f"""
    CREATE TABLE IF NOT EXISTS open_meteo_historical_weather_data_parquet_tbl_PROD WITH
    (external_location='s3://parquet-weather-table-prod-nikolas/',
    format='PARQUET',
    write_compression='SNAPPY',
    partitioned_by = ARRAY['capture_year', 'capture_month', 'capture_day', 'capture_hour']
    )
    AS

    SELECT
        *
    FROM "de_proj_database"."open_meteo_historical_weather_data_parquet_tbl"

    ;
    """,
    QueryExecutionContext = {
        'Database': 'de_proj_database'
    }, 
    ResultConfiguration = { 'OutputLocation': 's3://store-query-results-for-athena-may-2024-nickolas/'}
)