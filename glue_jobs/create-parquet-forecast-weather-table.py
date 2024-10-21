import boto3

client = boto3.client('athena')

# Refresh the table
queryStart = client.start_query_execution(
    QueryString="""
    CREATE TABLE IF NOT EXISTS open_meteo_forecast_weather_data_parquet_tbl WITH
    (
        external_location='s3://forecast-weather-table-pqt-nikolas/',
        format='PARQUET',
        write_compression='SNAPPY',
        partitioned_by = ARRAY['capture_year', 'capture_month', 'capture_day', 'capture_hour']
    )
    AS
    SELECT
        latitude,
        longitude,
        time,
        temp_c_max,
        temp_c_min,
        ROUND((temp_c_max * 9/5) + 32, 2) AS temp_f_max,
        ROUND((temp_c_min * 9/5) + 32, 2) AS temp_f_min,
        ROUND(daylight_duration / 3600, 2) AS daylight_duration_hours, -- Convert from seconds to hours
        ROUND(sunshine_duration / 3600, 2) AS sunshine_duration_hours, -- Convert from seconds to hours
        precipitation_sum,
        wind_speed_max,
        wind_gusts_max,
        row_ts,
        partition_0 AS capture_year,
        partition_1 AS capture_month,
        partition_2 AS capture_day,
        partition_3 AS capture_hour
     FROM "de_proj_database"."forecast_weather_data_bucket_nikolas"
    WHERE CAST(time AS DATE) >= date_add('day', -7, current_date)
    ORDER BY time DESC;
    
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