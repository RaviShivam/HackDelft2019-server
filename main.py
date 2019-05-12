from flask import Flask, request, json #import main Flask class and request object

app = Flask(__name__) #create the Flask app
fname = 'users/002.json'
fread = open(fname).read()
if not fread:
    allsubmissions = []
else:
    allsubmissions = json.loads(fread)

keys = len(allsubmissions)

@app.route('/submissions')
def jsonexample():
    return json.dumps(allsubmissions)

@app.route('/newsubmit', methods = ['POST'])
def api_message():
    global keys
    if request.headers['Content-Type'] == 'application/json':
        new_message = request.json
        new_message["declaration-id"] = keys
        keys = keys + 1

        # Classify
        auto_approve = True
        new_message["status"] = 'approved' if auto_approve else 'pending'
        allsubmissions.append(new_message)
        json.dump(allsubmissions, open(fname, 'w'))
        return json.dumps({'auto_approve': auto_approve})

    else:
        return "415 Unsupported Media Type ;)"


if __name__ == '__main_':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000
