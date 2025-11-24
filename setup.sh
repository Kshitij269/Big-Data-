#!/bin/bash

# Master setup script for Movie Rating Analysis Project

set -e

echo "=========================================="
echo "Movie Rating Analysis - Setup Script"
echo "=========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "Step 1: Downloading dataset..."
if [ ! -f "data/movies.csv" ] || [ ! -f "data/ratings.csv" ]; then
    chmod +x scripts/download_data.sh
    ./scripts/download_data.sh
else
    echo "Dataset already exists. Skipping download."
fi

echo ""
echo "Step 2: Starting Spark cluster..."
docker-compose -f docker-compose-spark.yml up -d

echo "Waiting for Spark to initialize (20 seconds)..."
sleep 20

echo ""
echo "Step 3: Starting frontend dashboard..."
docker-compose -f docker-compose-frontend.yml up -d

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Access points:"
echo "  - Spark Master:           http://localhost:8080"
echo "  - Frontend Dashboard:     http://localhost:5000"
echo ""
echo "Next steps:"
echo "  1. Run Spark analysis:    ./scripts/run_spark_job.sh"
echo "  2. View results:          http://localhost:5000"
echo ""

