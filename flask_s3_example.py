#!/usr/bin/env python
"""\
Flask S3 Example
"""

import sha
import hmac
import json
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
    uuid = 1    # TODO: SecureRandom.uuid
    title = request.args['title']
    s3_upload_policy_document = json.dumps({
        'expiration': (datetime.utcnow() + timedelta(minutes=30)).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        'conditions': [
            {'bucket': app.config['AWS_S3_BUCKET']},
            {'acl': 'public-read'},
            #['starts-with', '$key', 'uploads/'],
            {'success_action_status': '201'},
        ]})
    s3_upload_signature = b64encode(hmac.new(app.config['AWS_SECRET_ACCESS_KEY'], s3_upload_policy_document, sha).digest())
    return jsonify({
        'policy': s3_upload_policy_document,
        'signature': s3_upload_signature,
        'key': 'uploads/%s/%s' % (uuid, title),
        'success_action_redirect': '/',
    })


# Run development server
if __name__ == '__main__':
    app.run(app.config.get('HOST'), app.config.get('PORT'), app.debug)
