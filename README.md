# Movie Rating Analysis - Spark Project

This project analyzes movie rating datasets (MovieLens) to find average ratings per genre using Apache Spark. The project includes a web-based dashboard to visualize the analysis results.

## Project Structure

```
BGData/
├── docker-compose-spark.yml        # Spark cluster configuration (1 master + 2 workers)
├── docker-compose-frontend.yml     # Frontend web application
├── spark-apps/                     # Spark Python code
│   ├── movie_rating_analysis.py    # Genre rating analysis
│   └── top_movies_analysis.py     # Top rated movies analysis
├── frontend/                       # Web dashboard
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   ├── requirements.txt
│   └── Dockerfile
├── scripts/                        # Helper scripts
│   ├── download_data.sh            # Download MovieLens dataset
│   └── run_all_analyses.sh         # Run all analyses
└── data/                           # Dataset directory (created after download)
```

## Prerequisites

- Docker and Docker Compose installed
- At least 8GB RAM available
- Internet connection for downloading datasets

## Quick Setup


**WSL**
```bash
./setup.sh
```

This will automatically:
1. Download the dataset
2. Start Spark cluster
3. Start the frontend dashboard

## Manual Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd BGData
```

### 2. Download MovieLens Dataset

```bash
# Make scripts executable (Linux/Mac)
chmod +x scripts/*.sh

# Download dataset
./scripts/download_data.sh

# For Windows, you can manually download from:
# https://files.grouplens.org/datasets/movielens/ml-latest-small.zip
# Extract movies.csv and ratings.csv to the ./data directory
```

### 3. Start Spark Cluster

```bash
docker-compose -f docker-compose-spark.yml up -d
```

This will start:
- **Spark Master Node**
  - Web UI: http://localhost:8080

- **Spark Worker Nodes** (2 workers)
  - Worker 1 Web UI: http://localhost:8081
  - Worker 2 Web UI: http://localhost:8082

### 4. Start Frontend Dashboard

```bash
docker-compose -f docker-compose-frontend.yml up -d
```

Access the dashboard at: http://localhost:5000

## Running the Analysis

### Option 1: Run All Analyses

```bash
# Run both genre and top movies analyses
./scripts/run_all_analyses.sh
```

This will run:
1. **Genre Rating Analysis** - Average ratings per genre
2. **Top Movies Analysis** - Top 50 highest rated movies (min 50 ratings)

### Option 2: Run Individual Analyses

**Genre Analysis:**
```bash
./scripts/run_spark_job.sh
```

# Or manually:
```bash
docker exec spark-master /spark/bin/spark-submit \
    --master spark://spark-master:7077 \
    --executor-memory 2g \
    --driver-memory 1g \
    /spark-apps/movie_rating_analysis.py \
    /data/movies.csv \
    /data/ratings.csv \
    /data/spark_output
```

**Top Movies Analysis:**
```bash
docker exec spark-master /spark/bin/spark-submit \
    --master spark://spark-master:7077 \
    --executor-memory 2g \
    --driver-memory 1g \
    /spark-apps/top_movies_analysis.py \
    /data/movies.csv \
    /data/ratings.csv \
    /data/top_movies_output \
    50
```

Results will be available:
- Genre analysis: `/data/spark_output.json`
- Top movies: `/data/top_movies_output.json`

## Viewing Results

1. **Web Dashboard**: Open http://localhost:5000 in your browser
   - **Genre Analysis Tab**: View average ratings per genre with interactive charts
   - **Top Movies Tab**: View top rated movies with ratings and popularity metrics
   - Switch between analyses using the tabs at the top

2. **Spark Web UI**: http://localhost:8080
   - Monitor job execution
   - View application history
   - Check worker status

## Basic Commands Reference

### Spark Commands

```bash
# Submit Spark job
docker exec spark-master /spark/bin/spark-submit --master spark://spark-master:7077 /spark-apps/movie_rating_analysis.py /data/movies.csv /data/ratings.csv /data/spark_output

# Check Spark cluster status
docker exec spark-master /spark/bin/spark-shell --master spark://spark-master:7077

# View Spark logs
docker logs spark-master
docker logs spark-worker1
docker logs spark-worker2
```

### Docker Commands

```bash
# View running containers
docker ps

# View logs
docker logs spark-master
docker logs spark-worker1
docker logs spark-worker2
docker logs movie-rating-frontend

# Stop all services
docker-compose -f docker-compose-spark.yml down
docker-compose -f docker-compose-frontend.yml down

# Remove all containers and volumes
docker-compose -f docker-compose-spark.yml down -v
docker-compose -f docker-compose-frontend.yml down -v
```

## Project Requirements Checklist

✅ **Spark Setup**
- [x] One PC acting as Master Node (Docker container)
- [x] At least two PCs functioning as Worker Nodes (2 Docker containers)
- [x] Spark job for average ratings per genre
- [x] Spark job for top rated movies analysis

✅ **UI Interface**
- [x] Web-based dashboard using Flask and HTML/CSS/JavaScript
- [x] Displays multiple Spark analysis results
- [x] Tabbed interface for different analyses
- [x] Interactive charts and statistics for both analyses


## Architecture

```
┌─────────────────┐
│   Frontend UI   │ (Flask Dashboard)
│   Port: 5000    │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐
│ Spark │
│Master │
└───┬───┘
    │
┌───┴───┐
│Worker1│
│Worker2│
└───────┘
```

## Technologies Used

- **Apache Spark 3.0**: In-memory distributed data processing
- **Docker & Docker Compose**: Container orchestration
- **Flask**: Python web framework for API
- **HTML/CSS/JavaScript**: Frontend dashboard
- **Chart.js**: Data visualization
- **PySpark**: Python API for Spark
