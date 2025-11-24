"""
Spark Job to analyze top rated movies from MovieLens dataset
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, round as spark_round, desc
import sys

def main():
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("TopMoviesAnalysis") \
        .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    
    # Read movies and ratings data
    movies_path = sys.argv[1] if len(sys.argv) > 1 else "/data/movies.csv"
    ratings_path = sys.argv[2] if len(sys.argv) > 2 else "/data/ratings.csv"
    output_path = sys.argv[3] if len(sys.argv) > 3 else "/data/top_movies_output"
    min_ratings = int(sys.argv[4]) if len(sys.argv) > 4 else 50  # Minimum ratings threshold
    
    print("Reading movies from: {}".format(movies_path))
    print("Reading ratings from: {}".format(ratings_path))
    print("Output will be written to: {}".format(output_path))
    print("Minimum ratings threshold: {}".format(min_ratings))
    
    try:
        # Read CSV files
        movies_df = spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv(movies_path)
        
        ratings_df = spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv(ratings_path)
        
        # Calculate average rating and count per movie
        movie_stats = ratings_df \
            .groupBy("movieId") \
            .agg(
                spark_round(avg("rating"), 2).alias("average_rating"),
                count("rating").alias("total_ratings")
            ) \
            .filter(col("total_ratings") >= min_ratings)  # Filter movies with minimum ratings
        
        # Join with movies to get titles
        top_movies = movies_df.join(
            movie_stats,
            on="movieId",
            how="inner"
        ) \
        .select("movieId", "title", "genres", "average_rating", "total_ratings") \
        .orderBy(desc("average_rating"), desc("total_ratings")) \
        .limit(50)  # Top 50 movies
        
        # Show results
        print("\n=== Top Rated Movies (min {} ratings) ===".format(min_ratings))
        top_movies.show(truncate=False)
        
        # Write results to output
        top_movies.coalesce(1).write \
            .mode("overwrite") \
            .option("header", "true") \
            .csv(output_path)
        
        print("\nResults written to: {}".format(output_path))
        
        # Collect results for JSON output (for API)
        results = top_movies.collect()
        results_dict = [
            {
                "movieId": int(row["movieId"]),
                "title": row["title"],
                "genres": row["genres"],
                "average_rating": float(row["average_rating"]),
                "total_ratings": int(row["total_ratings"])
            }
            for row in results
        ]
        
        # Write JSON output
        import json
        json_output_path = output_path.replace("/data/top_movies_output", "/data/top_movies_output.json")
        with open(json_output_path, 'w') as f:
            json.dump(results_dict, f, indent=2)
        
        print("JSON results written to: {}".format(json_output_path))
        
    except Exception as e:
        print("Error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        spark.stop()

if __name__ == "__main__":
    main()

