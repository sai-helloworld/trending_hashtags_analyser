#!/usr/bin/env python3
"""
trend_tracker_local.py

End-to-end local Social Media Trend Tracker:
- Reads CSV with columns: date,hashtag,mentions,estimated_reach,sentiment_score,top_country
  Date format expected: DD-MM-YYYY (e.g. 01-05-2025)
- Preprocesses, creates time windows (day/week/month)
- Aggregates metrics per hashtag x window
- Computes trend scores (growth * log(reach+1) * (1 + sentiment))
- Produces `agg_counts.csv`, `trend_scores.csv`, `topk_per_window.csv`

Usage:
    pip install pandas
    python trend_tracker_local.py --input sample_posts.csv --window day --topk 10
"""

import argparse
import pandas as pd
import numpy as np
from datetime import datetime
import math

def parse_args():
    p = argparse.ArgumentParser(description="Local Social Media Trend Tracker")
    p.add_argument("--input", "-i", required=True, help="Input CSV file")
    p.add_argument("--window", "-w", choices=["day","week","month"], default="day",
                   help="Time window aggregation (day/week/month). Default: day")
    p.add_argument("--topk", "-k", type=int, default=10, help="Top-K per window. Default: 10")
    p.add_argument("--out_prefix", "-o", default="output", help="Output files prefix (default: output)")
    return p.parse_args()

def to_datetime_col(df, date_col="date"):
    # Accepts DD-MM-YYYY, tries to parse common variants
    def try_parse(x):
        for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y"):
            try:
                return datetime.strptime(x.strip(), fmt)
            except Exception:
                continue
        raise ValueError(f"Unrecognized date format: {x}")
    return pd.to_datetime(df[date_col].astype(str).map(try_parse))

def make_window_col(dt_series, window):
    if window == "day":
        return dt_series.dt.strftime("%Y-%m-%d")
    elif window == "week":
        # ISO week number with year (YYYY-Www)
        return dt_series.dt.strftime("%G-W%V")  # ISO year-week
    elif window == "month":
        return dt_series.dt.strftime("%Y-%m")
    else:
        raise ValueError("Invalid window")

def aggregate(df, window_col):
    # Group by hashtag & window: sum mentions, sum reach, avg sentiment (weighted by count)
    agg = df.groupby(["hashtag", window_col], as_index=False).agg(
        mentions_sum = ("mentions", "sum"),
        reach_sum = ("estimated_reach", "sum"),
        sentiment_avg = ("sentiment_score", "mean"),
        rows_count = ("hashtag", "count")
    )
    agg = agg.rename(columns={window_col: "window"})
    return agg

def compute_trend_scores(agg_df):
    # For each hashtag, sort windows in chronological order -> compute growth & score
    # First need an ordering key for windows to sort chronologically.
    # We'll convert window strings back to dates for ordering where possible.
    def window_to_sortkey(w):
        try:
            # day: YYYY-MM-DD, month: YYYY-MM, week: YYYY-Www
            if len(w) == 10:  # YYYY-MM-DD
                return datetime.strptime(w, "%Y-%m-%d")
            if "-W" in w:  # YYYY-Www
                return pd.to_datetime(w + "-1", format="%G-W%V-%u")  # convert week to date (Mon)
            if len(w) == 7:  # YYYY-MM
                return datetime.strptime(w, "%Y-%m")
        except Exception:
            pass
        return datetime.min

    rows = []
    for h, group in agg_df.groupby("hashtag"):
        g = group.copy()
        # compute sort key
        g["_sort"] = g["window"].map(window_to_sortkey)
        g = g.sort_values("_sort")
        prev_mentions = None
        for _, r in g.iterrows():
            mentions = int(r["mentions_sum"])
            reach = int(r["reach_sum"])
            sentiment = float(r["sentiment_avg"]) if not pd.isna(r["sentiment_avg"]) else 0.0
            # growth relative to previous window
            if prev_mentions is None:
                growth = 0.0
            else:
                growth = (mentions - prev_mentions) / (prev_mentions + 1.0)
            # score formula: growth * log(reach+1) * (1 + sentiment)
            try:
                score = growth * math.log(reach + 1.0) * (1.0 + sentiment)
            except Exception:
                score = growth
            if math.isnan(score) or math.isinf(score):
                score = growth
            rows.append({
                "hashtag": h,
                "window": r["window"],
                "score": score,
                "mentions": mentions,
                "reach": reach,
                "sentiment": sentiment,
                "rows_count": int(r["rows_count"])
            })
            prev_mentions = mentions
    trend_df = pd.DataFrame(rows)
    # ensure deterministic ordering
    trend_df = trend_df.sort_values(["window", "score"], ascending=[True, False]).reset_index(drop=True)
    return trend_df

def topk_per_window(trend_df, k):
    out_rows = []
    for w, g in trend_df.groupby("window"):
        topk = g.sort_values("score", ascending=False).head(k)
        for _, r in topk.iterrows():
            out_rows.append({
                "window": w,
                "hashtag": r["hashtag"],
                "score": r["score"],
                "mentions": int(r["mentions"]),
                "reach": int(r["reach"]),
                "sentiment": float(r["sentiment"]),
                "rows_count": int(r["rows_count"])
            })
    topk_df = pd.DataFrame(out_rows)
    topk_df = topk_df.sort_values(["window","score"], ascending=[True, False]).reset_index(drop=True)
    return topk_df

def main():
    args = parse_args()
    print("Reading CSV:", args.input)
    df = pd.read_csv(args.input, dtype={"hashtag":str})
    # basic cleanup of expected columns
    expected_cols = ["date","hashtag","mentions","estimated_reach","sentiment_score"]
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise SystemExit(f"Missing columns in input CSV: {missing}")
    # parse date
    df["__dt"] = to_datetime_col(df, date_col="date")
    df["mentions"] = pd.to_numeric(df["mentions"], errors="coerce").fillna(0).astype(int)
    df["estimated_reach"] = pd.to_numeric(df["estimated_reach"], errors="coerce").fillna(0).astype(int)
    df["sentiment_score"] = pd.to_numeric(df["sentiment_score"], errors="coerce").fillna(0.0).astype(float)
    # window column
    df["window"] = make_window_col(df["__dt"], args.window)
    # aggregate
    agg_df = aggregate(df, "window")
    agg_out = f"{args.out_prefix}_agg_counts.csv"
    agg_df.to_csv(agg_out, index=False)
    print("Wrote aggregated counts to:", agg_out)
    # trend scores
    trend_df = compute_trend_scores(agg_df)
    trend_out = f"{args.out_prefix}_trend_scores.csv"
    trend_df.to_csv(trend_out, index=False)
    print("Wrote trend scores to:", trend_out)
    # top-k per window
    topk_df = topk_per_window(trend_df, args.topk)
    topk_out = f"{args.out_prefix}_topk_per_window.csv"
    topk_df.to_csv(topk_out, index=False)
    print("Wrote top-K per window to:", topk_out)
    # print summary of top results to console (for quick check)
    print("\nTop results (first 20 rows):")
    print(topk_df.head(20).to_string(index=False))
    print("\nDone.")

if __name__ == "__main__":
    main()
