from flask import Flask, request, json #import main Flask class and request object

app = Flask(__name__) #create the Flask app
f = open('users/002.json').read()
allsubmissions = json.loads(f.read())
keys = len(allsubmissions)

@app.route('/submissions')
def jsonexample():
    if not allsubmissions:
        return json.dumps([])
    else:
        return json.dumps(allsubmissions)

@app.route('/newsubmit', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'application/json':
        new_message = json.loads(request.json)
        new_message["declaration-id"] = keys
        keys = keys + 1

        # Classify
        auto_approve = True
        new_message["status"] = 'approved' if auto_approve else 'pending'
        allsubmissions.append(new_message)
        json.dumps(allsubmissions, f)
        return json.dumps({'auto_approve': auto_approve})

    else:
        return "415 Unsupported Media Type ;)"


if __name__ == '__main_':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000