## IAM Roles and Permissions

This section outlines the final IAM roles and policies required for the **YouTube Trending Analyzer** project, detailing what each component needs to function correctly.

### **IAM Roles**

#### **1. Ingester VM**
- **Purpose**: Writes JSON files to `gs://youtube-trending-raw`.
- **Required Permission**:
  - `storage.objects.create`: Allows creating new objects in the GCS bucket.
- **IAM Role**:
  - `Storage Object Creator`: Includes `storage.objects.create`.
- **Service Account**:
  - Attached to the Ingester VM’s service account (e.g., Compute Engine default or custom).

#### **2. Dataproc Cluster**
- **Purpose**: Reads from `gs://youtube-trending-raw`, writes to the staging bucket, and loads data into BigQuery.
- **Required Permissions**:
  - **For GCS (`gs://youtube-trending-raw`)**:
    - `storage.objects.get`: To read JSON files.
  - **For GCS (`gs://dataproc-staging-us-central1-13060018848-l3ei8og8`)**:
    - `storage.objects.create`: To write temporary files.
  - **For BigQuery (`youtube_trending.trending_videos`)**:
    - `bigquery.tables.create`: To create the table if it doesn’t exist.
    - `bigquery.tables.updateData`: To insert or update data.
- **IAM Roles**:
  - `Storage Object Viewer`: Grants `storage.objects.get` for reading raw data.
  - `Storage Object Creator`: Grants `storage.objects.create` for the staging bucket.
  - `BigQuery Data Editor`: Grants `bigquery.tables.create` and `bigquery.tables.updateData`.
- **Service Account**:
  - Attached to the Dataproc cluster’s service account.
