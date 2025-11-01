"""
csv_utils.py
Independent CSV utilities for Neuraluxe-AI.
"""
import csv

def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.reader(f))

def write_csv(path, data):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)