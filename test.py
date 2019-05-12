import numpy as np
import joblib
xgb1 = joblib.load('xgb_inference.joblib')
print(xgb1.predict(np.ones((1, 15))))