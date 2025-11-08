#!/usr/bin/env python3
"""
mapper.py
Reads CSV rows from stdin and emits:
hashtag<TAB>mentions

Expected CSV header:
date,hashtag,mentions,estimated_reach,sentiment_score,top_country
"""
import sys
import csv

def safe_int(x):
    try:
        return int(x)
    except Exception:
        return 0

reader = csv.DictReader(sys.stdin)
for row in reader:
    # Basic validation
    hashtag = (row.get("hashtag") or "").strip()
    mentions = safe_int((row.get("mentions") or "").strip())
    if not hashtag:
        continue
    # Emit key-value pair for reducer
    print(f"{hashtag}\t{mentions}")
