# youtube-trending-analysis
This project is an ETL pipeline which analyzes YouTube trending video data from YouTube API, processing it with PySpark on Dataproc. Raw JSON data is ingested into GCS, transformed to extract metrics like video duration and growth rate, etc., and stored in BigQuery for analysis and tableau for visualization. The pipeline provides insights into video trends, leveraging scalable cloud infrastructure.

![a visual representation of the permissions flow between components](https://github.com/user-attachments/assets/da0c81d9-1950-4c5b-a03e-4b9d98cc767b)


## Overview
- Data is collected and stored in GCS buckets (`gs://youtube-trending-raw/raw/<country>/<timestamp>.json`).
- A PySpark script processes this data, calculates metrics like duration in minutes and growth rate, etc., and writes the results to BigQuery (`youtube_trending.trending_videos`).

## **Project Components**
The project consists of:
1. **Ingester VM**: Collects YouTube trending data and writes it as JSON files to Google Cloud Storage (GCS).
2. **Dataproc Cluster**: Processes raw data from GCS using PySpark and loads results into BigQuery.
3. **GCS Buckets**:
   - `gs://youtube-trending-raw`: Stores raw JSON data.
   - `gs://dataproc-staging-us-central1-13060018848-l3ei8og8`: Temporary staging bucket for Dataproc.
4. **BigQuery**: Stores processed data in the `youtube_trending.trending_videos` table.

## Running the Script
1. **Upload Script**: Upload `scripts/process_youtube.py` to your Dataproc cluster or a GCS bucket accessible by the cluster.
2. **Submit Job**: Use the Dataproc UI or `gcloud` command to submit the PySpark job.
