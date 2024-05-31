from flask import Flask, render_template, request, jsonify
import requests


# Flask instance
app = Flask(__name__, template_folder='templates')

# default route
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/msg", methods=['POST'])
def msg():


    response = requests.post("http://164.8.215.49:5005/webhooks/rest/webhook", json=request.get_json())


    if response.ok:
        return jsonify(response.json()), 200
    else:
        return "Error: No response", 500

@app.route('/about', methods=['GET'])
def about():
    return


if __name__ == '__main__':
    app.run(debug=True)