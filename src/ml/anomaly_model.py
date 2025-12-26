import numpy as np
from sklearn.ensemble import IsolationForest

def detect_numeric_anomaly(values):
    values = np.array(values).reshape(-1, 1)
    model = IsolationForest(contamination=0.1)
    predictions = model.fit_predict(values)
    return [i for i, p in enumerate(predictions) if p == -1]