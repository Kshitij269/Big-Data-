"""
Flask backend API for Movie Rating Analysis Dashboard
"""
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import json
import os
import csv

app = Flask(__name__)
CORS(app)

# Paths to result files
SPARK_OUTPUT_JSON = '/data/spark_output.json'
TOP_MOVIES_OUTPUT_JSON = '/data/top_movies_output.json'

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return render_template('index.html')

@app.route('/api/spark-results')
def get_spark_results():
    """Get results from Spark genre analysis"""
    try:
        if os.path.exists(SPARK_OUTPUT_JSON):
            with open(SPARK_OUTPUT_JSON, 'r') as f:
                data = json.load(f)
            return jsonify({
                'success': True,
                'data': data,
                'source': 'Spark',
                'type': 'genre_ratings'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Genre analysis results not found. Please run the Spark job first.',
                'data': []
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error reading Spark results: {str(e)}',
            'data': []
        })

@app.route('/api/top-movies')
def get_top_movies():
    """Get results from top movies analysis"""
    try:
        if os.path.exists(TOP_MOVIES_OUTPUT_JSON):
            with open(TOP_MOVIES_OUTPUT_JSON, 'r') as f:
                data = json.load(f)
            return jsonify({
                'success': True,
                'data': data,
                'source': 'Spark',
                'type': 'top_movies'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Top movies results not found. Please run the top movies analysis first.',
                'data': []
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error reading top movies results: {str(e)}',
            'data': []
        })


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'genre_results_exists': os.path.exists(SPARK_OUTPUT_JSON),
        'top_movies_results_exists': os.path.exists(TOP_MOVIES_OUTPUT_JSON)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

