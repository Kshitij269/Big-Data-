"""
Spark Job to analyze movie ratings and calculate average ratings per genre
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, explode, avg, count, round as spark_round
import sys

def main():
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("MovieRatingAnalysis") \
        .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    
    # Read movies data (movieId, title, genres)
    # Format: movieId,title,genres (genres are pipe-separated)
    movies_path = sys.argv[1] if len(sys.argv) > 1 else "/data/movies.csv"
    ratings_path = sys.argv[2] if len(sys.argv) > 2 else "/data/ratings.csv"
    output_path = sys.argv[3] if len(sys.argv) > 3 else "/data/spark_output"
    
    print("Reading movies from: {}".format(movies_path))
    print("Reading ratings from: {}".format(ratings_path))
    print("Output will be written to: {}".format(output_path))
    
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
        
        # Split genres and explode (one row per genre per movie)
        movies_with_genres = movies_df \
            .withColumn("genre", explode(split(col("genres"), "\\|"))) \
            .select("movieId", "title", "genre")
        
        # Filter out "(no genres listed)"
        movies_with_genres = movies_with_genres.filter(col("genre") != "(no genres listed)")
        
        # Join with ratings
        movie_ratings = movies_with_genres.join(
            ratings_df.select("movieId", "rating"),
            on="movieId",
            how="inner"
        )
        
        # Calculate average rating per genre
        genre_ratings = movie_ratings \
            .groupBy("genre") \
            .agg(
                spark_round(avg("rating"), 2).alias("average_rating"),
                count("rating").alias("total_ratings")
            ) \
            .orderBy(col("average_rating").desc())
        
        # Show results
        print("\n=== Average Ratings per Genre ===")
        genre_ratings.show(truncate=False)
        
        # Write results to output
        genre_ratings.coalesce(1).write \
            .mode("overwrite") \
            .option("header", "true") \
            .csv(output_path)
        
        print("\nResults written to: {}".format(output_path))
        
        # Collect results for JSON output (for API)
        results = genre_ratings.collect()
        results_dict = [
            {
                "genre": row["genre"],
                "average_rating": float(row["average_rating"]),
                "total_ratings": int(row["total_ratings"])
            }
            for row in results
        ]
        
        # Write JSON output
        import json
        json_output_path = output_path.replace("/data/spark_output", "/data/spark_output.json")
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

