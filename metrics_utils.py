"""
metrics_utils.py
Independent metrics utilities for Neuraluxe-AI.
"""
def accuracy(preds, labels):
    correct = sum(p==l for p, l in zip(preds, labels))
    return correct / len(labels) if labels else 0