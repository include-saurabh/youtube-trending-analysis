from pyspark.sql import SparkSession
from pyspark.sql.functions import col, unix_timestamp, explode, regexp_extract, expr, input_file_name, coalesce, lit

# Start Spark session
spark = SparkSession.builder \
    .appName("YouTubeTrendingAnalyzer") \
    .getOrCreate()

# Read JSON data
raw_data = spark.read.json("gs://youtube-trending-raw/raw/*/*.json")

# Explode the items array
raw_data_exploded = raw_data.select(
    explode(col("items")).alias("item"),
    input_file_name().alias("file_path"),
    regexp_extract(input_file_name(), r"raw/([A-Z]{2})/", 1).alias("country")
)

# Process data with duration in minutes (with decimals)
videos = raw_data_exploded.select(
    col("item.id").alias("video_id"),
    col("item.snippet.title").alias("title"),
    col("item.snippet.categoryId").alias("category_id"),
    col("item.snippet.categoryName").alias("category"),
    col("item.statistics.viewCount").cast("long").alias("views"),
    col("item.statistics.likeCount").cast("long").alias("likes"),
    col("item.statistics.commentCount").cast("long").alias("comments"),
    (coalesce(regexp_extract(col("item.contentDetails.duration"), r"PT(\d+)H", 1).cast("float"), lit(0)) * 60 +
     coalesce(regexp_extract(col("item.contentDetails.duration"), r"PT.*?(\d+)M", 1).cast("float"), lit(0)) +
     coalesce(regexp_extract(col("item.contentDetails.duration"), r"PT.*?(\d+)S", 1).cast("float"), lit(0)) / 60
    ).alias("duration_minutes"),
    unix_timestamp(col("item.snippet.publishedAt"), "yyyy-MM-dd'T'HH:mm:ss'Z'").alias("publish_timestamp"),
    col("country")
)

# Calculate growth rate
videos_with_growth = videos.withColumn(
    "growth_rate",
    expr("views / NULLIF(unix_timestamp() - publish_timestamp, 0)")
)

# Write to BigQuery
videos_with_growth.write \
    .mode("overwrite") \
    .format("bigquery") \
    .option("table", "youtube_trending.trending_videos") \
    .option("temporaryGcsBucket", "dataproc-staging-us-central1-13060018848-l3ei8og8") \
    .save()

# Clean up
spark.stop()