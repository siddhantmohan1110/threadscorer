# threadscorer : A thread scoring engine for social media feeds

## Files in the repository

```main.py```: The main script to run the full data processing and analysis pipeline.

```generate_threads.py```: Module for generating the synthetic threads.csv dataset.

```score_threads.py```: Module containing the original and alternate scoring logic.

```sort_threads.py```: Module for sorting threads by score and extracting the top 10.

```multi_user.py```: Module for assigning simulated user IDs to each thread.

```multi_user_analysis.py```: Module for calculating per-user average scores and plotting the results.

```plot_threads.py```: Module for generating score vs. age and top 10 engagement plots.

```requirements.txt```: A file listing the Python packages required to run the project.

## Scoring functions

1. ```score = 2 * n_likes + 3 * n_replies + 2.5 * n_reposts * exp(-age_minutes / 120)```

This scoring function gives highest weightage to replies, followed by reposts and lastly by likes. The weightage given to reposts is decayed exponentially based on the age of the post (in minutes). This ensures that the value of the engagement metrics is tempered by the age of the thread. 

2. ```alternate_score = (np.log2((likes * 2) + 1) + np.log2((replies * 3) + 1) + np.log2((reposts * 2.5) + 1)) * np.exp(-age_minutes / decay_constant)```

This scoring function is used to simulate diminishing returns by using decaying all three engagements based on age of the post, in minutes.

## Installation and setup
1. Clone the repository locally and navigate to the directory.
```bash
git clone https://github.com/siddhantmohan1110/threadscorer.git
cd threadscorer
```

2. Create a virtual environment and activate it.
```bash 
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies within the environment.
```bash
pip install -r requirements.txt
``` 

## Running the threadscorer
1. To generate the dataset
```bash
python3 generate_threads.py
```

2. To score the dataset with both functions
```bash
python3 score_threads.py
```

3. To get the top 10 threads and their corresponding metadata
```bash
python3 sort_threads.py
```

4. To get the score v age scatter plot and the engagements of the top 10 threads.
```bash
python3 plot_threads.py
```

## Results

### From dataset generated using seed 42, with scoring function 1

![Score vs Age Scatter Plot](images/score_vs_age.png)

![Top 10 Engagements](images/top10_engagements.png)

### From dataset generated using seed 42, with scoring function 2

![Alternate Score vs Age Scatter Plot](images/alter_score_vs_age.png)

![Alternate Top 10 Engagements](images/alter_top10_engagements.png)

![Alternate User Score Distribution](images/alter_user_score_distribution.png)