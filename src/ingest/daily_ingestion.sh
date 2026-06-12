#!/bin/bash

export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8

echo "=== Pipeline Start ==="

~/.local/bin/kaggle kernels output jeongjaeahn/notebook4e2d36e53e -p /home/maria_dev/raw_data

FILES=$(find /home/maria_dev/raw_data -name "ecommerce_apparel_*.csv")

if [ -z "$FILES" ]; then
    echo "Error: No CSV files downloaded!"
else
    for file in $FILES; do
        DATE=$(echo $file | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')

        hdfs dfs -mkdir -p /user/maria_dev/fashion/dt=$DATE
        hdfs dfs -put -f $file /user/maria_dev/fashion/dt=$DATE/

        echo "[$DATE] Uploaded to HDFS"

        rm -f $file
    done
fi

echo "=== Pipeline End ==="
