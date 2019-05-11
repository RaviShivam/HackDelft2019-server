from flask import Flask, request, json #import main Flask class and request object

app = Flask(__name__) #create the Flask app
allsubmissions = json.loads(open('users/001.json').read())

@app.route('/submissions')
def jsonexample():
    if not allsubmissions:
        return json.dumps([])
    else:
        return json.dumps(allsubmissions)

@app.route('/newsubmit', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'application/json':
        new_message = request.json
        allsubmissions.append(new_message)
        # Classify

        auto_approve = True
        return json.dumps({'auto_approve': auto_approve})

    else:
        return "415 Unsupported Media Type ;)"


if __name__ == '__main_':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000
