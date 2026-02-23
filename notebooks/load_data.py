from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("spark://iceberg-sandbox-spark-master:7077")
    .appName("iceberg-sandbox")
    .config("spark.driver.host", "iceberg-sandbox-jupyter")
    .config("spark.driver.bindAddress", "0.0.0.0")
    .config("spark.driver.port", "7078")
    .config("spark.blockManager.port", "7079")
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
    .config("spark.sql.catalog.iceberg_jdbc", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.iceberg_jdbc.catalog-impl", "org.apache.iceberg.jdbc.JdbcCatalog")
    .config("spark.sql.catalog.iceberg_jdbc.uri", "jdbc:postgresql://iceberg-sandbox-postgres:5432/iceberg-jdbc-catalog")
    .config("spark.sql.catalog.iceberg_jdbc.jdbc.user", "iceberg")
    .config("spark.sql.catalog.iceberg_jdbc.jdbc.password", "iceberg")
    .config("spark.sql.catalog.iceberg_jdbc.jdbc.driver", "org.postgresql.Driver")
    .config("spark.sql.catalog.iceberg_jdbc.warehouse", "s3a://iceberg/warehouse")
    .config("spark.hadoop.fs.s3a.endpoint", "http://iceberg-sandbox-minio:9000")
    .config("spark.hadoop.fs.s3a.access.key", "minioadmin")
    .config("spark.hadoop.fs.s3a.secret.key", "minioadmin")
    .config("spark.hadoop.fs.s3a.path.style.access", "true")
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config("spark.executor.cores", "1")
    .config("spark.executor.memory", "1g")
    .config("spark.cores.max", "1")
    .config("spark.ui.showConsoleProgress", "true")
    .getOrCreate()
)

print("=== Create Database ===")
spark.sql("CREATE DATABASE IF NOT EXISTS iceberg_jdbc.ecommerce")

spark.sql("SHOW SCHEMAS FROM iceberg_jdbc").show()

print("=== 1. Load Customers Data ===")

df_customers = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("s3a://dataset/ecommerce_order_dataset/train/df_Customers.csv")
df_customers.createOrReplaceTempView("customers_raw")
spark.sql("""CREATE OR REPLACE TABLE iceberg_jdbc.ecommerce.customers
USING iceberg
AS SELECT * FROM customers_raw;
""")
print("=== Check Customers Data ===")
df_check = spark.sql("select * from iceberg_jdbc.ecommerce.customers limit 5")
df_check.show()

print("=== 2. Load Orders Data ===")

df_orders = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("s3a://dataset/ecommerce_order_dataset/train/df_Orders.csv")
df_orders.createOrReplaceTempView("orders_raw")
spark.sql("""CREATE OR REPLACE TABLE iceberg_jdbc.ecommerce.orders
USING iceberg
AS SELECT * FROM orders_raw;
""")
print("=== Check Orders Data ===")
df_check = spark.sql("select * from iceberg_jdbc.ecommerce.orders limit 5")
df_check.show()

print("=== 3. Load Order Items Data ===")

df_order_items = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("s3a://dataset/ecommerce_order_dataset/train/df_OrderItems.csv")
df_order_items.createOrReplaceTempView("order_items_raw")
spark.sql("""CREATE OR REPLACE TABLE iceberg_jdbc.ecommerce.order_items
USING iceberg
AS SELECT * FROM order_items_raw;
""")
print("=== Check Order Items Data ===")
df_check = spark.sql("select * from iceberg_jdbc.ecommerce.order_items limit 5")
df_check.show()


print("=== 4. Load Payments Data ===")
df_payments = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("s3a://dataset/ecommerce_order_dataset/train/df_Payments.csv")
df_payments.createOrReplaceTempView("payments_raw")
spark.sql("""CREATE OR REPLACE TABLE iceberg_jdbc.ecommerce.payments
USING iceberg
AS SELECT * FROM payments_raw;
""")
print("=== Check Payments Data ===")
df_check = spark.sql("select * from iceberg_jdbc.ecommerce.payments limit 5")
df_check.show()

print("=== 5. Load Products Data ===")
df_products = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("s3a://dataset/ecommerce_order_dataset/train/df_Products.csv")
df_products.createOrReplaceTempView("products_raw")
spark.sql("""CREATE OR REPLACE TABLE iceberg_jdbc.ecommerce.products
USING iceberg
AS SELECT * FROM products_raw;
""")
print("=== Check Products Data ===")
df_check = spark.sql("select * from iceberg_jdbc.ecommerce.products limit 5")
df_check.show()
