# AWS S3 bucket details
s3_bucket_name = "your-s3-bucket-name"
mount_name = "/mnt/your_mount_name"  # Choose your mount name
aws_key = dbutils.secrets.get(scope="your_secret_scope", key="aws-access-key-id")
aws_secret = dbutils.secrets.get(scope="your_secret_scope", key="aws-secret-access-key")

# Mount the S3 bucket
dbutils.fs.mount(
    source=f"s3a://{s3_bucket_name}",
    mount_point=mount_name,
    extra_configs={
        "fs.s3a.access.key": aws_key,
        "fs.s3a.secret.key": aws_secret
    }
)

# Reading parquet

# Read the Parquet file (assuming it's partitioned by year, month, day)
input_path = f"{mount_name}/your_parquet_location"

# Read the Parquet file into a DataFrame
df = spark.read.parquet(input_path)

# Display the DataFrame
display(df)
