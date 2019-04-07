from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import time
import json
import subprocess
from tempfile import NamedTemporaryFile
from random import randint
import datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from DatabaseOperations import DatabaseOperations
from TaskHandler import TaskHandler

app = Flask(__name__) #create the Flask app

CORS(app)
app.config['SECRET_KEY'] = 'securi'
jwt = JWTManager(app)


tmpDIR = './static/mirrors'
puppeteerDIR = '../puppeteer-jobs/generate-mirror.js'

db_ops = DatabaseOperations()
periodic_task_handler = TaskHandler()
periodic_task_handler.start_task_handler()


@app.route('/generate-mirror', methods=['GET', 'POST'])
def generate_mirror():
    #time.sleep(randint(0, 3))   # for chaos
    data = request.data
    dataDict = json.loads(data)

    with NamedTemporaryFile(dir=tmpDIR) as tf:
        fname = tf.name + '.png'
        img = 'http://localhost:5000/static/mirrors/' + fname.rsplit('\\')[-1]
    print(fname, img, dataDict['url'])

    command = 'node {} {} {}'.format(puppeteerDIR, dataDict['url'], fname)
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = proc.communicate()
    p_status = proc.wait()

    # puppeteer job exited without error
    ret = {}
    if not err:
        jfname = fname.rsplit('.')[0] + '.json'
        with open(jfname) as f:
            data = json.load(f)
            ret[img] = data

    return jsonify(ret)


@app.route('/add-task', methods=['POST'])
def add_task():
    if request.is_json:
        received_data = request.get_json()
        task_id = db_ops.insert_new_task(received_data)

        if task_id is not None:
            task = {'task_id': task_id,
                    'scheduled_time': time.time(),
                    'period': int(received_data['taskFreq']),
                    'call': gcf_part_one,
                    }
            periodic_task_handler.insert_task(task)

    return 'Talk is cheap'


@app.route('/gcf-part-one', methods=['POST'])
def gcf_part_one(task_data):
    required_data = db_ops.get_data(task_data['task_id'], 'taskTargetURL', 'taskTargetId')
    print(required_data)


@app.route('/gcf-part-two', methods=['POST'])
def gcf_part_two():
    # get gcf's request for part two
    pass


@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401


@app.route('/api/v1/register', methods=['POST'])
def register():
    received_data = request.get_json()
    email = received_data.get('email')
    password = received_data.get('password')

    if not email:
        return jsonify({"message": "Missing email parameter"}), 400
    if not password:
        return jsonify({"message": "Missing password parameter"}), 400

    if not db_ops.is_user_exists(email):
        db_ops.add_user(email, password)
        return jsonify({'message': 'You registered!'}), 200
    return jsonify({'message': 'This user already registered'}), 400


@app.route('/api/v1/login', methods=['POST'])
def login():
    received_data = request.get_json()
    email = received_data.get('email')
    password = received_data.get('password')

    if not email:
        return jsonify({"message": "Missing email parameter"}), 400
    if not password:
        return jsonify({"message": "Missing password parameter"}), 400

    user = db_ops.get_user_details(email, password)
    if user is None:
        return jsonify({'success': False, 'message': 'Bad email or password'}), 401

    access_token = create_access_token(identity=str(user['_id']))
    return jsonify({'success': True, 'token': access_token}), 200


@app.route('/verify-token', methods=['POST'])
@jwt_required
def verify_token():
    return jsonify({'success': True}), 200


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
