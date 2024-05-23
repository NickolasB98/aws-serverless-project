import boto3

client = boto3.client('athena')

# Refresh the table
queryStart = client.start_query_execution(
    QueryString="""
    CREATE TABLE IF NOT EXISTS open_meteo_weather_batch_data_parquet_tbl WITH
    (
        external_location='s3://open-meteo-weather-data-parquet-bucket-nickolas/',
        format='PARQUET',
        write_compression='SNAPPY',
        partitioned_by = ARRAY['time'])
    AS
    
    SELECT
        latitude
        ,longitude
        ,temp_c_mean
        ,(temp_c_mean * 9/5) + 32 AS temp_f_mean  -- Adjusted conversion formula
        ,temp_c_max
        ,temp_c_min
        ,daylight_duration
        ,sunshine_duration
        ,precipitation_sum
        ,wind_speed_max
        ,wind_gusts_max
        ,row_ts
        ,time
        
    FROM "de_proj_database"."gro-meteoweather_batch_databucket_nickolas"
    
    ;
    """,
    QueryExecutionContext={
        'Database': 'de_proj_database'
    },
    ResultConfiguration={
        'OutputLocation': 's3://store-query-results-for-athena-may-2024-nickolas'
    }
)

print(f"Query execution started. Check Athena console for details.")