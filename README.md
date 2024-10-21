# 📊 Building a Scalable OLAP System for Credit Card Transaction Analysis

## 🌟 Introduction
This project is a continuation of my previous work on creating a transactional storage (MongoDB) for credit card data using an OLTP approach. The current focus is on building an OLAP (Online Analytical Processing) system and creating a data warehouse for downstream users.

🎯 Main Objectives:
1. Construct an OLAP data warehouse by loading data into cloud-distributed storage through various data staging processes.
2. Implement a star schema, a common data model in OLAP systems, by designing fact and dimension tables tailored to business requirements.
3. Gain hands-on experience with modern data engineering solutions like Databricks and dbt to expand my skillset as an aspiring data engineer.

🏢 Scenario:
In financial institutions and service providers, effective data monetization is crucial for driving organizational direction and goals through data-driven solutions. This requires a well-designed system that caters to stakeholder needs. Ideally, every department should be able to integrate and customize the data solution (in this case, the data warehouse) by creating specific departmental data marts.

OLAP is particularly suited for this scenario as it prioritizes fast querying and analytical use cases. Implementing a star schema model further specializes the data warehouse to answer business questions through tailored fact models and related descriptive data in dimension models.

## 📚 Contents

- [The Dataset](#the-dataset)
- [Project Architecture](#project-architecture)
- [Transaction Batch Processing Pipeline](#transaction-batch-processing-pipeline)
- [Project Demo Highlights](#project-demo-highlights)
- [Technical Challenges and Solutions](#-technical-challenges-and-solutions)
- [Conclusion](#-conclusion)
- [Future Enhancements](#-future-enhancements)
- [Connect With Me](#-connect-with-me)
- [Appendix](#-appendix)

## 📊 The Dataset
For simplicity, I used data spanning from 01/01/2020 to 02/01/2020, encompassing both legitimate and fraudulent transactions from a simulated credit card transaction dataset obtained from Kaggle.

The data dictionary is shown below:

| **Attribute**              | **Description**                        |
|----------------------------|----------------------------------------|
| `trans_date_trans_time`   | Transaction date and time                     |
| `cc_num`                  | Credit card number                            |
| `merchant`                | Merchant name                                 |
| `category`                | Merchant category                             |
| `amt`                     | Transaction amount                            |
| `first`                   | First name of credit card holder              |
| `last`                    | Last name of credit card holder               |
| `gender`                  | Gender of credit card holder                  |
| `street`                  | Street address of credit card holder          |
| `city`                    | City of credit card holder                    |
| `state`                   | State of credit card holder                   |
| `zip`                     | ZIP code of credit card holder                |
| `lat`                     | Latitude of credit card holder's location     |
| `long`                    | Longitude of credit card holder's location    |
| `city_pop`                | Population of the cardholder's city           |
| `job`                     | Job of the credit card holder                 |
| `dob`                     | Date of birth of credit card holder           |
| `trans_num`               | Unique transaction identifier                 |
| `unix_time`               | Unix timestamp for the transaction            |
| `merch_lat`               | Latitude of the merchant's location           |
| `merch_long`              | Longitude of the merchant's location          |
| `is_fraud`                | Fraud flag (Target variable: 1 = Fraud, 0 = Not Fraud) |

## 🏗️ Project Architecture
The project leverages several key technologies to create a robust OLAP system:

![Transaction Batch Process Architecture](./images/OLAP_Architecture.jpg)

The data processing pipeline consists of four main phases:

1. Connect 🔌: Scripts extract data from the source, transform it, and send it to target storage for further processing.
2. Processing ⚙️: Raw data undergoes transformation and cleaning.
3. Storage 💾: Processed data is stored in a database optimized for analytical queries.
4. Visualization 📈: Tools analyze and display the processed data, enabling data-driven reporting based on organizational needs.

## 🔄 Transaction Batch Processing Pipeline

![Transaction Batch Process Architecture](./images/OLTP_OLAP_Pipeline_Overview.jpg)

**Note:** Batch Processing Pipeline components are highlighted with blue color stickers. 

The image illustrates the relationship between the previous streaming process of the OLTP system and this OLAP pipeline.

### Detailed Process Flow:

#### Connect
Amazon S3 bucket serves as the data source for this project. The data initially resides in MongoDB (representing the OLTP system storage) and is extracted to S3. This distributed storage solution was chosen to explore AWS cloud services and integrate with Databricks. S3's object storage model, which doesn't use a traditional file hierarchy, aligns well with our data modeling approach.

#### Processing
Spark processing is utilized in two key areas:

1. Data Extraction and Transfer:

- Spark runs in dockerized mode to extract data from MongoDB and transfer it to the S3 bucket.
- The process is detailed in [mongo_to_spark_to_s3.ipynb](./S3bucket/ApacheSpark/mongo_to_spark_to_s3.ipynb).
- After data migration, Databricks is set up and the S3 storage is mounted in the Databricks workspace using [setup_s3_conn.py](./databricks/setup_s3_conn.py)

Key points:
- ensure to have matching JAR package file for Spark-AWS S3 connection
- prepare beforehand required credentials in an `.env` file and set up a S3 bucket
```
example credentials in env file:

AWS_ACCESS_KEY_ID=abc123
AWS_SECRET_ACCESS_KEY=abc123
AWS_DEFAULT_REGION=ap-southeast-5
```
- ensure to run docker-compose (with env) file to enable the said services
```
docker run --env-file /home/user/config/.env -p 8888:8888 -p 4040-4080:4040-4080 pyspark-s3
```
> **Note**: The composed file can be found here [docker-compose.yml](./S3bucket/docker-compose.yml). It should be run first before implementing aforementioned extraction tasks in this project.

2. dbt + Spark (in Databricks):

dbt (data build tool) is used to plan and execute transformations in a DAG (Directed Acyclic Graph) manner within the Databricks lakehouse.
dbt's built-in documentation feature provides visibility into data lineage, enhancing collaboration and preventing redundant transformations.
The transformation process creates three schemas (bronze, silver, and gold) following a medallion architecture, with the gold layer containing tables in a star schema format.
Resulting tables in each schema are saved in the Databricks-provisioned S3 bucket.

#### Storage
The Databricks-provisioned S3 bucket serves as the main storage for this OLAP project. Leveraging Delta Lake, a powerful lakehouse feature, it enables optimized storage governed by a unity catalog. The object storage model of S3 aligns well with the medallion architecture, treating each stored table as a separate object, ensuring modularity and isolation between medal layers.

### Visualization
PowerBI is employed for data visualization. The implemented dashboard provides a comprehensive overview of credit card transaction data, including customer demographics, location information, and key business metrics. An exception report is also included to facilitate drill-down analysis of fraudulent activities and their details. Refer to ![Credit_card_goal2.pbix](./PowerBI/Credit_card_goal2.pbix) for the sample dashboard created.


## 🪧Project Demo Highlights

0. Data Model Setup
- It is essential to setup a model as the final gold layer depends very much on this design. Generally, for a fact table, it usually contain all measurements by stakeholder interest (usually datatype is continuous). For dimension tables, it is descriptive of what the attribute in fact table is all about.
- In this project, I have lay out few potential business questions to start constructing the fact table and created the star schema model below. Refer [Sample_business_requirement.pdf](./Sample_business_requirement.pdf) for guidance on how I select fact dimension using business key metrics.

[star schema](./images/star_schema_powerbi.png)

1. S3 Bucket Setup and Naming Conventions
- Sample filename best practice script and excerpt from AWS official docs

![Sample filename best practice excerpt from AWS official docs](./images/sample_naming_convention_official_aws_doc.png).

- Also, below image is the generated partitoned file in bucket using the sample script:

```
input_df.write \
    .partitionBy("year", "month", "day") \
    .mode("append") \
    .option("compression", "gzip") \
    .parquet(output_path)
```
![Sample filename in custom S3 bucket](./images/sample_sourcebucket_naming.png)

- Sample S3 bucket, my custom bucket `bronze-cctransaction-example` and dedicated databricks S3 bucket
-- the dedicated S3 bucket is auto created when first initialize teh service. It is created with help of AWS CloudFormation which create like a cluster of service require for running databricks including ec2 instance, dedicated virtual private cloud (VPC), S3 bucket for databricks allocatted configuration and for unity catalog and also IAM policy

![S3 bucket creation](./images/sample_bucket_autocreate_databricks.png)

2. Databricks Integration
- Sample script and check on mounting custom S3 bucket on databricks 

![mount S3 bucket on databricks](./images/mount_s3_to_databricks_code.png)

- Upload notebook / script into databricks' workspace

![Upload script into databricks workspace ](./images/sample_attached_script_databricks.png)

- Sample read custom mounted S3 bucket in databricks workspace

![read custom S3 bucket after mount ](./images/sample_readparquet_in_S3.png)

3. Medallion Architecture in databricks
- the materialized dbt model will turn as table alongside its dedicated schema

![Medallion Architecture in databricks ](./images/file_structure_databricks_medallion_layer.png)

4. dbt Project Structure and Configuration
- Sample of a new dbt project file structure. Some important folder and files are:
- models : where all the transformation script for medallion layer is placed. Each script might include a schema.yml script that configure testing of data quality, brief column description etc.

example sql model script:
```
{{ config(
    materialized='table',
    file_format='delta',
    partition_by=['year', 'month', 'day'],
    schema='bronze'
) }}

SELECT * FROM TableA
```

example schema.yml:
```
version: 2

models:
  - name: stg_raw_cc_txn
    description: "A starter dbt model"
    columns:
      - name: trans_num
        description: "Unique transaction number"
        tests:
          - not_null
          - unique
```
- macros : consist of function (repetitive task) or even change of default dbt configuration
- seeds : insert data (more like a lookup table)
- profiles.yml : contain configuration setup and target environment (like run script as dev environment etc). Excerpt:
```
databrick_dbt:
  target: dev
  outputs:
    dev:
      type: databricks
      host: "{{ env_var('DATABRICKS_HOST') }}"
      http_path: "{{ env_var('DATABRICKS_HTTP_PATH') }}"
      schema: "dev"
      token: "{{ env_var('DATABRICKS_TOKEN') }}"
      threads: 1
      database: "s3_databricks_dbt"
```
- dbt_project.yml : define default materialization,file format and schema of model and even store variable here. Excerpt:
```
models:
  databrick_dbt:
    +database: s3_databricks_dbt
    bronze:
      +schema: bronze
      +materialized: table
      +file_format: delta
```
![dbt project filestructure](./images/sample_dbt_file_structure.png)

- Sample required connection setting for configuration of dbt-databricks adapter

![dbt-databricks adapter config ](./images/sample_databricks_menu_and_connection.png)

- Sample testing dbt adapter connection to databricks
-- see in image below the connection is successfully done

![dbt debug ](./images/sample_dbt_debug_log.png)

- Sample `dbt run` log after successfully setup all required file in dbt project

![dbt run log ](./images/sample_dbt_run_log.png)

5. Data Lineage and Documentation
- Sample filename save in databricks' govern S3 bucket
-- the dbt model is materialzed with partition on year, month and day

![Sample filename unity catalog partitioned](./images/sample_databricks_filename_unitcatalog_partitioned.png)

-- another reference is below image, where in unity catalog, the table is stored with random name under file path 'tables' followed by its partiton order. I.e., tables/0x312ncvkf/year=2020/month=01/day=01/part-0001-snappy.parquet

![Sample filename unity catalog](./images/sample_filename_in_unity_catalog.png)

- Database, Schema and table structure from dbt docs
-- dbt provided nice file structure to all schema and tables created using materialize SQL/Python model.  Note that it represent the exact same structure as in file structure in databricks unity catalog

![Database, Schema and table structure from dbt docs](./images/database_databricks_in_docs.png)

- Sample model/table dependency in dbt docs
-- In image below, the landing data in silver layer act as prerequisite layer for staging (stg_customer,stg_location,stg_merchant, stg_transaction)

![Model dependency in dbt docs](./images/sample_dbt_doc_generate_refrenceby.png)

-- Also, dbt docs has lineage graph view option that offers visual DAG relationship of each model as below:

![dbt lineage graph docs](./images/sample_lineage_graph_generated.png)

6. PowerBI Dashboard
- Dashboard demo using PowerBI
-- i encompass teh dashboard into two section where the first is more on overvie of transaction data. User will get a brief idea on how well their service/institution is handling frud transaction. Overview alos helps to focus on region with top fraud instance for example. Then the second section provide the exception report which can be presented to higher ups or even as follow up to frontline on finding anremediation plan for fraud instances.

![powerbi overview](./images/powerbi_overview.png)

![powerbi overview](./images/powerbi_exception_report.png)

7. Cost Monitoring
- Sample cost monitoring using AWS `Billing and Cost Management` service
-- I have created a few budget alert to avoid unwanted spike cost / over budget

![Budget Alert](./images/cost_monitoring.png)

## 🚧 Technical Challenges and Solutions
1. Spark and AWS S3 Connection Setup
- Challenge: Finding compatible versions of aws-java-sdk and hadoop-aws.
- Solution: Identified the Java and Hadoop versions running on the notebook and selected compatible SDK versions.
- Refrence materials here: [ref1](https://stackoverflow.com/questions/52310416/noclassdeffounderror-org-apache-hadoop-fs-streamcapabilities-while-reading-s3-d#:~:text=whatever%20version%20of%20the%20hadoop%2D%20JARs%20you%20have%20on%20your%20local%20spark%20installation%2C%20you%20need%20to%20have%20exactly%20the%20same%20version%20of%20hadoop%2Daws%2C%20and%20exactly%20the%20same%20version%20of%20the%20aws%20SDK%20which%20hadoop%2Daws%20was%20built%20with.%20Try%20mvnrepository%20for%20the%20details. )
2. AWS Region Service Connection
- Challenge: It seems setting up compatible software is not enough. It is equally important to check if the s3 region needs extra configuration like enable region (I notice new region like my case `Kuala Lumpur` need to do this setup). 
- Solution: Ensure to enable version is at latest postion
```
-Dcom.amazonaws.services.s3.enableVx=true
```
3. Insufficient Compute Storage in Databricks
- Challenge: Encountered storage limitations when creating clusters.
- Solution: Refreshed and created new clusters as a workaround.
4. Python Module Support in dbt
- Challenge: this error occur when I try to use python model with locally hsot postgres
- Solution: to solve it, there is only 4 services like Databricks, SNowflake compatible with python dbt model
5. File Naming in Medallion Architecture
I want to implement different prefix to indicate the file is what medla layer or data mart. when I created table (mount my S3 in databricks workspace for example), databricks has its own way of filename creation for storing data. I found that it is due to unity catalog features.Below is sample naming from my custom S3 setup and auto created S3 in databricks (databricks data is managed by unity catalog causing not lenient/custom naming convention when saving table/data)

```
Desired S3: bronze-cctransaction-example.s3.ap-southeast-5.amazonaws.com/mongo/ap-southeast-5/creditcard_trx/bronze/year=2020/month=01/day=01/part-00000-.gz.parquet

Databricks S3: s3://s3-databricks-dbt-stack-bucket/unity-catalog/3559579205239172/__unitystorage/catalogs/810fd750-cd69-44f2-b91e-a6c14cde8fd9/tables/6e6f9b96-8755-4ab1-b2b4-e1276077bf57
```

I have thought about three possible workaround to this problem:
- option 1 - do every transformation in dbt
-- benefit - utilize storage in databricks environment
although filename almost not human readable, it can be considered as different layer as S3 treated file as object
i also manuever the data to see if i have control and it looks like i can still managed the encryption key type, Lifecyle and other governance thingy
- option 2 - create external table in databricks. I have googled and some folks said to use 'location_root' in dbt model's config. It means that the 'location_root' specify will be save file changes. 
-- benefit - i can managed the naming prefix at specified store location
- option 3 - use databricks workspace with only pyspark with no dbt.
-- benefit - I can easily write in custom name and place for storage

For this project, I selected the first option as I would like to utilize databricks and dbt to upmost possible. Although the filenaming is predetermined by unity catalog, I believe as table/materialzed is stored as different
object, it is still in accordance to medallion layer

## 🎓 Conclusion
This OLAP system for credit card transaction analysis demonstrates a robust, scalable approach to handling large volumes of financial data. By leveraging cloud technologies like AWS S3 and Databricks, combined with modern data transformation tools like dbt, we've created a powerful analytical platform capable of providing valuable insights into transaction patterns and potential fraudulent activities.

The implementation of a medallion architecture ensures data quality and enables iterative refinement of our datasets. The star schema model in the gold layer facilitates efficient querying and reporting, making it easier for various departments to derive actionable insights from the data.

Through this project, I've gained valuable experience in cloud-based data engineering, distributed computing with Spark, and advanced data modeling techniques. These skills are crucial for tackling real-world big data challenges in the financial sector and beyond.

## 🚀 Future Enhancements
During my journey of exploring the tools locally, I identified several areas for improvement that could have enhanced the project's complexity, as well as improved data quality and governance overall. Below are some thoughts I have in mind:

- Integrate customized data quality tests using dbt or Great Expectations.
- Implement incremental load strategies such as Slowly Changing Dimensions (SCD).
- Utilize Databricks' Auto Loader feature for more efficient data ingestion.
- Merge workflows using Databricks notebooks and local dbt models for a more streamlined process.
- Implement advanced security measures and data masking for sensitive financial information.

## 🤝 Connect With Me
- [LinkedIn](https://www.linkedin.com/in/faizpuad/)

## 📚 Appendix
- [Kaggle Dataset](https://www.kaggle.com/datasets/kartik2112/fraud-detection?select=fraudTrain.csv)
- [Inspiration & Reference from Coach Andreas Kretz Academy](https://learndataengineering.com/)