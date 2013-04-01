#!/usr/bin/env python
"""\
Flask S3 Example
"""

import sha
import hmac
from uuid import uuid4
from json import dumps
from base64 import b64encode
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify


# Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')


# Views
@app.route('/')
def index():
    return render_template('index.html',
        s3_bucket=app.config['AWS_S3_BUCKET'],
        aws_access_key=app.config['AWS_ACCESS_KEY_ID'])


@app.route('/signed_urls')
def signed_urls():
    def make_policy():
        policy_object = {
            'expiration': (datetime.now() + timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            'conditions': [
                {'bucket': app.config['AWS_S3_BUCKET']},
                {'acl': 'public-read'},
                ['starts-with', '$key', 'uploads/'],
                {'success_action_status': '201'}
            ]
        }
        return b64encode(dumps(policy_object))

    def sign_policy(policy):
        return b64encode(hmac.new(app.config['AWS_SECRET_ACCESS_KEY'], policy, sha).digest())

    uuid = uuid4().hex
    title = request.args['title']
    policy = make_policy()

    return jsonify({
        'policy': policy,
        'signature': sign_policy(policy),
        'key': 'uploads/%s-%s' % (uuid, title),
        'success_action_redirect': '/',
    })


# Run development server
if __name__ == '__main__':
    app.run(app.config.get('HOST'), app.config.get('PORT'), app.debug)
