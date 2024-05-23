import sys
import awswrangler as wr

# Define the combined quality check query 
COMBINED_DQ_CHECK = f"""
SELECT
  -- Completeness checks
  SUM(CASE WHEN temp_c_mean IS NULL THEN 1 ELSE 0 END) AS missing_temp_c_mean,
  SUM(CASE WHEN temp_f_mean IS NULL THEN 1 ELSE 0 END) AS missing_temp_f_mean,
  SUM(CASE WHEN daylight_duration IS NULL THEN 1 ELSE 0 END) AS missing_daylight_duration,
  SUM(CASE WHEN sunshine_duration IS NULL THEN 1 ELSE 0 END) AS missing_sunshine_duration,
  SUM(CASE WHEN precipitation_sum IS NULL THEN 1 ELSE 0 END) AS missing_precipitation_sum,
  SUM(CASE WHEN wind_speed_max IS NULL THEN 1 ELSE 0 END) AS missing_wind_speed_max,
  SUM(CASE WHEN wind_gusts_max IS NULL THEN 1 ELSE 0 END) AS missing_wind_gusts_max,
  SUM(CASE WHEN row_ts IS NULL THEN 1 ELSE 0 END) AS missing_row_ts,

  -- Extreme values checks (adjust thresholds as needed)
  SUM(CASE WHEN temp_c_min < -20 OR temp_c_max > 50 THEN 1 ELSE 0 END) AS extreme_temp_c,
  SUM(CASE WHEN wind_speed_max > 100 THEN 1 ELSE 0 END) AS extreme_wind_speed,
  SUM(CASE WHEN precipitation_sum < 0 THEN 1 ELSE 0 END) AS negative_precipitation

  
FROM "de_proj_database"."open_meteo_weather_batch_data_parquet_tbl"
"""

# Run the combined quality check
df = wr.athena.read_sql_query(sql=COMBINED_DQ_CHECK, database="de_proj_database")

# Analyze results and exit with appropriate messages
failed_checks = []
for col, val in df.iloc[0].items():
  if val > 0:
    failed_checks.append(col.replace("_", " ").capitalize())

if failed_checks:
  message = f"Quality check failed. Issues found in: {', '.join(failed_checks)}"
  sys.exit(message)
else:
  print('Quality checks passed.')