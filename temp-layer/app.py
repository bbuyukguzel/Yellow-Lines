from flask import Flask, request
from flask_cors import CORS, cross_origin
import time

app = Flask(__name__) #create the Flask app
CORS(app)


@app.route('/generate-mirror', methods=['GET', 'POST'])
def generate_mirror():
    data = request.data
    time.sleep(5)
    return 'Don\'t Panic.'


if __name__ == '__main__':
    app.run(debug=True, port=5000)
