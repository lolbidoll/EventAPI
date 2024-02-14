from flask import Flask, render_template, request
import csv
import json
import http.client
import ssl

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file'].read().decode('utf-8').splitlines()
        APIk = request.form.get('apikey')
        assetid = request.form.get('aid')
        epapi = request.form.get('endpoint')
        coname = request.form.get('colname')
        aw = request.form.get('aws')
        if file:
            # Read CSV file
            reader = csv.DictReader(file)
            events = [row[coname] for row in reader]

            # Trigger API
            for event in events:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE

                conn = http.client.HTTPSConnection(epapi, context=context)
                payload = json.dumps([
                    {
                        "asset_id": assetid,
                        "activity_name": event,
                        "identity": "9155892115",
                        "activity_source": aw,
                        "timestamp": "2024-01-13T20:30:28+05:30",
                        "activity_params": {
                                "amount": 120.45,
                                "prid": "ibaeufnowerjfiojoi3e2903rdq02",
                                "prqt": 22,
                                "date": "2024-01-13 13:03:01"
                            }
                    }
                ])
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + APIk
                }
                conn.request("POST", "/v1/activity/upload", payload, headers)
                res = conn.getresponse()
                data = res.read()
                print(data.decode("utf-8"))
            return render_template("login.html");
            #return 'File uploaded and events added to Panel!'

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
