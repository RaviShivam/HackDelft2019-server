import pandas as pd
import joblib

import numpy as np
from datetime import datetime as dtt
from forex_python.converter import CurrencyRates
from collections import Counter
from imblearn.over_sampling import RandomOverSampler
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from xgboost import XGBRegressor 
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

df = pd.read_excel('train_data/Hackatondata.xls')

cols =['declaratie_nr', 'decl_datum_invoer', 'decl_datum_ingediend', 'huidig_declaratie_omschrijving', 
       'log_reden_wijziging', 'dde_omschrijving']
cols_dataset = ['declaratie_nr', 'decl_datum_invoer', 'decl_datum_ingediend', 'decl_valuta_code','decl_verw_bedr_val_vreem',
                'decl_verwacht_bedrag', 'dde_omschrijving', 'huidig_declaratie_status']
data = df[cols_dataset].drop_duplicates('declaratie_nr', keep='last')

data.decl_valuta_code.fillna(inplace=True, value='EUR')

mask = data.decl_verw_bedr_val_vreem.isna()
data.decl_verw_bedr_val_vreem[mask] = data.decl_verwacht_bedrag[mask].copy()

data.columns = ['ID', 'DatumInvoer', 'DatumIngediend', 'Valuta', 'BedragVreemd', 'BedragVerwacht', 'Categorie', 'Status']

data = data.dropna()

# types
data.DatumInvoer = pd.to_datetime(data.DatumInvoer)
data.DatumIngediend = pd.to_datetime(data.DatumIngediend)
data.Status = data.Status.astype(int)

a = list(data.Valuta.value_counts().head().index)
vmap = {'Parkeerkosten': 'Parking', 'Hotelkosten': 'Hotel', 'VOG / uittreksel GBA overig': 'VOG', 'Opleidingskosten': 'Certificatescosts', 'Reiskosten YP': 'Travelcosts'}

for i, r in data.iterrows():
    v = r['Categorie'] 
    v2 = r['Valuta']
    data.at[i, 'Categorie'] = vmap[v] if v in vmap else 'Other'
    data.at[i, 'Valuta'] = v2 if v2 in a else 'Other'

def useful(x):
    if x == 90:
        return True
    elif x > 90:
        return False
    else:
        return np.nan


data['Label'] = data.Status.apply(useful)

data = data.dropna(subset=['Label'])

data['DateDiff'] = (data.DatumIngediend - data.DatumInvoer).apply(lambda x: x.days)

data = data.drop(columns=['ID', 'Status', 'DatumInvoer', 'DatumIngediend'])

combined = pd.concat([data[['BedragVreemd', 'BedragVerwacht', 'Label', 'DateDiff']], pd.get_dummies(data.Valuta), 
           pd.get_dummies(data.Categorie)], axis=1)

y = combined.Label.astype(int)
X = combined.drop(columns=['Label'])

ros = RandomOverSampler(random_state=0)
X_resampled, y_resampled = ros.fit_resample(X, y)
X_train, X_validation, y_train, y_validation = train_test_split(X_resampled, y_resampled, test_size=0.2,
                                                           random_state=42, stratify=y_resampled)
print('Start training model...')
xgb = XGBClassifier(max_depth=25, n_estimators=500, n_jobs=8)
xgb.fit(X_train, y_train)

y_pred = xgb.predict(X_validation)
print("Model trained with validation accuracy: {:.2f}".format(accuracy_score(y_validation, y_pred)))
print("Serializing model.....")

# Saving model
joblib.dump(xgb, 'xgb_inference.joblib')