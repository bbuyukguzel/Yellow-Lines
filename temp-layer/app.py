from flask import Flask, request
from flask_cors import CORS, cross_origin
import time
import json
import subprocess
from tempfile import NamedTemporaryFile
from random import randint

app = Flask(__name__) #create the Flask app
CORS(app)

tmpDIR = './static/mirrors'
puppeteerDIR = '../puppeteer-jobs/generate-mirror.js'


@app.route('/generate-mirror', methods=['GET', 'POST'])
def generate_mirror():
    time.sleep(randint(0, 3))   # for chaos
    data = request.data
    dataDict = json.loads(data)

    with NamedTemporaryFile(dir=tmpDIR) as tf:
        fname = tf.name + '.png'
        img = 'http://localhost:5000/static/mirrors/' + fname.rsplit('\\')[-1]
    print(fname, img, dataDict['url'])
    command = 'node {} {} {}'.format(puppeteerDIR, dataDict['url'], fname)
    subprocess.call(command, shell=True)
    return 'Don\'t Panic. '+img


if __name__ == '__main__':
    app.run(debug=True, port=5000)
