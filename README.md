A Serverless AWS Project fetching weather data from an API, utilizing these AWS Services: Lambda, Kinesis Firehose, S3, Glue Crawler, Glue ETL Workflow Orchestration, EventBridge as a Lambda Trigger, and CloudWatch Logs for monitoring the Lambda functions and ETL job scripts. The processed data is then visualized using Grafana connected to Athena for interactive exploration.

**Project Architecture**
![Project Architecture](https://github.com/NickolasB98/aws_severless_project/assets/157819544/be0e17c5-8219-4e05-998f-49a3b3fcbaa6)

This project leverages a serverless architecture on AWS to build two data pipelines for weather data.  

##### The project's interactive snapshot of Historical weather visualizations in Grafana: 
[https://nickolasb98.grafana.net/dashboard/snapshot/m4CRJegtK7BHuHdACZ2LzTgdeiiMYUdi]

##### The project's interactive snapshot of Forecast weather visualizations in Grafana: 
[https://nickolasb98.grafana.net/dashboard/snapshot/dDK8XqEN93xn5XqgJQvvfUwl7g7j3Xul]

**Here's a breakdown of the key components and their roles:**

**Data Source:** 

<img width="1191" alt="image" src="https://github.com/user-attachments/assets/dd003295-a8a0-4835-a1ab-43d664e0346f">



The data originates from the [(https://open-meteo.com/)] API ([([[https://open-meteo.com/en/docs](https://open-meteo.com/en/docs/historical-weather-api#latitude=53.2192&longitude=6.5667&start_date=2024-03-01&end_date=2024-05-15&hourly=&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,daylight_duration,sunshine_duration,precipitation_sum,wind_speed_10m_max,wind_gusts_10m_max&timezone=Europe%2FBerlin](https://archive-api.open-meteo.com/v1/archive?latitude=53.2192&longitude=6.5667&start_date=2024-03-01&end_date=2024-05-15&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,daylight_duration,sunshine_duration,precipitation_sum,wind_speed_10m_max,wind_gusts_10m_max&timezone=Europe%2FBerlin)))]). This API provides access to historical weather data for Groningen,NL the city I obtained my MSc degree. 
Open-meteo provides access through APIs to both historical and real-time weather data for various locations around the world.

**AWS Lambda Functions:**

**get-batch-weather-data:** This serverless function triggers manually. It pre-processes and prepares the data before sending it to the Kinesis Firehose for batch streaming of historical weather data.

<img width="668" alt="image" src="https://github.com/NickolasB98/aws_severless_project/assets/157819544/1903f229-5e12-44b4-98af-e9d8160c2984">

**get-real-time-weather-data:** This function is triggered by AWS EventBridge at time intervals every 7 days. It is designed to handle  streams of forecast weather data each week, performing real-time processing before sending it to Kinesis Firehose.

<img width="855" alt="image" src="https://github.com/user-attachments/assets/70b22bf0-8eb5-41d3-817f-b7a6793b5d48">


**Amazon Data Firehose (Former Kinesis Firehose):**

<img width="1081" alt="image" src="https://github.com/user-attachments/assets/f11369e1-c7a8-4810-b9dd-a69e4881be12">


Based on the invoked Lambda function, the Firehose can handle both historical and forecast weather data:

**Historical Weather Data:** If triggered by the historical Data Lambda, the Firehose streams the prepared data in batches to its S3 destination in one single batch.
 
**Weekly Forecast Weather Data:** When triggered at 7-day timed intervals, the Firehose streams the real-time forecast data to an S3 bucket, creating subfolders based on the time of year / month / week the data was captured from the open-meteo api. This action creates different weekly folder and is later utilized by AWS Glue crawler to figure the datetime based partitions automatically.

AWS offers automated Firehose stream metrics, for Incoming bytes, Put Requests, Records or potential Throttled Records counts,etc. :

<img width="1420" alt="image" src="https://github.com/user-attachments/assets/a2973e2f-bc4c-4d59-b20a-68c70304e9ae">


**Amazon S3:**

Amazon S3 serves as the storage layer for this project, housing the weather data at various stages of the pipeline. Here's a breakdown of the different S3 buckets and their purposes:

#### Weather Data Buckets:

(forecast)-weather-data-bucket: These buckets store the raw, unprocessed weather data received from the Open-Meteo API, having already been invoked by the Lambda function and consumed by the Data Firehose. The data format can be JSON, the original format provided by the API. These buckets might be named with timestamps or identifiers indicating the time period of the data (e.g., May 2024).

#### Processed Data Buckets:

weather-table-pqt-nikolas/: This bucket contain the historical weather data that has been processed and converted into the Parquet format by ETL job scripts. Parquet is columnar and optimized for efficient querying with Athena, making it ideal for later analysis.

forecast-weather-table-pqt-nikolas/: This bucket holds the transformed forecast weather data stored in Parquet format. Each week, a new subfolder is created by the Firehose inside this s3, reffering to the month and week the new weekly data was captured by the API. This way, the next week's forecast weather is being added every 7 days in a different week subfolder inside the same month / year.

#### Production-level Data Buckets:

These buckets hold the final, transformed weather data stored in Parquet format, making the final product of the ETL Workflow. This is the data readily available for querying and analysis with Athena and potentially for visualization with Grafana.

The data inside this bucket have already undergone the other ETL job processes, including passing or failing the Data Quality checks. The final data is now production ready and stored in the buckets: (forecast)-parquet-weather-table-prod-nikolas/

#### Temporary Buckets:

Buckets named like aws-athena-query-results-** / `store-query-results-for-athena-** are used temporarily to store the results of Athena queries. Depending on the configuration, these buckets could be automatically cleaned up after a set period.

#### Firehose Partitioning into the S3:

The Kinesis Firehose automatically partitions the data as it delivers it to S3 buckets. This partitioning helps Glue Crawler efficiently discover the schema of the data. Each partition represents a specific time period or data segment, making it easier to query and analyze specific weather data ranges using Athena later.

By utilizing different S3 buckets for various data stages, the project maintains a clear separation between raw, processed, and final weather data. This organization simplifies data retrieval for analysis and ensures efficient querying with Athena.

This is a snapshot of all my S3 buckets, for both the historical batch weather data, and the continuous incoming weather data triggered by the EventBridge.
Both data are fetched by the same Firehose.

<img width="1045" alt="image" src="https://github.com/user-attachments/assets/1218ac96-041b-4351-9e8d-33bfe7668d7e">

<img width="1050" alt="image" src="https://github.com/user-attachments/assets/25cf71a5-e0b7-4270-95a2-591f37e5d821">


**AWS Glue:**

**Glue Crawler:** 

Crawler automatically discovers and defines the schema of the weather data stored in S3. It also creates the table's partitions based on the different subfolders already created by the Firehose. **('capture_year', 'capture_month', 'capture_day', 'capture_hour')** The created tables have their schema already correctly defined and the parquet formatted data can be partitioned effectively leading to faster queries and lower costs.

Historical Weather Crawler:

<img width="1087" alt="image" src="https://github.com/user-attachments/assets/a2bc7f7d-45b6-4e25-9d59-dfb718d4e525">

Forecast Weather Crawler:

<img width="1097" alt="image" src="https://github.com/user-attachments/assets/475c705f-3d24-4fe1-be8d-abec071d460b">


**Glue ETL Workflow Orchestration:** 

We utilize Glue's capabilities to define and orchestrate the data transformation logic. A series of Glue jobs perform data transformations, data quality checks, and ultimately save the processed data to a new table stored as Parquet files.

This is the historical weather pipeline.

<img width="1071" alt="image" src="https://github.com/user-attachments/assets/5b030034-918a-4cc4-ad85-ba2f608b7c71">


The workflow consists of the Glue crawler, ETL Jobs written in Python, and Triggers between them.
It also has a Starting Trigger that can be connected to EventBridge events.

An ETL job example written in Python, which wraps a SQL query in order to create the Parquet historical weather table.

**create-parquet-historical-weather-table**


	import boto3
	
	client = boto3.client('athena')
	
	# Refresh the table
	queryStart = client.start_query_execution(
	    QueryString="""
	    CREATE TABLE IF NOT EXISTS open_meteo_historical_weather_data_parquet_tbl WITH
	    (
	        external_location='s3://weather-table-pqt-nikolas/',
	        format='PARQUET',
	        write_compression='SNAPPY',
	        partitioned_by = ARRAY['capture_year', 'capture_month', 'capture_day', 'capture_hour']
	    )
	    AS
	    SELECT
	        latitude,
	        longitude,
	        time,
	        temp_c_mean,
	        ROUND((temp_c_mean * 9/5) + 32, 2) AS temp_f_mean, -- Temperature in Fahrenheit (rounded to 2 decimals)
	        temp_c_max,
	        temp_c_min,
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
	    FROM "de_proj_database"."weather_data_bucket_oct_2024"
	    
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


This ETL script uses Amazon Athena and S3 to create a table for storing the processed weather data in a Parquet format. It checks if a table named open_meteo_historical_weather_data_parquet_tbl exists, and if not, it creates it. It selects data from an existing table and transforms it —for example, converting temperatures to Fahrenheit and converting durations from seconds to hours. The data is partitioned by year, month, day, and hour, based on the capture time. Finally, the output is stored in the S3 bucket for processed data.

The Forecast Weather Pipeline works differently by being triggered whenever a new object is added to the designated S3 bucket for forecast weather data. This trigger occurs after data from the API is captured and processed using the get-real-time-weather-data function, ensuring that the weekly forecast data is successfully stored. This event-based trigger automatically starts the workflow, ultimately updating the production-level table.

<img width="1098" alt="image" src="https://github.com/user-attachments/assets/b3fb632f-520d-44a8-9203-68aac32d1c18">

This is a snapshot of the EventBridge rule that triggers our pipeline.

<img width="1043" alt="image" src="https://github.com/user-attachments/assets/1a60d965-8c00-42fe-9ac0-73b3ef9337b8">


**Amazon Athena:**

This serverless interactive query service allows us to analyze the transformed weather data using standard SQL queries.

<img width="1360" alt="image" src="https://github.com/user-attachments/assets/87d6c4f8-c023-44f4-bba3-2620e950c0cc">


**Grafana:**

Grafana is the visualization tool that connects to Athena, enabling the creation of interactive dashboards to explore the weather data insights. You can leverage standard SQL queries within Grafana to visualize the processed data. The queries are exectuted directly in Athena and can be found also in the Recent Queries tab.


The static snapshots as pdf files for a quick overview:

### Severless AWS Project Groningen's Historical Weather Dashboard

<img width="1426" alt="image" src="https://github.com/user-attachments/assets/1e2b6406-1e6f-4097-beca-a33f8edd2dcc">

<img width="1402" alt="image" src="https://github.com/user-attachments/assets/6a071520-4511-45cd-9384-60a433fbfde6">

<img width="1411" alt="image" src="https://github.com/user-attachments/assets/d5ac6cc5-dc27-4a95-9915-b1418466d511">

<img width="1405" alt="image" src="https://github.com/user-attachments/assets/502c6c94-994e-4125-b0e5-edfd9bd859ac">

<img width="1410" alt="image" src="https://github.com/user-attachments/assets/f2b1d0d2-2e5d-4c99-921a-4cda556a7ead">

<img width="1409" alt="image" src="https://github.com/user-attachments/assets/fa8a3fc0-38a5-4eb3-b39a-710ae98c48aa">

### Severless AWS Project Groningen's Weekly Forecast Weather Dashboard

<img width="1418" alt="image" src="https://github.com/user-attachments/assets/7a20267e-1975-443c-b871-55f6599f4877">

<img width="1404" alt="image" src="https://github.com/user-attachments/assets/0c45cd17-6c1d-4285-815d-c4d89e4ccf7e">

<img width="1410" alt="image" src="https://github.com/user-attachments/assets/24814b23-c459-4bf6-9f7b-d940bdb1a6db">

<img width="1400" alt="image" src="https://github.com/user-attachments/assets/d7bc9b35-b696-474d-99dd-974c4bf2a403">



**Pipeline Functionality:**

Data Ingestion: A Lambda function is triggered periodically (or based on an event) to fetch weather data from the chosen API.

Data Streaming: The retrieved data is sent to Amazon Kinesis Firehose for continuous streaming.

Data Storage: The Firehose delivers the data to an S3 bucket for raw data storage.

Schema Discovery: A Glue Crawler automatically discovers and defines the schema of the data stored in S3.

Data Transformation:
	Glue ETL jobs are designed to:
	Cleanse and transform the data as needed.
	Perform data quality checks to ensure data integrity.

Data Quality Checks:

The completeness checks include verifying if any key columns have missing values, such as temperature, daylight duration, sunshine duration, precipitation, wind speed, wind gusts, and row timestamps. For each column, it counts the number of missing values.

The extreme values checks evaluate whether certain values fall outside of expected ranges. 

Temperature values below -30°C or above 50°C.
Wind speeds exceeding 100 km/h.
Negative precipitation values.

Data Storage (Processed): The transformed data is saved to a new table in S3 using the Parquet format, optimized for analytics.

Data Analysis: Amazon Athena, when connected to Grafana Cloud, allows querying the processed weather data using standard SQL for further analysis and visualization.

Monitoring:
This project utilizes AWS CloudWatch Logs for centralized monitoring of the data pipeline components. CloudWatch Logs capture details about:
	Lambda Function Execution: Invocation time, duration, and any errors encountered during data ingestion.
	Glue ETL Job Execution: Start and end times, completed job steps, and any errors during data transformation.
By analyzing CloudWatch Logs, you can identify potential issues, monitor performance, and ensure the smooth operation of the pipeline.

**Benefits:**

Scalability and Cost-Efficiency: Serverless architecture scales automatically based on data volume and minimizes infrastructure management costs.

Flexibility: The pipeline can be easily adapted to handle different weather APIs or data sources.

Automation: Data ingestion, transformation, and storage are automated, reducing manual intervention.

Analytics Ready: The processed data in Parquet format is optimized for efficient querying with Athena.
