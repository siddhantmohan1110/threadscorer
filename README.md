# threadscorer : A thread scoring engine for social media feeds

## Files in the repository

- `main.py`: The main script to run the full data processing and analysis pipeline.
- `generate_threads.py`: Module for generating the synthetic threads.csv dataset, now including likes, dislikes, replies, reposts, other interactions, cursory and engaged views, and age.
- `score_normalized.py`: Module for calculating the Normalized Trending Post Score, fully parameterized for weights.
- `score_time_weighted.py`: Module for calculating the Time-Weighted Trending Post Score, with adjustable decay constant.
- `score_category_topic_asset.py`: Module for calculating trending scores for categories, topics, and assets.
- `score_threads.py`: Module containing the original and alternate scoring logic.
- `sort_threads.py`: Module for sorting threads by score and extracting the top 10.
- `multi_user.py`: Module for assigning simulated user IDs to each thread.
- `multi_user_analysis.py`: Module for calculating per-user average scores and plotting the results.
- `plot_threads.py`: Module for generating score vs. age and top 10 engagement plots.
- `requirements.txt`: A file listing the Python packages required to run the project.
- `app.py`: FastAPI web app for interactive demo (see below).

## Scoring functions

### 1. Normalized Trending Post Score

This score uses a weighted sum of shares, other interactions, comments, likes, dislikes, and views, normalized by the total interactions. All weights and parameters are easily adjustable.

### 2. Time-Weighted Trending Post Score

This score applies an exponential decay to the normalized score over time periods (e.g., days), allowing recent activity to have more influence. The decay constant is fully parameterized.

### 3. Trending Category/Topic/Asset Score

These scores aggregate the normalized or time-weighted scores for all posts in a given category, topic, or asset.

### 4. Original and Alternate Scores

Legacy scoring functions are also included for comparison.

## Web App Demo

A FastAPI web app (`app.py`) is included for interactive demonstration.  
- The app generates a fixed set of synthetic threads (using a constant random seed).
- Users can adjust all weights and the decay constant via a web panel.
- The app instantly recalculates and displays all scores (original, alternate, normalized, and time-weighted) for each thread.

---

## Installation and Setup

### 1. Clone the repository and navigate to the directory
```bash
git clone https://github.com/siddhantmohan1110/threadscorer.git
cd threadscorer
```

### 2. Create a virtual environment and activate it
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Data Pipeline

To run the full data pipeline and generate all outputs:
```bash
python main.py
```

---

## Running the FastAPI Backend

To launch the interactive demo API:
```bash
uvicorn app:app --reload
```
- Open your browser and go to [http://localhost:8000/docs](http://localhost:8000/docs) for the API documentation and testing.
- The `/scores` endpoint accepts POST requests with weights and decay constant, and returns all thread scores in JSON format.

---

## Running the Frontend (Optional)

A sample frontend is provided in a separate folder (e.g., `threadscorer-frontend/`).  
To run the frontend:

1. Navigate to the frontend directory:
   ```bash
   cd threadscorer-frontend
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Start the frontend development server:
   ```bash
   npm run dev
   ```
   - Open the URL shown in your terminal (usually [http://localhost:5173](http://localhost:5173)).

**Note:** The frontend expects the FastAPI backend to be running at `http://localhost:8000`.

---

## Notes

- All scoring weights and parameters are easily adjustable in both the pipeline and the web app, making this project ready for integration with an admin panel or further web development.
- The synthetic data is generated with a fixed random seed for reproducibility in demos.

---

*For more details on the scoring algorithms, see `Trend Post Score.md`.*