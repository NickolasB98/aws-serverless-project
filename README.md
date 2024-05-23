A Severless AWS Project fetching weather data from an API, utilizing these AWS Services: Lambda, Kinesis Firehose, S3, Glue Crawler, Glue ETL Workflow Orchestration, EventBridge as a Lambda Trigger, and CloudWatch Logs for monitoring the Lambda functions and ETL job scripts. The processed data is then visualized using Grafana connected to Athena for interactive exploration.

**Project Architecture**
![Project Architecture](https://github.com/NickolasB98/aws_severless_project/assets/157819544/be0e17c5-8219-4e05-998f-49a3b3fcbaa6)

This project leverages a serverless architecture on AWS to build a data pipeline for weather data.  

**Here's a breakdown of the key components and their roles:**

Data Source: 

<img width="1148" alt="image" src="https://github.com/NickolasB98/aws_severless_project/assets/157819544/0c166040-fe13-4055-af62-59fc79a71255">


The data originates from the [(https://open-meteo.com/)] API ([([[https://open-meteo.com/en/docs](https://open-meteo.com/en/docs/historical-weather-api#latitude=53.2192&longitude=6.5667&start_date=2024-03-01&end_date=2024-05-15&hourly=&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,daylight_duration,sunshine_duration,precipitation_sum,wind_speed_10m_max,wind_gusts_10m_max&timezone=Europe%2FBerlin](https://archive-api.open-meteo.com/v1/archive?latitude=53.2192&longitude=6.5667&start_date=2024-03-01&end_date=2024-05-15&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,daylight_duration,sunshine_duration,precipitation_sum,wind_speed_10m_max,wind_gusts_10m_max&timezone=Europe%2FBerlin)))]). This API provides access to historical weather data for Groningen,NL the city I obtained my MSc degree. 
Open-meteo provides access through APIs to both historical and real-time weather data for various locations around the world.

**AWS Lambda Functions:**

<img width="668" alt="image" src="https://github.com/NickolasB98/aws_severless_project/assets/157819544/1903f229-5e12-44b4-98af-e9d8160c2984">

**Batch Data Lambda:** This serverless function triggers upon new weather data batches arriving from the API. It likely pre-processes and prepares the data before sending it to the Kinesis Firehose for streaming.


 <img width="650" alt="image" src="https://github.com/NickolasB98/aws_severless_project/assets/157819544/b7781362-ae96-4adc-992b-0fd11e29c91f">

**Continuous Data Lambda:** This function is triggered by AWS EventBridge at time intervals. It's designed to handle continuous streams of weather data, performing real-time processing before sending it to the Firehose.

**Amazon Kinesis Firehose:**

<img width="1043" alt="image" src="https://github.com/NickolasB98/aws_severless_project/assets/157819544/e2c27d1a-f6f9-41f3-b948-e35b638fd78e">


Based on the invoked Lambda function, the Firehose can handle data in two ways:

**Batch Data:** If triggered by the Batch Data Lambda, the Firehose streams the prepared data in batches to its S3 destination.
 
**Continuous Data:** When triggered by the Continuous Data Lambda (at timed intervals), the Firehose continuously streams the real-time data to S3.

AWS offers automated Firehose stream metrics, for Incoming bytes, Put Requests, Records or potential Throttled Records counts:
<img width="1010" alt="image" src="https://github.com/NickolasB98/aws_severless_project/assets/157819544/7136c90c-eeff-4694-b080-14871b26f9b6">

**Amazon S3:**

The firehose delivers the data to an S3 bucket for storage. Firehose automatically partitions the data in a proper way for Glue Crawler to discover the schema, in order to later enable Athena to interactively SQL query the partitioned table.

This is a snapshot of all my S3 buckets, for both the historical batch weather data, and the continuous incoming weather data triggered by the EventBridge.
Both data are fetched by the same Firehose.

<img width="1019" alt="image" src="https://github.com/NickolasB98/aws_severless_project/assets/157819544/385db9fb-3528-420d-8707-e89e484c627a">


**AWS Glue:**

**Glue Crawler:** 
This automatically discovers and defines the schema of the weather data stored in S3.

<img width="1064" alt="image" src="https://github.com/NickolasB98/aws_severless_project/assets/157819544/93a7db7d-bff3-46ea-89dc-a57b32aeab63">


**Glue ETL Workflow Orchestration:** 
We utilize Glue's capabilities to define and orchestrate the data transformation logic. A series of Glue jobs perform data transformations, data quality checks, and ultimately save the processed data to a new table stored as Parquet files.

<img width="1058" alt="image" src="https://github.com/NickolasB98/aws_severless_project/assets/157819544/f488cf8f-487b-4577-a521-be719e0c5a91">

		
**Amazon Athena:**
This serverless interactive query service allows us to analyze the transformed weather data using standard SQL queries.

<img width="1282" alt="image" src="https://github.com/NickolasB98/aws_severless_project/assets/157819544/60e91fc8-13f6-4b06-87d4-cbe61e6f9553">

<img width="912" alt="image" src="https://github.com/NickolasB98/aws_severless_project/assets/157819544/19401e2c-8a25-4d34-8717-8b4d5db2da79">


**Grafana:**
Grafana, a visualization tool, connects to Athena, enabling the creation of interactive dashboards to explore the weather data insights. You can leverage standard SQL queries within Grafana to visualize the processed data.

While static images of the dashboard are be included below, the power of Grafana lies in its interactivity. To explore the dashboard functionalities directly, you can access a linked snapshot: [Grafana Dashboard Snapshot]([https://nickolasb98.grafana.net/dashboard/snapshot/1uXP8OvJex8ybSvKMYCoRaydwpI9eooa](https://nickolasb98.grafana.net/dashboard/snapshot/Ai88cLexmGBYYFXgAwDgwEasJz8C3c3W))


<img width="1057" alt="image" src="https://github.com/NickolasB98/aws_severless_project/assets/157819544/9c588c46-a12b-4fd4-afca-445e12d04130">

<img width="1069" alt="image" src="https://github.com/NickolasB98/aws_severless_project/assets/157819544/9cbc1248-523b-4ad6-9e85-ed60bed9836d">


**Pipeline Functionality:**

Data Ingestion: A Lambda function is triggered periodically (or based on an event) to fetch weather data from the chosen API.

Data Streaming: The retrieved data is sent to Amazon Kinesis Firehose for continuous streaming.

Data Storage: The Firehose delivers the data to an S3 bucket for raw data storage.

Schema Discovery: A Glue Crawler automatically discovers and defines the schema of the data stored in S3.

Data Transformation:
	Glue ETL jobs are designed to:
	Cleanse and transform the data as needed.
	Perform data quality checks to ensure data integrity.

Data Storage (Processed): The transformed data is saved to a new table in S3 using the Parquet format, optimized for analytics.

Data Analysis: Amazon Athena, when connected to Grafana Cloud, allows querying the processed weather data using standard SQL for further analysis and visualization.

Monitoring:

This project utilizes AWS CloudWatch Logs for centralized monitoring of the data pipeline components. CloudWatch Logs capture details about:
	**Lambda Function Execution:** Invocation time, duration, and any errors encountered during data ingestion.
	**Glue ETL Job Execution:** Start and end times, completed job steps, and any errors during data transformation.
By analyzing CloudWatch Logs, you can identify potential issues, monitor performance, and ensure the smooth operation of the pipeline.

**Benefits:**

Scalability and Cost-Efficiency: Serverless architecture scales automatically based on data volume and minimizes infrastructure management costs.

Flexibility: The pipeline can be easily adapted to handle different weather APIs or data sources.

Automation: Data ingestion, transformation, and storage are automated, reducing manual intervention.

Analytics Ready: The processed data in Parquet format is optimized for efficient querying with Athena.
