#!/bin/bash

# Hadoop Streaming JAR
HADOOP_STREAMING_JAR=/opt/hadoop-2.7.4/share/hadoop/tools/lib/hadoop-streaming-2.7.4.jar

# HDFS directories
INPUT_DIR=/user/root/input_trends
OUTPUT_DIR=/user/root/output_trends

# Local dataset path
LOCAL_DATASET=/root/Trending_hastag/dataset/hashtags.csv

# Remove previous output
echo "Removing previous output (if any)..."
hdfs dfs -rm -r -f $OUTPUT_DIR

# Create HDFS input directory
echo "Creating HDFS input dir..."
hdfs dfs -mkdir -p $INPUT_DIR

# Upload dataset to HDFS
echo "Uploading dataset to HDFS..."
hdfs dfs -put -f $LOCAL_DATASET $INPUT_DIR

# Run Hadoop Streaming job
echo "Running Hadoop Streaming job..."
hadoop jar $HADOOP_STREAMING_JAR \
    -input $INPUT_DIR \
    -output $OUTPUT_DIR \
    -mapper mapper.py \
    -reducer reducer.py \
    -files /root/Trending_hastag/mapper.py,/root/Trending_hastag/reducer.py

# Display top trending hashtags
echo "Job completed. Top trending hashtags:"
hdfs dfs -cat $OUTPUT_DIR/part-00000 | sort -k2 -nr | head -10
