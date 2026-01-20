import pandas as pd
import numpy as np

def detect_spike(series, window=7):
    """
    Spike = value > rolling_mean + 3 * rolling_std
    """
    rolling_mean = series.rolling(window).mean()
    rolling_std = series.rolling(window).std()

    threshold = rolling_mean + 3 * rolling_std
    spike = series > threshold

    return spike, threshold
