A Severless AWS Project fetching weather data from an API, utilizing these AWS Services: Lambda, Kinesis Firehose, S3, Glue Crawler, Glue ETL Workflow Orchestration, Athena, and Grafana which was connected with AWS Athena, visualizing the transformed data by leveraging SQL queries.

**Project Architecture**
![Project Architecture](https://github.com/NickolasB98/aws_severless_project/assets/157819544/be0e17c5-8219-4e05-998f-49a3b3fcbaa6)

This project leverages a serverless architecture on AWS to build a data pipeline for weather data.  Here's a breakdown of the key components and their roles:

**Data Source:** We are fetching weather data from an external API.

**AWS Lambda:** This serverless compute service acts as the entry point, triggering upon new data arrival from the API.

**Amazon Kinesis Firehose:** This service continuously streams the incoming weather data to its destination.

**Amazon S3:** The firehose delivers the data to an S3 bucket for storage.

**AWS Glue:**

  **Glue Crawler:** This automatically discovers and defines the schema of the weather data stored in S3.
  
  **Glue ETL Workflow Orchestration:** We utilize Glue's capabilities to define and orchestrate the data transformation logic.
		
**Amazon Athena:** This serverless interactive query service allows us to analyze the transformed weather data using standard SQL queries.

**Grafana:** This visualization tool connects to Athena, enabling the creation of interactive dashboards to explore the weather data insights.
