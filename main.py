from flask import Flask, request, json #import main Flask class and request object
from forex_python.converter import CurrencyRates
from datetime import datetime
import numpy as np
import joblib


app = Flask(__name__) #create the Flask app
fname = 'users/002.json'
fread = open(fname).read()
if not fread:
    allsubmissions = []
else:
    allsubmissions = json.loads(fread)

keys = len(allsubmissions)
c = CurrencyRates()
xgb1 = joblib.load('xgb_inference.joblib')

currencyi = {'EUR':0, 'GBP':1, 'INR':2, 'Other':3, 'SEK':4, 'USD':5} 
categoryi= {'Certificatescosts':0, 'Hotel':1, 'Other':2, 'Parking':3, 'Travelcosts':4, 'VOG':5}

@app.route('/submissions')
def jsonexample():
    return json.dumps(allsubmissions)


@app.route('/newsubmit', methods = ['POST'])
def api_message():
    global keys
    if request.headers['Content-Type'] == 'application/json':
        new_message = request.json
        # Prep 
        cat = new_message['category']
        curr = new_message['currency']
        decl_date  = datetime.strptime(new_message['date-declare'], '%Y-%m-%d')
        inv_date = datetime.strptime(new_message['date-invoice'], '%Y-%m-%d')
        diff_date = (decl_date - inv_date).days
        amount = new_message['amount']
        foreign_amount = amount*c.get_rate(curr, 'EUR', decl_date)

        # Feature construction
        feats = np.zeros(3)
        feats[0] = amount
        feats[1] = foreign_amount
        feats[2] = diff_date
        ohe_currency = np.zeros(len(currencyi))
        ohe_category = np.zeros(len(categoryi))
        curri = currencyi[curr] if curr in currencyi else currencyi['Other']
        cati = categoryi[cat] if cat in categoryi else categoryi['Other']
        ohe_currency[curri] = 1 
        ohe_category[cati] = 1
        feats = np.concatenate((feats, ohe_currency, ohe_category))

        # Features 
        auto_approve = bool(xgb1.predict(feats)[0])

        new_message["declaration-id"] = keys
        new_message["status"] = 'approved' if auto_approve else 'pending'
        new_message["status-descripion"] = 'none'
        allsubmissions.append(new_message)
        json.dump(allsubmissions, open(fname, 'w'))
        keys = keys + 1
        return json.dumps({'auto_approve': auto_approve})

    else:
        return "415 Unsupported Media Type ;)"


if __name__ == '__main_':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000
