# youtube-trending-analysis
This project analyzes YouTube trending video data from YouTube API, processing it with PySpark on Dataproc. Raw JSON data is ingested into GCS, transformed to extract metrics like video duration and growth rate, etc., and stored in BigQuery for analysis. The pipeline provides insights into video trends, leveraging scalable cloud infrastructure.

## Overview
- Data is collected and stored in GCS buckets (`gs://youtube-trending-raw/raw/<country>/<timestamp>.json`).
- A PySpark script processes this data, calculates metrics like duration in minutes and growth rate, etc., and writes the results to BigQuery (`youtube_trending.trending_videos`).

## Setup
1. **Google Cloud Project**: Ensure you have a Google Cloud project with billing enabled.
2. **GCS Buckets**: Create the necessary GCS buckets:
   - `gs://youtube-trending-raw` for raw data.
   - `gs://dataproc-staging-us-central1-13060018848-l3ei8og8` for Dataproc staging.
3. **BigQuery Dataset**: Create a BigQuery dataset named `youtube_trending`.
4. **IAM Permissions**: Set up IAM roles as detailed in `/docs/iam_rules.md`.
5. **Dataproc Cluster**: Create a Dataproc cluster to run the PySpark job.

## Running the Script
1. **Upload Script**: Upload `scripts/process_youtube.py` to your Dataproc cluster or a GCS bucket accessible by the cluster.
2. **Submit Job**: Use the Dataproc UI or `gcloud` command to submit the PySpark job:
   ```bash
   gcloud dataproc jobs submit pyspark \
       --cluster=<cluster-name> \
       --region=<region> \
       gs://<path-to-script>/process_youtube.py
