#!/usr/bin/env python
# -*- mode: python -*- -*- coding: utf-8 -*-
from functools import wraps
import json
from urllib.request import urlopen

from flask import (Flask, jsonify, request, current_app, _request_ctx_stack)
from flask_cors import cross_origin
from jose import jwt

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py', silent=True)

# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

def get_token_auth_header():
    '''Obtains the access token from the Authorization Header'''
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({'code': 'authorization_header_missing',
                         'description': 'Authorization header is expected'}, 401)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthError({'code': 'invalid_header',
                         'description':
                            'Authorization header must start with Bearer'}, 401)
    elif len(parts) == 1:
        raise AuthError({'code': 'invalid_header', 'description': 'Token not found'}, 401)
    elif len(parts) > 2:
        raise AuthError({'code': 'invalid_header',
                         'description': 'Authorization header must be Bearer token'}, 401)

    token = parts[1]
    return token

def requires_auth(f):
    '''Determines if the access token is valid'''
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        auth_url = 'https://%s/.well-known/jwks.json' % current_app.config['AUTH0_DOMAIN']
        response = urlopen(auth_url)
        jwks = json.loads(response.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=current_app.config['ALGORITHMS'],
                    audience=current_app.config['API_AUDIENCE'],
                    issuer='https://%s/' % current_app.config['AUTH0_DOMAIN']
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({'code': 'token_expired',
                                 'description': 'token is expired'}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({'code': 'invalid_claims',
                                 'description': 'incorrect claims, '
                                 'please check the audience and issuer'}, 401)
            except Exception as e:
                #print (e)
                raise AuthError({'code': 'invalid_header',
                                 'description': 'Unable to parse authentication token.'},
                                400)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({'code': 'invalid_header',
                         'description': 'Unable to find appropriate key'}, 400)
    return decorated

## Controllers API

# This doesn't need authentication
@app.route('/ping')
@cross_origin(headers=['Content-Type', 'Authorization'])
def ping():
    return "All good. You don't need to be authenticated to call this"

# This does need authentication
@app.route('/secured/ping')
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def secured_ping():
    return "All good. You only get this message if you're authenticated"

if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True)
