from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("Fashion_Weather_Join_Pipeline") \
    .getOrCreate()

print("=== Spark Application Started ===")

fashion_df = spark.read.option("header", "true") \
    .csv("/user/maria_dev/fashion/")

weather_df = spark.read.option("header", "true") \
    .csv("/user/maria_dev/weather/")

fashion_clean = fashion_df.select(
    col("event_time"),
    col("event_type"),
    col("product_id"),
    col("category_code"),
    col("price").cast("float"),
    col("user_id"),
    col("dt")
).dropna(subset=["category_code", "price"])

weather_clean = weather_df.select(
    col("date"),
    col("avg_temp").cast("float"),
    col("rainfall").cast("float")
)

joined_df = fashion_clean.join(
    weather_clean,
    fashion_clean.dt == weather_clean.date,
    "inner"
).drop("date")

joined_df.write.mode("overwrite").parquet("/user/maria_dev/processed_data/")

print("=== Spark Preprocessing & Join Successfully Completed ===")
spark.stop()
