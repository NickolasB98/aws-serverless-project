A Severless AWS Project fetching weather data from an API, utilizing these AWS Services: Lambda, Kinesis Firehose, S3, Glue Crawler, Glue ETL Workflow Orchestration, Athena, and Grafana which was connected with AWS Athena, visualizing the transformed data by leveraging SQL queries.

**Project Architecture**
![Project Architecture](https://github.com/NickolasB98/aws_severless_project/assets/157819544/be0e17c5-8219-4e05-998f-49a3b3fcbaa6)

This project leverages a serverless architecture on AWS to build a data pipeline for weather data.  Here's a breakdown of the key components and their roles:

**Data Source:** We are fetching weather data from an external API.

**AWS Lambda Functions:**

**Batch Data Lambda:** This serverless function triggers upon new weather data batches arriving from the API. It likely pre-processes and prepares the data before sending it to the Kinesis Firehose for streaming.

**Continuous Data Lambda:** This function is triggered by AWS EventBridge at time intervals. It's designed to handle continuous streams of weather data, performing real-time processing before sending it to the Firehose.

**Amazon Kinesis Firehose:** Based on the invoked Lambda function, the Firehose can handle data in two ways:

  **Batch Data:** If triggered by the Batch Data Lambda, the Firehose streams the prepared data in batches to its S3 destination.
 
  **Continuous Data:** When triggered by the Continuous Data Lambda (at timed intervals), the Firehose continuously streams the real-time data to S3.

**Amazon S3:** The firehose delivers the data to an S3 bucket for storage. Firehose automatically partitions the data in a proper way for Glue Crawler to discover the schema, in order to enable Athena to interactively SQL query the partitioned table.

**AWS Glue:**

  **Glue Crawler:** This automatically discovers and defines the schema of the weather data stored in S3.
  
  **Glue ETL Workflow Orchestration:** We utilize Glue's capabilities to define and orchestrate the data transformation logic. A series of Glue jobs perform data transformations, data quality checks, and ultimately save the processed data to a new table stored as Parquet files.
		
**Amazon Athena:** This serverless interactive query service allows us to analyze the transformed weather data using standard SQL queries.

**Grafana:** This visualization tool connects to Athena, enabling the creation of interactive dashboards through SQL queries, to explore the weather data insights.
