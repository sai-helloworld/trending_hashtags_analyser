🧠 Social Media Trend Tracker
📊 A Big Data Analytics Project

The Social Media Trend Tracker is a Python-based analytical tool that processes social media hashtag data to identify and rank trending topics across different time windows (day, week, month).
It reads structured CSV data, aggregates key engagement metrics, computes a trend score, and outputs the top trending hashtags for each period — all locally, without needing online APIs.

🚀 Features

✅ Reads and preprocesses hashtag data from a CSV file

✅ Supports multiple time windows — day, week, month

✅ Aggregates mentions, estimated reach, and sentiment

✅ Computes custom Trend Scores based on:

Trend Score
=
Growth
×
log
⁡
(
Reach
+
1
)
×
(
1
+
Sentiment
)
Trend Score=Growth×log(Reach+1)×(1+Sentiment)

✅ Generates output CSVs:

*_agg_counts.csv – aggregated metrics

*_trend_scores.csv – computed trend scores

*_topk_per_window.csv – top-K hashtags per window

✅ Works fully offline — no API or internet dependency

🧩 Project Structure
├── trend_tracker_local.py        # Main project script
├── sample_posts.csv              # Example dataset (user provided)
├── README.md                     # Project documentation
└── output_*.csv                  # Generated result files

🧠 How It Works

Data Input:
The tool reads a CSV file containing columns:
date, hashtag, mentions, estimated_reach, sentiment_score, top_country.

Preprocessing:

Parses multiple date formats (DD-MM-YYYY, YYYY-MM-DD, etc.)

Handles missing or invalid numeric values

Aggregation:

Groups data by hashtag and time window

Computes total mentions, total reach, and average sentiment

Trend Scoring:

Calculates growth compared to previous window

Computes trend score based on growth × log(reach) × sentiment

Top-K Extraction:

Identifies top trending hashtags for each window

⚙️ Installation
1️⃣ Clone the Repository
git clone [https://github.com/<your-username>/social-media-trend-tracker](https://github.com/sai-helloworld/trending_hashtags_analyser).git
cd social-media-trend-tracker

2️⃣ Install Dependencies
pip install pandas numpy

💻 Usage
Run the Tracker
python trend_tracker_local.py --input sample_posts.csv --window week --topk 10 --out_prefix results

Command-Line Arguments
Argument	Description	Default
--input, -i	Input CSV file path	required
--window, -w	Time window: day, week, or month	day
--topk, -k	Number of top hashtags per window	10
--out_prefix, -o	Output file prefix	output
📂 Example Outputs

After running the script, you’ll get:

results_agg_counts.csv → Aggregated data per hashtag

results_trend_scores.csv → Trend scores with growth info

results_topk_per_window.csv → Top-K trending hashtags per window

🧪 Sample Run Output
Reading CSV: sample_posts.csv
Wrote aggregated counts to: results_agg_counts.csv
Wrote trend scores to: results_trend_scores.csv
Wrote top-K per window to: results_topk_per_window.csv

Top results (first 20 rows):
 window     hashtag     score  mentions  reach  sentiment  rows_count
 2025-W17   #AI         5.712     200     5000     0.85        12
 2025-W17   #Data       4.321     180     4200     0.77        10
 ...
Done.

🧰 Technologies Used

Python 3.8+

Pandas – Data manipulation

NumPy – Numerical operations

Matplotlib / Excel (optional) – Visualization

📈 Future Enhancements

Integration with live APIs (e.g., Twitter/X API, Reddit)

Trend prediction using time-series forecasting (ARIMA, Prophet)

Interactive dashboards using Plotly or Streamlit

Geographical trend visualization

🧑‍💻 Contributors

Middela Sai Pavan — Project Developer

Vardhaman College of Engineering

Big Data Analytics Project — 2025

📚 References (IEEE Format)

[1] A. Gandomi and M. Haider, “Beyond the hype: Big data concepts, methods, and analytics,” Int. J. Inf. Manage., vol. 35, no. 2, pp. 137–144, 2015.
[2] H. Liang et al., “Detecting emerging trends on social media using time-series analytics,” IEEE Access, vol. 8, pp. 128942–128953, 2020.
[3] The pandas development team, pandas-dev/pandas: Pandas 2.0.3. Zenodo, 2023.
[4] NumPy Developers, NumPy Documentation, 2023.
[5] McKinsey & Co., “Harnessing the power of social media analytics,” McKinsey Digital Report, 2023.

📜 License

This project is licensed under the MIT License – you are free to use, modify, and distribute it with attribution.
