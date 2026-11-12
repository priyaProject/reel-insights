# 🎬 Reel Insights – Movie Analytics Dashboard

## 1. Project Overview

Reel Insights is a movie analytics project developed using Python, SQL, and Streamlit.

The project focuses on analysing movie data to discover insights about movie performance, genres, actors, ratings, budgets, revenue, and popularity.

An interactive Streamlit dashboard allows users to explore movie data through visualizations, filters, and predefined analytical queries.

## 2. Project Objectives

- Analyse movie performance based on budget, revenue, ratings, and popularity.
- Identify top-performing movies.
- Understand movie genre distribution and trends.
- Analyse actors based on their movie appearances.
- Explore movie release trends over the years.
- Compare movie budgets and revenue.
- Build an interactive analytics dashboard.

## 3. Dataset Overview

The project uses six related datasets.

| Dataset | Records |
|---|---:|
| Movies | 2,509 |
| Genres | 19 |
| Movie Genres | 6,888 |
| Cast | 24,917 |
| Crew | 7,297 |
| Movie Keywords | 41,701 |

## 4. Technologies Used

- Python
- Pandas
- NumPy
- SQLite
- SQL
- Plotly
- Streamlit
- Jupyter Notebook
- Visual Studio Code

## 5. Project Workflow

1. Data Loading
2. Data Exploration
3. Data Cleaning and Preprocessing
4. Data Validation
5. Exploratory Data Analysis (EDA)
6. SQL-Based Analysis
7. Data Visualization
8. Interactive Dashboard Development

## 6. Dashboard Features

### Dashboard

- Total Movies
- Total Genres
- Total Actors
- Average Movie Rating
- Top 10 Movies by Revenue
- Genre Distribution
- Budget vs Revenue Analysis
- Interactive Filters
- Downloadable Filtered Movie Data

### Query Explorer

- Predefined Analytical Queries
- Movie Revenue Analysis
- Movie Rating Analysis
- Popularity Analysis
- Movie Release Trends
- Genre-Based Analysis
- Top Actors by Movie Count
- Financial Summary
- Interactive Charts
- Downloadable Query Results

### Interactive Filters

- Genre
- Release Year
- Minimum Rating
- Minimum Votes
- Original Language

## 7. Project Structure

```text
reel_insights/
│
├── data/
│   ├── cast.csv
│   ├── crew.csv
│   ├── genres.csv
│   ├── movie_genres.csv
│   ├── movie_keywords.csv
│   └── movies.csv
│
├── 01_data_cleaning.ipynb
├── 02_sql_analysis.ipynb
├── 03_pandas_analysis.ipynb
├── 04_visualizations.ipynb
│
├── app.py
├── reel_insights.db
├── requirements.txt
├── README.md
└── .gitignore
```

## 8. Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/priyaProject/reel-insights.git
```

### Step 2: Navigate to the Project Folder

```bash
cd reel_insights
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 5: Install Required Libraries

```bash
pip install -r requirements.txt
```

### Step 6: Run the Streamlit Application

```bash
streamlit run app.py
```

## 9. Expected Outcome

Reel Insights provides an interactive platform for exploring movie datasets, identifying trends, comparing movie performance, and generating meaningful insights through data analysis and visualization.

## 10. Author

**Reel Insights – Movie Analytics Project**