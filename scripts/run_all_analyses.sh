#!/bin/bash

# Script to run all Spark analyses

echo "=========================================="
echo "Running All Spark Analyses"
echo "=========================================="
echo ""

# Run genre analysis
echo "1. Running Genre Rating Analysis..."
docker exec spark-master /spark/bin/spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    --executor-memory 2g \
    --driver-memory 1g \
    /spark-apps/movie_rating_analysis.py \
    /data/movies.csv \
    /data/ratings.csv \
    /data/spark_output

echo ""
echo "2. Running Top Movies Analysis..."
docker exec spark-master /spark/bin/spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    --executor-memory 2g \
    --driver-memory 1g \
    /spark-apps/top_movies_analysis.py \
    /data/movies.csv \
    /data/ratings.csv \
    /data/top_movies_output \
    50

echo ""
echo "=========================================="
echo "All analyses completed!"
echo "=========================================="
echo ""
echo "Results available:"
echo "  - Genre ratings: /data/spark_output.json"
echo "  - Top movies: /data/top_movies_output.json"

