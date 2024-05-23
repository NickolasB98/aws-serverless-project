A Severless AWS Project fetching weather data from an API, utilizing these AWS Services: Lambda, Kinesis Firehose, S3, Glue Crawler, Glue ETL Workflow Orchestration, Athena, and Grafana which was connected with AWS Athena, visualizing the transformed data by leveraging SQL queries.

**Project Architecture**
![Project Architecture](https://github.com/NickolasB98/aws_severless_project/assets/157819544/be0e17c5-8219-4e05-998f-49a3b3fcbaa6)

This project leverages a serverless architecture on AWS to build a data pipeline for weather data.  

**Here's a breakdown of the key components and their roles:**

Data Source: 

The data originates from the [(https://open-meteo.com/)] API ([([[https://open-meteo.com/en/docs](https://open-meteo.com/en/docs/historical-weather-api#latitude=53.2192&longitude=6.5667&start_date=2024-03-01&end_date=2024-05-15&hourly=&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,daylight_duration,sunshine_duration,precipitation_sum,wind_speed_10m_max,wind_gusts_10m_max&timezone=Europe%2FBerlin](https://archive-api.open-meteo.com/v1/archive?latitude=53.2192&longitude=6.5667&start_date=2024-03-01&end_date=2024-05-15&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,daylight_duration,sunshine_duration,precipitation_sum,wind_speed_10m_max,wind_gusts_10m_max&timezone=Europe%2FBerlin)))]). This API provides access to historical weather data for Groningen,NL the city I obtained my MSc degree. 
Open-meteo provides access through APIs to both historical and real-time weather data for various locations around the world.

AWS Lambda Functions:

	Batch Data Lambda: This serverless function triggers upon new weather data batches arriving from the API. It likely pre-processes and prepares the data before sending it to the Kinesis Firehose for streaming.

	Continuous Data Lambda: This function is triggered by AWS EventBridge at time intervals. It's designed to handle continuous streams of weather data, performing real-time processing before sending it to the Firehose.

Amazon Kinesis Firehose: 

Based on the invoked Lambda function, the Firehose can handle data in two ways:

	Batch Data: If triggered by the Batch Data Lambda, the Firehose streams the prepared data in batches to its S3 destination.
  	Continuous Data: When triggered by the Continuous Data Lambda (at timed intervals), the Firehose continuously streams the real-time data to S3.

Amazon S3: 

The firehose delivers the data to an S3 bucket for storage. Firehose automatically partitions the data in a proper way for Glue Crawler to discover the schema, in order to enable Athena to interactively SQL query the partitioned table.

AWS Glue:

  	Glue Crawler: This automatically discovers and defines the schema of the weather data stored in S3.
  
  	Glue ETL Workflow Orchestration: We utilize Glue's capabilities to define and orchestrate the data transformation logic. A series of Glue jobs perform data transformations, data quality checks, and ultimately save the processed data to a new table stored as Parquet files.
		
Amazon Athena: 

This serverless interactive query service allows us to analyze the transformed weather data using standard SQL queries.

Grafana: 

This visualization tool connects to Athena, enabling the creation of interactive dashboards through SQL queries, to explore the weather data insights.



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

**Benefits:**

Scalability and Cost-Efficiency: Serverless architecture scales automatically based on data volume and minimizes infrastructure management costs.

Flexibility: The pipeline can be easily adapted to handle different weather APIs or data sources.

Automation: Data ingestion, transformation, and storage are automated, reducing manual intervention.

Analytics Ready: The processed data in Parquet format is optimized for efficient querying with Athena.
