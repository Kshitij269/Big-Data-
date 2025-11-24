#!/bin/bash

# Script to download MovieLens dataset
# This downloads a small sample dataset (100k ratings)

echo "Downloading MovieLens 100k dataset..."

DATA_DIR="./data"
mkdir -p $DATA_DIR

# Download MovieLens 100k dataset
cd $DATA_DIR

if [ ! -f "ml-latest-small.zip" ]; then
    echo "Downloading dataset..."
    wget https://files.grouplens.org/datasets/movielens/ml-latest-small.zip
    
    echo "Extracting dataset..."
    unzip ml-latest-small.zip
    
    # Copy required files
    cp ml-latest-small/movies.csv .
    cp ml-latest-small/ratings.csv .
    
    echo "Dataset downloaded and extracted successfully!"
    echo "Files available in: $DATA_DIR"
    echo "  - movies.csv"
    echo "  - ratings.csv"
else
    echo "Dataset already exists. Skipping download."
fi

cd ..



