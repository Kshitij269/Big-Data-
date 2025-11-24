# Quick Start Guide - Movie Rating Analysis

## Prerequisites
- Docker Desktop installed and running
- At least 8GB RAM available
- Internet connection

## Step-by-Step Setup

### 1. Download the Dataset

./scripts/download_data.sh
```

**Manual Download:**
1. Visit: https://files.grouplens.org/datasets/movielens/ml-latest-small.zip
2. Extract `movies.csv` and `ratings.csv` to `./data/` directory

### 2. Start Spark Cluster
docker-compose -f docker-compose-spark.yml up -d


Wait 30 seconds. Verify at:
- Spark Master: http://localhost:8080

### 3. Run Spark Analysis

./scripts/run_all_analyses.sh

### 4. Start Frontend Dashboard

docker-compose -f docker-compose-frontend.yml up -d

Access dashboard at: **http://localhost:5000**


## Verify Everything is Working

1. **Spark Cluster:**
   - http://localhost:8080 - Should show 2 workers

3. **Frontend:**
   - http://localhost:5000 - Should load dashboard

4. **Check Results:**
   ```bash
   # Spark results
   docker exec spark-master cat /data/spark_output.json
   ```