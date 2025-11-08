#!/usr/bin/env python3
"""
reducer.py
Aggregates 'hashtag<TAB>mentions' lines from stdin and prints:
hashtag<TAB>total_mentions
"""
import sys

current_hashtag = None
current_total = 0

def flush():
    global current_hashtag, current_total
    if current_hashtag is not None:
        print(f"{current_hashtag}\t{current_total}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) != 2:
        continue
    hashtag, mentions_s = parts
    try:
        mentions = int(mentions_s)
    except Exception:
        mentions = 0

    if current_hashtag == hashtag:
        current_total += mentions
    else:
        # output previous
        flush()
        current_hashtag = hashtag
        current_total = mentions

# final flush
flush()
